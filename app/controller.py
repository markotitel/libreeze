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
        url = self.groupId + "/"
        url = url.replace(".", "/")
        return "http://mirrors.ibiblio.org/maven2/" + url

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
            url = dependency.url() + dependency.artifactId + "/maven-metadata.xml"
            page = requests.get(url)
            if page.status_code == requests.codes.ok:
                tree = ET.fromstring(page.content)
                metadata = tree.iter('versioning')
                for release in metadata:
                    try:
                        rel = release.find('release').text
                    except AttributeError:
                        rel = tree.find("version").text

           # for response in responses:
                if dependency.artifactId == rel:
                    dependency.latest = rel
                    latest = LatestDependency(name = dependency.key(), version = dependency.latest)
                    latest.save()
                    print 'Stored to db ' + latest.__str__()

    return dependencies
