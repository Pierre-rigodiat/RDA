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
import zmq
from lxml import etree
import json

REQUEST_TIMEOUT = 10000
REQUEST_RETRIES = 3
SERVER_ENDPOINT = "tcp://127.0.0.1:5555"

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

    if XERCES_VALIDATION and _xerces_exists():
        try:
            xsd_string = etree.tostring(xsd_tree)
            message = {'xsd_string': xsd_string}
            message = json.dumps(message)
            error = send_message(message)
            # error = _xerces_validate_xsd(etree.tostring(xsd_tree))
        except Exception, e:
            print e.message
            error = _lxml_validate_xsd(xsd_tree)
    else:
        error = _lxml_validate_xsd(xsd_tree)

    return error


def send_message(message):
    """
    Send a message to the Schema validation server
    :param message: JSON structure containing parameters
    :return:
    """
    context = zmq.Context(7)

    print "Connecting to server..."
    socket = context.socket(zmq.REQ)
    socket.connect(SERVER_ENDPOINT)

    poll = zmq.Poller()
    poll.register(socket, zmq.POLLIN)

    retries_left = REQUEST_RETRIES
    request = 0

    while retries_left:
        request += 1

        print("Sending request %s..." % request)
        socket.send(message)

        expect_reply = True
        while expect_reply:
            socks = dict(poll.poll(REQUEST_TIMEOUT))
            if socks.get(socket) == zmq.POLLIN:
                reply = socket.recv()
                if not reply:
                    break
                else:
                    print reply
                    if reply == 'ok':
                        reply = None
                    retries_left = 0
                    expect_reply = False
            else:
                print "No response from server, retrying..."
                # Socket is confused. Close and remove it.
                socket.setsockopt(zmq.LINGER, 0)
                socket.close()
                poll.unregister(socket)
                retries_left -= 1
                if retries_left == 0:
                    reply = "Error : XML Validation server seems to be offline, please contact the administrator."
                    break
                print "Reconnecting and resending..."
                # Create new connection
                socket = context.socket(zmq.REQ)
                socket.connect(SERVER_ENDPOINT)
                poll.register(socket, zmq.POLLIN)
                socket.send(message)

    socket.close()
    context.term()

    if reply == 'ok':
        return None
    return reply


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
