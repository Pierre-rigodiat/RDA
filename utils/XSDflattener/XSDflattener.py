################################################################################
#
# File Name: XSDflattener.py
# 
# Purpose: Flatten an XSD file - gather all dependencies in one file
# 
# V1: 
#    - works with include statement only (not import)
#    - works with API URL in include schemaLocation attribute
#	 - works with local URI
#
# Author: Guillaume SOUSA AMARAL
#         guillaume.sousa@nist.gov
#
#		  Sharief Youssef
#         sharief.youssef@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################

import lxml.etree as etree
from io import BytesIO
from abc import ABCMeta, abstractmethod
import urllib2
from django.utils.importlib import import_module
import os
from mgi.exceptions import MDCSError

settings_file = os.environ.get("DJANGO_SETTINGS_MODULE")
settings = import_module(settings_file)
PARSER_DOWNLOAD_DEPENDENCIES = settings.PARSER_DOWNLOAD_DEPENDENCIES

class XSDFlattener(object):
    __metaclass__ = ABCMeta

    def __init__(self, xmlString):
        self.xmlString = xmlString
        self.dependencies = []

    def get_flat(self):
        parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
        etree.set_default_parser(parser=parser)

        # parse the XML String removing blanks, comments, processing instructions
        xmlTree = etree.parse(BytesIO(self.xmlString.encode('utf-8')))

        # check if it has includes
        includes = xmlTree.findall("{http://www.w3.org/2001/XMLSchema}include")
        if len(includes) > 0:
            for el_include in includes:
                uri = el_include.attrib['schemaLocation']
                flatDependency = self.get_flat_dependency(uri)
                if flatDependency is not None:
                    # append flatDependency to the tree
                    dependencyTree = etree.fromstring(flatDependency)
                    dependencyElements = dependencyTree.getchildren()
                    for element in dependencyElements:
                        xmlTree.getroot().append(element)
                el_include.getparent().remove(el_include)
        return etree.tostring(xmlTree)

    def get_flat_dependency(self, uri):
        try:
            if uri not in self.dependencies:
                self.dependencies.append(uri)
                dependencyContent = self.get_dependency_content(uri)
                xmlTree = etree.parse(BytesIO(dependencyContent.encode('utf-8')))
                includes = xmlTree.findall("{http://www.w3.org/2001/XMLSchema}include")
                if len(includes) > 0:
                    for el_include in includes:
                        uri = el_include.attrib['schemaLocation']
                        flatDependency = self.get_flat_dependency(uri)
                        if flatDependency is not None:
                            # append flatDependency to the tree
                            dependencyTree = etree.fromstring(flatDependency)
                            dependencyElements = dependencyTree.getchildren()
                            for element in dependencyElements:
                                xmlTree.getroot().append(element)
                        el_include.getparent().remove(el_include)
                return etree.tostring(xmlTree)
            else:
                return None
        except:
            return None

    @abstractmethod
    def get_dependency_content(self, uri):
        pass

################################################################################
#
# XSDFlattenerURL
#
# future: flattener that could work using URL and local files
#
################################################################################
class XSDFlattenerURL(XSDFlattener):
    def get_dependency_content(self, uri):
        content = ""

        if PARSER_DOWNLOAD_DEPENDENCIES:
            file = urllib2.urlopen(uri)
            content = file.read()
        else:
            raise MDCSError('Dependency cannot be loaded')

        return content
