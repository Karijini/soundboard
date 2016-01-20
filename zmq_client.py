#!/usr/bin/python
import os
import time
import zmq

if __name__ == '__main__':
    port = 5555
    ip = 'python-timer.rhcloud.com'
    ip = '192.168.0.18'
    context = zmq.Context()
    print "Connecting to server..."
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://%s:%s" % (ip,port))
    socket.send ("Hello")
    print socket.recv()