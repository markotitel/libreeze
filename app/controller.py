__author__ = 'nmilinkovic'

import requests

from pkg_resources import parse_version
from xml.etree import ElementTree as ET

from app.models import MavenRepoDependency


def check_versions(xml):
    dtos = parse_xml(xml)
    return retrieve_latest(dtos)


class MavenDependencyDTO:
    def __init__(self, group_id, artifact_id, version):
        self.group_id = group_id
        self.artifact_id = artifact_id
        self.version = version
        self.release = ''
        self.latest = ''
        self.up_to_date = True


# TODO add error handling
def parse_xml(xml):
    ns = "{http://maven.apache.org/POM/4.0.0}"

    root = ET.fromstring(xml)

    properties_map = {}

    properties = root.find("%sproperties" % ns)
    for prop in properties:
        key = prop.tag[len(ns):]
        value = prop.text
        properties_map[key] = value

    parsed_list = []

    # parse the xml
    dependencies = root.iter("%sdependency" % ns)
    for dependency in dependencies:
        group_id = dependency.find("%sgroupId" % ns).text
        artifact_id = dependency.find("%sartifactId" % ns).text
        version = dependency.find("%sversion" % ns).text
        if version.startswith("${"):
            key = version[2:-1]
            version = properties_map[key]
        dto = MavenDependencyDTO(group_id, artifact_id, version)
        parsed_list.append(dto)

    return parsed_list


# TODO add task that periodically (once a day) updates latest versions

def determine_latest_version(versions):
    latest = ''
    for version in versions:
        is_latest = parse_version(version.text) > parse_version(latest)
        if is_latest:
            latest = version.text
    return latest


def retrieve_latest(dtos):

    for dto in dtos:

        stored = MavenRepoDependency.objects.filter(group_id=dto.group_id, artifact_id=dto.artifact_id)

        # First check if the latest dependency is already stored in the database
        if stored:
            dto.latest = stored[0].latest
            dto.release = stored[0].release
            print 'Retrieved from db ' + stored[0].__str__()
        else:
            # If not, look it up online and store it to the db
            url = "http://repo1.maven.org/maven2/" + dto.group_id.replace('.', '/') \
                  + '/' + dto.artifact_id + "/maven-metadata.xml"
            maven_metadata_xml_page = requests.get(url)

            if maven_metadata_xml_page.status_code == 200:

                root = ET.fromstring(maven_metadata_xml_page.text)

                latest_element = root.find("./versioning/latest")
                latest = ''
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

                dto.latest = latest
                dto.release = release

                maven_dependency = MavenRepoDependency(group_id=dto.group_id, artifact_id=dto.artifact_id,
                                                       latest=dto.latest, release=dto.release)
                maven_dependency.save()
                print 'Stored to db ' + maven_dependency.__str__()

            else:
                # This dependency is not found in the maven repo
                print "Received response code %s for url %s" % (maven_metadata_xml_page.status_code, url)

        # Set up_to_date flag
        if dto.latest:
            dto.up_to_date = dto.version == dto.latest
        else:
            if dto.release:
                dto.up_to_date = dto.version == dto.release

    return dtos
