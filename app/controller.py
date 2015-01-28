__author__ = 'nmilinkovic'

import requests
import json

from xml.etree import ElementTree as ET

from app.models import LatestDependency

class MavenDependency:
    def __init__(self, groupId, artifactId, version):
        self.groupId = groupId
        self.artifactId = artifactId
        self.version = version
        self.latest = '???'

    def url(self):
        url = '"' + self.groupId  + '"' + "&rows=20&wt=json"
        return "http://search.maven.org/solrsearch/select?q=g:" + url

    def key(self):
        return self.groupId + '.' + self.artifactId

def check_versions(xml):
    dependencies = parse_xml(xml)
    return retrieve_latest(dependencies)

# TODO add error handling
def parse_xml(xml):
    ns = "{http://maven.apache.org/POM/4.0.0}"

    root = ET.fromstring(xml)

    propertiesMap = {}

    properties = root.find("%sproperties" % ns)
    for prop in properties:
        key = prop.tag[len(ns):]
        value = prop.text
        propertiesMap[key] = value

    parsedList = []

    # parse the xml
    dependencies = root.iter("%sdependency" % ns)
    for dependency in dependencies:
        groupId = dependency.find("%sgroupId" % ns).text
        artifactId = dependency.find("%sartifactId" % ns).text
        version = dependency.find("%sversion" % ns).text
        if version.startswith("${"):
            key = version[2:-1]
            version = propertiesMap[key]
        dep = MavenDependency(groupId, artifactId, version)
        parsedList.append(dep)

    return parsedList


# TODO add task that periodically (once a day) updates latest versions

def retrieve_latest(dependencies):
    # assign latest version to list
    for dependency in dependencies:

        stored = LatestDependency.objects.filter(name=dependency.key())

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
                    latest = LatestDependency(name = dependency.key(), version = dependency.latest)
                    latest.save()
                    print 'Stored to db ' + latest.__str__()

    return dependencies
