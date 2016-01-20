#!/usr/bin/python
import os
import time
import pygame

# virtenv = os.environ['OPENSHIFT_PYTHON_DIR'] + '/virtenv/'
# virtualenv = os.path.join(virtenv, 'bin/activate_this.py')
# try:
#     execfile(virtualenv, dict(__file__=virtualenv))
# except IOError:
#     pass
#
import zmq

def list_sounds():
    sounds = []
    for item in os.listdir('sounds'):
        if item.endswith('.wav'):
            sounds.append(item)
    return ','.join(sounds)

if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()

    port = 5555
    ip = '*'
    if 'OPENSHIFT_PYTHON_IP' in os.environ:
        ip = os.environ.get('OPENSHIFT_PYTHON_IP')
    #ip = '54.88.2.59'
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    a = "tcp://%s:%s" % (ip,port)
    print a
    socket.bind(a)
    #socket.bind("tcp://127.0.0.1:%s" % port)
    while True:
        #  Wait for next request from client
        message = socket.recv()
        print message
        #print "Received request: ", message
        #time.sleep (1)
        if message == "listSounds":
            socket.send("listSoundsResult:%s"%(list_sounds()))
        elif message.startswith("playSound:"):
            sound = message.strip('playSound:')
            snd1 = pygame.mixer.Sound('sounds/%s'%sound)
            channel = snd1.play()
            channel.set_endevent(pygame.SONG_END)
            socket.send("playSound:%s"%(sound))
