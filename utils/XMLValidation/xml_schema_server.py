import zmq
import time
from lxml import etree
import json
from cStringIO import StringIO

from utils.XMLValidation.xml_schema import _xerces_exists

SERVER_ENDPOINT = "tcp://127.0.0.1:5555"

context = zmq.Context(7)
socket = context.socket(zmq.REP)
socket.bind(SERVER_ENDPOINT)

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
        return "Xerces is not installed"


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
        return "Xerces is not installed"

while True:
    #  Wait for next request from client
    message = socket.recv()
    print "Received request"

    try:
        message = json.loads(message)

        response = ''
        # validate data against schema
        if 'xml_string' in message:
            pass
            # xsd_tree = etree.XML(str(message['xsd_string'].encode('utf-8')))
            # xml_schema = etree.XMLSchema(xsd_tree)
            # xml_doc = etree.XML(str(message['xml_string'].encode('utf-8')))
            # pretty_XML_string = etree.tostring(xml_doc, pretty_print=True)
            # try:
            #     xml_schema.assertValid(etree.parse(StringIO(pretty_XML_string)))
            #     response = 'ok'
            # except Exception, e:
            #     response = e.message
        else:
            xsd_string = message['xsd_string']

            error = _xerces_validate_xsd(xsd_string)
            if error is None:
                error = 'ok'

            response = error

        print response

        socket.send(str(response))
        print "Sent response"
    except:
        pass

    time.sleep(1)



