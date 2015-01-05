#!/usr/bin/env python

from xml.etree import ElementTree as et
from lxml import html
import requests
import sys
import json

class Dependency:
    def __init__(self, groupId, artifactId, version):
        self.groupId = groupId
        self.artifactId = artifactId
        self.version = version

    def __str__(self):
        return "%s:%s:%s" % (self.groupId, self.artifactId, self.version)

    def url(self, base_url):
        url = '"' + dependency.groupId  + '"' + "&rows=20&wt=json"
        return base_url + url

class bcolors:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    ENDC = '\033[0m'

if __name__ == "__main__":

    ns = "{http://maven.apache.org/POM/4.0.0}"
    maven_repo_url = "http://search.maven.org/solrsearch/select?q=g:"

    group = artifact = version = ""

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
        #print "%s:%s:%s" % (groupId, artifactId, version)
        dep = Dependency(groupId, artifactId, version)
        list.append(dep)

    for dependency in list:
        url = dependency.url(maven_repo_url)
        page = requests.get(url)
        data = json.loads(page.text)
        r = data['response']['docs']
        for a in r:
            if dependency.artifactId == a['a']:
                if dependency.version != a['latestVersion']:
                    print bcolors.WARNING + "%s:%s:>>%s" % (a['a'], dependency.version, a['latestVersion']) + bcolors.ENDC
                else:
                    print bcolors.OKGREEN + "%s:%s:>>%s" % (a['a'], dependency.version, a['latestVersion']) + bcolors.ENDC
