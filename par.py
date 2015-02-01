#!/usr/bin/env python
import requests
import json

from xml.etree import ElementTree as et


class Dependency:
    def __init__(self, groupId, artifactId, version):
        self.groupId = groupId
        self.artifactId = artifactId
        self.version = version
        self.latest = ''

    def url(self, base_url):
        url = '"' + dependency.groupId  + '"' + "&rows=20&wt=json"
        return base_url + url

class bcolors:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    ENDC = '\033[0m'

def check_versions(xml):
    dependencies = parse_xml(xml)
    return retrieve_latest(dependencies)

class MavenViewDependency:
    def __init__(self, group_id, artifact_id, version):
        self.group_id = group_id
        self.artifact_id = artifact_id
        self.version = version
        self.release = ''
        self.latest = ''


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
        project_dependency = MavenViewDependency(group_id, artifact_id, version)
        parsed_list.append(project_dependency)

    return parsed_list


# TODO add task that periodically (once a day) updates latest versions

def retrieve_latest(dependencies):
    # assign latest version to list
    for dependency in dependencies:

        stored = MavenDependency.objects.filter(group_id = dependency.group_id, artifact_id = dependency.artifact_id)

        # First check if the latest dependency is already stored in the database
        if (stored):
            dependency.latest = stored[0].version
            print 'Retrieved from db ' + stored.__str__()
        else:
            # If not, look it up online and store it to the db
            url = dependency.url()
            page = requests.get(url)
            data = json.loads(page.text)
            responses = data['response']['docs']
            for response in responses:
                if dependency.artifactId == response['a']:
                    dependency.latest = response['latestVersion']
                    latest = MavenDependency(group_id = dependency.groupId, artifact_id = dependency.artifactId, latest = dependency.latest, release = dependency.latest)
                    latest.save()
                    print 'Stored to db ' + latest.__str__()



if __name__ == "__main__":

    ns = "{http://maven.apache.org/POM/4.0.0}"
    maven_repo_url = "http://search.maven.org/solrsearch/select?q=g:"

#    group = artifact = version = ""

    tree = et.ElementTree()
    tree.parse("pom.xml")
    root = tree.getroot()

    propertiesMap = {}
    list = []

    properties = root.find("%sproperties" % ns)
    for prop in properties:
        key = prop.tag[len(ns):]
        value = prop.text
        propertiesMap[key] = value
    dependencies = root.iter("%sdependency" % ns)
    for dependency in dependencies:
        groupId = dependency.find("%sgroupId" % ns).text
        artifactId = dependency.find("%sartifactId" % ns).text
        version = dependency.find("%sversion" % ns).text
        if version.startswith("${"):
            key = version[2:-1]
            version = propertiesMap[key]
        dep = Dependency(groupId, artifactId, version)
        list.append(dep)

    for dependency in list:
        url = dependency.url(maven_repo_url)
        page = requests.get(url)
        data = json.loads(page.text)
        r = data['response']['docs']
        for a in r:
            if dependency.artifactId == a['a']:
                if dependency.version == a['latestVersion']:
                    print bcolors.OKGREEN + "%s:%s:>>%s" % (a['a'], dependency.version, a['latestVersion']) + bcolors.ENDC
                else:
                    print bcolors.WARNING + "%s:%s:>>%s" % (a['a'], dependency.version, a['latestVersion']) + bcolors.ENDC
