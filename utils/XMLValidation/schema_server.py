import zmq
import time
from lxml import etree
import json
from cStringIO import StringIO

SERVER_ENDPOINT = "tcp://127.0.0.1:5555"

context = zmq.Context(7)
socket = context.socket(zmq.REP)
socket.bind(SERVER_ENDPOINT)

while True:
    #  Wait for next request from client
    message = socket.recv()
    print "Received request"

    try:
        message = json.loads(message)

        response = ''
        # validate data against schema
        if 'xml_string' in message:
            xsd_tree = etree.XML(str(message['xsd_string'].encode('utf-8')))
            xml_schema = etree.XMLSchema(xsd_tree)
            xml_doc = etree.XML(str(message['xml_string'].encode('utf-8')))
            pretty_XML_string = etree.tostring(xml_doc, pretty_print=True)
            try:
                xml_schema.assertValid(etree.parse(StringIO(pretty_XML_string)))
                response = 'ok'
            except Exception, e:
                response = e.message
        else:
            xsd_tree = etree.XML(str(message['xsd_string'].encode('utf-8')))
            try:
                xml_schema = etree.XMLSchema(xsd_tree)
                response = 'ok'
            except Exception, e:
                response = e.message

        print response

        socket.send(str(response))
        print "Sent response"
    except:
        pass

    time.sleep(1)
