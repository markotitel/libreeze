__author__ = 'nmilinkovic'

import requests
import json

from xml.etree import ElementTree as ET

from app.models import MavenDependency

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
            dependency.latest = stored[0].latest
            dependency.release = stored[0].release
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

    return dependencies
