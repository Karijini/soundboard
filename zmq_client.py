#!/usr/bin/python
import os
import time
import zmq

if __name__ == '__main__':
    port = 5555
    ip = 'python-timer.rhcloud.com'
    ip = '127.0.0.1'
    context = zmq.Context()
    print "Connecting to server..."
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://%s:%s" % (ip,port))
    socket.send ("listSounds")
    print socket.recv()
    socket.send ("playSound:intro")
    print socket.recv()
    socket.send ("playSound:level_up")
    print socket.recv()