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


class Server(object):
    def __init__(self, ip, port):
        self.__ip = ip
        self.__port = port
        self.__ctx = None
        self.__socket = None
        self.__sounds_path = 'sounds'
        self.__sounds = {}
        pygame.mixer.init()

    def load_sounds(self):
        sounds = {}
        for item in os.listdir(self.__sounds_path):
            if item.endswith('.wav'):
                sound_file_path = os.path.join(self.__sounds_path,item)
                sound = pygame.mixer.Sound(sound_file_path)
                length = sound.get_length()
                sounds[item] = {'sound':sound,
                                'length':length}
        return sounds

    def serve(self):
        self.__ctx = zmq.Context()
        a = "tcp://%s:%s" % (self.__ip,self.__port)
        self.__socket = self.__ctx.socket(zmq.REP)
        self.__socket.bind(a)
        print a
        print 'loading sounds...'
        self.__sounds = self.load_sounds()
        while True:
            #  Wait for next request from client
            message = self.__socket.recv()
            print message

            if message == "listSounds":
                self.__socket.send("listSoundsResult:%s"%(','.join([item for item in self.__sounds])))
            elif message.startswith("playSound:"):
                sound = message.strip('playSound:')
                snd1 = pygame.mixer.Sound('sounds/%s'%sound)
                channel = snd1.play()
                print snd1.get_length()
                self.__socket.send("playSoundResult:%s:%f"%(sound,snd1.get_length()))


if __name__ == '__main__':

    server = Server('*',5555)
    server.serve()
    #
    # port = 5555
    # ip = '*'
    # if 'OPENSHIFT_PYTHON_IP' in os.environ:
    #     ip = os.environ.get('OPENSHIFT_PYTHON_IP')
    # #ip = '54.88.2.59'
    # context = zmq.Context()
    # socket = context.socket(zmq.REP)
    # a = "tcp://%s:%s" % (ip,port)
    # print a
    # socket.bind(a)
    # #socket.bind("tcp://127.0.0.1:%s" % port)
    # while True:
    #     #  Wait for next request from client
    #     message = socket.recv()
    #     print message
    #
    #     if message == "listSounds":
    #         socket.send("listSoundsResult:%s"%(list_sounds()))
    #     elif message.startswith("playSound:"):
    #         sound = message.strip('playSound:')
    #         snd1 = pygame.mixer.Sound('sounds/%s'%sound)
    #         channel = snd1.play()
    #         print snd1.get_length()
    #         socket.send("playSoundResult:%s:%f"%(sound,snd1.get_length()))
