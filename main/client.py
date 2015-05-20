#!/usr/bin/python
import packet
import threading
import huffman
from audio import Audio

import socket
import time
import struct


class Client1(threading.Thread):
    
    def __init__(self,fifo,lock,**kw):
        threading.Thread.__init__(self,**kw)
        self.port = 1333
        self.ip = '127.0.0.1'
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.packet = packet.Packet()
        self.sock.bind((self.ip,self.port))
        self.fifo = fifo
        self.lock = lock
        
        self.nBS = 18

    def run(self):
        BS = -1
        FS = -1
        raiz = 0
        tree = []
        audio = []
        while True:
            pack_h, addr = self.sock.recvfrom(10240)
            hist,header,body = self.packet.unPackByType(pack_h)
            fs = header[0]
            bs = header[1]
            bc = header[2]            
                                    #si se reinicia el server
            if hist and fs > FS or (fs == 0 and FS > 3):
                FS = fs
                raiz, tree = huffman.make_tree(body)
                BS = -1
            elif not hist and fs == FS and bs > BS and raiz and len(tree):
                BS = bs
                row = huffman.decode_string(tree,raiz,body)
                self.lock.acquire()
                self.fifo.append(row)
                self.lock.release()

	
class Client2(threading.Thread):

    def __init__(self,fifo,lock,**kw):
        threading.Thread.__init__(self,**kw)
        self.fifo = fifo
        self.lock = lock
        self.audio = Audio(byte=True,seconds=1)
        self.sleep = 1
        self.BS = 18
    

    def run(self):
        while True:         
            self.lock.acquire()
            out = []
            if len(self.fifo) >= self.BS:
                for i in range(self.BS):
                    out += self.fifo.pop(0)
                self.lock.release()
            else:
                self.lock.release()
            if len(out):
                self.audio.out_chunck(out)

if __name__ == '__main__':
    fifo = []
    lock = threading.Lock()
    c1 = Client1(fifo,lock)
    c2 = Client2(fifo,lock)
    c1.start()
    c2.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt,e:
        print str(e)
        print "stop client"
        for thread in threading.enumerate():
            if thread.isAlive():
                try:
                    thread._Thread__stop()
                except:
                    print 'No se pudo matar todos los threads'
        exit(0)
