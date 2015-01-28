__author__ = 'nmilinkovic'

import requests
import json

from xml.etree import ElementTree as ET

class Dependency:
    def __init__(self, groupId, artifactId, version):
        self.groupId = groupId
        self.artifactId = artifactId
        self.version = version

    def url(self, base_url):
        url = '"' + self.groupId  + '"' + "&rows=20&wt=json"
        return base_url + url


def parse_xml(xml):
    ns = "{http://maven.apache.org/POM/4.0.0}"

    root = ET.fromstring(xml)

    propertiesMap = {}
    list = []

    properties = root.find("%sproperties" % ns)
    for prop in properties:
        key = prop.tag[len(ns):]
        value = prop.text
        propertiesMap[key] = value
        print propertiesMap

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

    return list