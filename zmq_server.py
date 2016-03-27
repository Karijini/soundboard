import ConfigParser
import pygame
import os
from collections import OrderedDict
import zmq

class Soundboard(object):
    def __init__(self,ip,port):
        self.__ip = ip
        self.__port = port
        self.__mixer=pygame.mixer.init()
        self.__sounds = OrderedDict()

    def __load_sounds(self):
        self.__sounds.clear()
        cfg = ConfigParser.ConfigParser()
        cfg.readfp(open('sounds.cfg'))
        for section in cfg.sections():
            print section
            if not cfg.has_option(section,"file"):
                continue
            sound_file_path = os.path.join('sounds', cfg.get(section,'file'))
            if not os.path.isfile(sound_file_path):
                print 'ignoring',sound_file_path
                
            sound = pygame.mixer.Sound(sound_file_path)
            length = sound.get_length()
            _in = 0
            if cfg.has_option(section,'in'):
                _in = cfg.getfloat(section,'in')
            _out = length
            if cfg.has_option(section,'out'):
                __out = cfg.getfloat(section,'out')
                if __out < _out:
                    _out = __out
            if _in!=0 or _out!=length:
                print sound
                a1 = pygame.sndarray.samples(sound)
                samples_per_second = pygame.mixer.get_init()[0]
                start_pos_in_samples = int(_in * samples_per_second)
                end_pos_in_samples = int(_out * samples_per_second)
                print start_pos_in_samples, end_pos_in_samples
                a2 = a1[start_pos_in_samples:end_pos_in_samples]
                
                sound = pygame.sndarray.make_sound(a2)
            print section,sound_file_path, sound.get_length()

            self.__sounds[section] = {'sound':sound,
                                      'length':sound.get_length(),
                                      }
            self.__sounds[section]['fade_in']= 0
            if cfg.has_option(section,'fade_in'):
                self.__sounds[section]['fade_in']=cfg.getfloat(section,'fade_in')
            self.__sounds[section]['fade_out']= 0
            if cfg.has_option(section,'fade_out'):
                self.__sounds[section]['fade_out']=cfg.getfloat(section,'fade_out')

        self.__sounds['stop']={'length':500}
    
    def start(self):
        self.__ctx = zmq.Context()
        a = "tcp://%s:%s" % (self.__ip,self.__port)
        self.__socket = self.__ctx.socket(zmq.REP)
        self.__socket.bind(a)
        print a
        print 'loading sounds...'
        self.__load_sounds()
        while True:
            #  Wait for next request from client
            message = self.__socket.recv()
            print message

            if message == "listSounds":
                self.__socket.send("listSoundsResult:%s"%(','.join([item for item in self.__sounds])))
            elif message.startswith("playSound:"):
                sound_name = message.split('playSound:')[1]
                if sound_name == "stop":
                    self.stop_sounds()
                    length = 1.0
                else:
                    length = self.play_sound(sound_name)
                self.__socket.send("playSoundResult:%s:%f"%(sound_name,length))

    def play_sound(self, sound_name):
        sound = self.__sounds.get(sound_name,None)
        print self.__sounds.keys()
        print sound
        if sound == None:
            return False
        sound['sound'].play(fade_ms=int(sound['fade_in']*1000))
        return sound['length']

    def stop_sounds(self):
        pygame.mixer.fadeout(self.__sounds['stop']['length'])


if __name__ == "__main__":
    # soundboard = Soundboard()
    # print soundboard.get_sounds()
    # soundboard.play_sound('intro')
    # while True:
    #     pass
    server = Soundboard('*',5555)
    server.start()
