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
 
import sys
import zmq
import os
 
REQUEST_TIMEOUT = 10000
REQUEST_RETRIES = 3
SERVER_ENDPOINT = "tcp://127.0.0.1:5555"
 
 
def sendRDF(rdfStr):
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
        socket.send(rdfStr.encode('utf-8'))
         
        expect_reply = True
        while expect_reply:
            socks = dict(poll.poll(REQUEST_TIMEOUT))
            if socks.get(socket) == zmq.POLLIN:
                reply = socket.recv()
                if not reply:
                    break
                else:
                    print reply
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
                    print "Error : Server seems to be offline, abandoning"
                    break
                print "Reconnecting and resending..."
                # Create new connection
                socket = context.socket(zmq.REQ)
                socket.connect(SERVER_ENDPOINT)
                poll.register(socket, zmq.POLLIN)
                socket.send(rdfStr.encode('utf-8'))
 
    socket.close()
    context.term()
