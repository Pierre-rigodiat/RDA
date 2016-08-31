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
from mgi.exceptions import MDCSError
import os
from django.utils.importlib import import_module

settings_file = os.environ.get("DJANGO_SETTINGS_MODULE")
settings = import_module(settings_file)
XERCES_VALIDATION = settings.XERCES_VALIDATION


def validate_xml_schema(xsd_tree):
    """
    Send XML Schema to server to be validated
    :param xsd_tree:
    :return:
    """
    error = None

    if XERCES_VALIDATION:
        try:
            error = _xerces_validate_xsd(etree.tostring(xsd_tree))
        except Exception, e:
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
        try:
            error = _xerces_validate_xml(etree.tostring(xsd_tree), pretty_XML_string)
        except Exception, e:
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
        import xerces_wrapper
        error = xerces_wrapper.validate_xsd(xsd_string)

        if len(error) <= 1:
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
        import xerces_wrapper
        error = xerces_wrapper.validate_xsd(xsd_string, xml_string)

        if len(error) <= 1:
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
        xml_schema = etree.XMLSchema(xsd_tree)
    except Exception, e:
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
        xml_schema = etree.XMLSchema(xsd_tree)
        xml_schema.assertValid(xml_tree)
    except Exception, e:
        error = e.message  
    return error
