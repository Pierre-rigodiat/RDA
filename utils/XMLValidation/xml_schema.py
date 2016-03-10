################################################################################
#
# File Name: rdfPublisher.py
# Application: curate
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


import zmq
from lxml import etree
import json
  
REQUEST_TIMEOUT = 10000
REQUEST_RETRIES = 3
SERVER_ENDPOINT = "tcp://127.0.0.1:5555"
  
  
def validate_xml_schema(xsd_tree):
    """
    Send XML Schema to server to be validated
    :param xsd_tree:
    :return:
    """
    xsd_string = etree.tostring(xsd_tree)
    message = {'xsd_string': xsd_string}
    message = json.dumps(message)
    return send_message(message)


def validate_xml_data(xsd_tree, xml_tree):
    """
    Send XML Data and XML Schema to server to validate data against the schema
    :param xsd_tree:
    :param xml_tree:
    :return:
    """
    xsd_string = etree.tostring(xsd_tree)
    xml_string = etree.tostring(xml_tree)
    message = {'xsd_string': xsd_string,
               'xml_string': xml_string}
    message = json.dumps(message)
    return send_message(message)


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

    return reply