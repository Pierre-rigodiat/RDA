################################################################################
#
# File Name: xml_schema.py
# Application: utils
# Purpose:   
#
# Author: Sharief Youssef
#         sharief.youssef@nist.gov
#
#         Guillaume SOUSA AMARAL
#         guillaume.sousa@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################


from lxml import etree
from cStringIO import StringIO
import threading
from mgi.exceptions import MDCSError
from subprocess import check_output
import os
import sys
from django.utils.importlib import import_module

settings_file = os.environ.get("DJANGO_SETTINGS_MODULE")
settings = import_module(settings_file)
SITE_ROOT = settings.SITE_ROOT
XERCES_VALIDATION = settings.XERCES_VALIDATION


def validate_xml_schema(xsd_tree):
    """
    Send XML Schema to server to be validated
    :param xsd_tree:
    :return:
    """    
    error = None
    
    if XERCES_VALIDATION:
        print "XERCES VALIDATION"
        try:
            error = _xerces_validate_xsd(etree.tostring(xsd_tree))
        except Exception, e:
            print "EXCEPTION DURING XERCES VALIDATION"
            print e.message
            error = _lxml_validate_xsd(xsd_tree)
    else:
        error = _lxml_validate_xsd(xsd_tree)

    return error


def validate_xml_data(xsd_tree, xml_tree):
    """
    Send XML Data and XML Schema to server to validate data against the schema
    :param xsd_tree:
    :param xml_tree:
    :return:
    """
    error = None
    pretty_XML_string = etree.tostring(xml_tree, pretty_print=True)
    
    if XERCES_VALIDATION:
        print "XERCES VALIDATION"
        try:
            error = _xerces_validate_xml(etree.tostring(xsd_tree), pretty_XML_string)
        except Exception, e:
            print "EXCEPTION DURING XERCES VALIDATION"
            print e.message
            error = _lxml_validate_xml(xsd_tree, etree.parse(StringIO(pretty_XML_string)))
    else:
        error = _lxml_validate_xml(xsd_tree, etree.parse(StringIO(pretty_XML_string)))

    return error


def _xerces_exists():
    """
    Check if xerces wrapper is installed
    :return:
    """
    try:
        __import__('xerces_wrapper')
    except ImportError:
        print "XERCES DOES NOT EXIST"
        return False
    else:
        print "XERCES EXISTS"
        return True


def _xerces_validate_xsd(xsd_string):
    """
    Validate schema using Xerces
    :param xsd_string
    :return: errors
    """
    if _xerces_exists():        
        print "VALIDATE SCHEMA USING XERCES"        
        # run xerces as subprocess to avoid server crashing on validation
        python_exe = sys.executable
        xerces_cmd = os.path.join(SITE_ROOT, 'utils', 'xerces_wrapper', 'xerces_wrapper_cmd.py')
        print xerces_cmd
        error = check_output([python_exe, 
                              xerces_cmd,
                              '-xsd',
                              xsd_string])
        print "XERCES VALIDATION DONE"

        if len(error) <= 1:
            print "XERCES SAYS VALID"
            error = None
    
        return error
    else:
        raise MDCSError("Xerces is not installed")
        

def _xerces_validate_xml(xsd_string, xml_string):
    """
    Validate document using Xerces
    :param xsd_string
    :param xml_string
    :return: errors
    """
    if _xerces_exists():        
        print "VALIDATE DATA USING XERCES"        
        # run xerces as subprocess to avoid server crashing on validation
        python_exe = sys.executable
        xerces_cmd = os.path.join(SITE_ROOT, 'utils', 'xerces_wrapper', 'xerces_wrapper_cmd.py')
        print xerces_cmd
        error = check_output([python_exe, 
                              xerces_cmd,
                              '-xsd',
                              xsd_string,
                              '-xml',
                              xml_string])
        print "XERCES VALIDATION DONE"

        if len(error) <= 1:
            print "XERCES SAYS VALID"
            error = None
    
        return error
    else:
        raise MDCSError("Xerces is not installed")

                              
def _lxml_validate_xsd(xsd_tree):                          
    """
    Validate schema using LXML
    :param xsd_tree
    :return: errors
    """
    error = None
    try:
        print "VALIDATE SCHEMA USING LXML"
        xml_schema = etree.XMLSchema(xsd_tree)
        print "LXML VALIDATION DONE"
    except Exception, e:
        print "LXML SAYS INVALID"
        error = e.message  
    return error


def _lxml_validate_xml(xsd_tree, xml_tree):                          
    """
    Validate document using LXML
    :param xsd_tree
    :return: errors
    """
    error = None
    try:
        print "VALIDATE DATA USING LXML"
        xml_schema = etree.XMLSchema(xsd_tree)
        xml_schema.assertValid(xml_tree)
        print "LXML VALIDATION DONE"
    except Exception, e:
        print "LXML SAYS INVALID"
        error = e.message  
    return error
