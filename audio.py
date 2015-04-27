#!/usr/bin/python

import alsaaudio
import sys
#default
SIZE = 160
CHANNELS = 1
RATE = 44100

class Audio(object):

    def __init__(self,rate=RATE,size=SIZE,channels=CHANNELS,seconds=1,byte=False):
        #print size
        self.inBytes = byte
        self.size = size
        self.rate = rate
        self.seconds = seconds
        sound_in = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NORMAL)
        sound_in.setchannels(channels)
        sound_in.setrate(rate)
        sound_in.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        sound_in.setperiodsize(size)
        self.input = sound_in
        sound_out = alsaaudio.PCM()
        sound_out.setchannels(channels)
        sound_out.setrate(rate)
        sound_out.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        sound_out.setperiodsize(size)
        self.out = sound_out

    def get_chunck(self):
        #size,data = self.input.read()
        #print 's',size
        #return data
        res = ''
        for i in range(0, self.rate / self.size * self.seconds):
            size,data = self.input.read()
            #print size
            #print len(data)
            res += data
        if self.inBytes:
            return bytearray(res)
        return res
        
    def out_chunck(self,chunk):
    	#self.out.write(chunk)
        if type(chunk) == list:
            chunk = bytearray(chunk)
            
        if self.inBytes:
            chunk = str(chunk)
        self.out.write(chunk)

"""
inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NONBLOCK)
inp.setchannels(CHANNELS)
inp.setrate(RATE)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
inp.setperiodsize(SIZE)

sound_out = alsaaudio.PCM()
sound_out.setchannels(CHANNELS)
sound_out.setrate(RATE)
sound_out.setformat(alsaaudio.PCM_FORMAT_S16_LE)
sound_out.setperiodsize(SIZE)
"""

if __name__ == '__main__':
    audio = Audio(seconds=1)
    while 1:
        data = audio.get_chunck()
        audio.out_chunck(data)
    
    """
    f = open('datos.o','wb+')
    f.write(data)
    f.close()
    print sys.getsizeof(data)

    audio.out_chunck(data)
    while True:
    #for i in range(0, 44100 / SIZE * RECORD_SECONDS):
    # Read data from device
        l,data = inp.read()
        sound_out.write(data)
    """
