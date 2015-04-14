__author__ = 'nmilinkovic'

import requests

from pkg_resources import parse_version
from xml.etree import ElementTree as ET

from app.models import RepoDependency

MAVEN_NAMESPACE = "{http://maven.apache.org/POM/4.0.0}"


def process_pom_file(xml):
    project = parse_xml(xml)
    return retrieve_latest(project)


class MavenProjectDTO:
    def __init__(self, group_id, artifact_id, version, dependencies):
        self.group_id = group_id
        self.artifact_id = artifact_id
        self.version = version
        self.dependencies = dependencies


class MavenDependencyDTO:
    def __init__(self, group_id, artifact_id, version):
        self.group_id = group_id
        self.artifact_id = artifact_id
        self.version = version
        self.release = ''
        self.latest = ''
        self.up_to_date = True


# Need this to handle pom files without namespace
def node_find(root, tag):
    node = root.find("%s%s" % (MAVEN_NAMESPACE, tag))
    if node is None:
        node = root.find(tag)
    return node


def node_iter(root, tag):
    node = root.iter("%s%s" % (MAVEN_NAMESPACE, tag))
    if node is None:
        node = root.iter(tag)
    return node


# TODO add error handling
def parse_xml(xml):

    root = ET.fromstring(xml)

    project_group_id = node_find(root, "groupId").text
    project_artifact_id = node_find(root, "artifactId").text
    project_version = node_find(root, "version").text

    properties_map = {}

    property_nodes = node_find(root, "properties")
    if property_nodes is not None:
        for node in property_nodes:
            key = node.tag[len(MAVEN_NAMESPACE):]
            value = node.text
            properties_map[key] = value

    dependencies = []

    # parse the xml
    dependency_nodes = node_iter(root, "dependency")
    for node in dependency_nodes:

        group_id = node_find(node, "groupId").text

        artifact_id = node_find(node, "artifactId").text

        version = ''
        node_version = node_find(node, "version")
        if node_version is not None:
            version = node_version.text

        if version.startswith("${"):
            key = version[2:-1]
            if key in properties_map:
                version = properties_map[key]

        dependency = MavenDependencyDTO(group_id, artifact_id, version)
        dependencies.append(dependency)

    return MavenProjectDTO(project_group_id, project_artifact_id, project_version, dependencies)


# TODO add task that periodically (once a day) updates latest versions

def determine_latest_version(versions):
    latest = ''
    for version in versions:
        is_latest = parse_version(version.text) > parse_version(latest)
        if is_latest:
            latest = version.text
    return latest


def build_maven_repo_url(group_id, artifact_id):
    return "http://repo1.maven.org/maven2/" + group_id.replace('.', '/')  + '/' + artifact_id + "/maven-metadata.xml"


def check_maven_repo_dependency(group_id, artifact_id):
    url = build_maven_repo_url(group_id, artifact_id)
    maven_metadata_xml_page = requests.get(url)

    if maven_metadata_xml_page.status_code == 200:

        root = ET.fromstring(maven_metadata_xml_page.text)

        latest_element = root.find("./versioning/latest")
        if latest_element is not None:
            latest = latest_element.text
            print "Retrieved latest directly from metadata: " + latest
        else:
            versions = root.iter("version")
            latest = determine_latest_version(versions)
            print "Determined latest from metadata: " + latest

        release = ''
        release_element = root.find("./versioning/release")
        if release_element is not None:
            release = release_element.text
            print "Retrieved release from metadata: " + release

        return latest, release

    else:
        # This dependency is not found in the maven repo
        print "Received response code %s for url %s" % (maven_metadata_xml_page.status_code, url)
        return None, None


def retrieve_latest(project):

    for dto in project.dependencies:

        stored = RepoDependency.objects.filter(namespace=dto.group_id, name=dto.artifact_id)

        # First check if the latest dependency is already stored in the database
        if stored:
            dto.latest = stored[0].latest
            dto.release = stored[0].release
            print 'Retrieved from db ' + stored[0].__str__()
        else:

            latest, release = check_maven_repo_dependency(dto.group_id, dto.artifact_id)

            if latest is not None:
                dto.latest = latest
                dto.release = release

                dependency = RepoDependency(namespace=dto.group_id, name=dto.artifact_id,
                                            latest=dto.latest, release=dto.release)
                dependency.save()
                print 'Stored to db ' + dependency.__str__()

        # Set up_to_date flag
        if dto.release:
            dto.up_to_date = dto.version == dto.release
        elif dto.latest:
            dto.up_to_date = dto.version == dto.latest

    return project
