import zmq
import time
from lxml import etree
import json

SERVER_ENDPOINT = "tcp://127.0.0.1:5555"

context = zmq.Context(7)
socket = context.socket(zmq.REP)
socket.bind(SERVER_ENDPOINT)

while True:
    #  Wait for next request from client
    message = socket.recv()
    print "Received request"

    message = json.loads(message)

    response = ''
    # validate data against schema
    if 'xml_string' in message:
        xsd_tree = etree.XML(str(message['xsd_string'].encode('utf-8')))
    else:
        xsd_tree = etree.XML(str(message['xsd_string'].encode('utf-8')))
        try:
            xmlSchema = etree.XMLSchema(xsd_tree)
            response = 'ok'
        except Exception, e:
            response = e.message

    print response

    socket.send(str(response))
    print "Sent response"

    time.sleep(1)
