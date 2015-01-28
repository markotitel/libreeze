__author__ = 'nmilinkovic'

import requests
import json

from xml.etree import ElementTree as ET

class Dependency:
    def __init__(self, groupId, artifactId, version):
        self.groupId = groupId
        self.artifactId = artifactId
        self.version = version
        self.latest = '???'

    def url(self):
        url = '"' + self.groupId  + '"' + "&rows=20&wt=json"
        return "http://search.maven.org/solrsearch/select?q=g:" + url


def parse_xml(xml):
    ns = "{http://maven.apache.org/POM/4.0.0}"

    root = ET.fromstring(xml)

    propertiesMap = {}


    properties = root.find("%sproperties" % ns)
    for prop in properties:
        key = prop.tag[len(ns):]
        value = prop.text
        propertiesMap[key] = value
        print propertiesMap
        print propertiesMap

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
        dep = Dependency(groupId, artifactId, version)
        parsedList.append(dep)

    # assign latest version to list
    # TODO split this later in another method
    for dependency in parsedList:
        url = dependency.url()
        page = requests.get(url)
        data = json.loads(page.text)
        responses = data['response']['docs']
        for response in responses:
            if dependency.artifactId == response['a']:
                dependency.latest = response['latestVersion']

    return parsedList