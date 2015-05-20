#!/usr/bin/python
from audio import Audio
import huffman
import packet
import time
import socket
import threading

class Server1(threading.Thread):

    def __init__(self,fifo,lock,audio,**kw):
        threading.Thread.__init__(self,**kw)
        self.audio = audio
        self.fifo = fifo
        self.lock = lock

    def run(self):
        while True:
            data = self.audio.get_chunck()        
            self.lock.acquire()
            self.fifo.append(list(data))
            self.lock.release()

class Server2(threading.Thread):

    def __init__(self,fifo,lock,audio,**kw):
        threading.Thread.__init__(self,**kw)
        self.fifo = fifo
        self.lock = lock
        self.audio = audio
        self.chuckSizeToSend = 1000#bytes 1kb
        self.packet = packet.Packet()
        self.fs = 0
        self.port = 1333
        self.dest = '127.0.0.1'
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)


    def run(self):
        while True:
            if len(fifo):
                self.lock.acquire()
                data = self.fifo.pop(0)
                self.lock.release()
                self.huffman(data)
            else:
                time.sleep(0.02)

    def huffman(self,data):
        size = len(data)#in bytes
        hist = huffman.make_hist(data)
        raiz,tree = huffman.make_tree(hist)
        bs = 0#0 si es histograma
        bc = 4096 # 256*2*8#tiene que ser 16 bits
        packHist = self.packet.packHist(self.fs,bs,bc,hist)
        self.send(packHist)
        #print "PACKETS",len(range(0,size,self.chuckSizeToSend))
        for i in range(0,size,self.chuckSizeToSend):
            perKb = data[i:i+self.chuckSizeToSend]
            com = huffman.compress(tree,perKb)
            bs +=1
            bc =  len(perKb)*8
            pack = self.packet.pack(self.fs,bs,bc,com)
            self.send(pack)

        self.fs += 1
        
        #TEST
        """
        s = []
        for pack in self.packets:
            header,d = self.packet.unPack(pack)
            s  += huffman.decode_string(tree,raiz,d)
        print 'SIZE 2',len(s)
        self.packets = []
        self.audio.out_chunck(s)
        """
	 

    def send(self,pack):
        self.sock.sendto(pack,(self.dest,self.port))

if __name__ == '__main__':
    audio = Audio(byte=True,seconds=1)
    fifo = []
    lock = threading.Lock()
    p1 = Server1(fifo,lock,audio)
    p2 = Server2(fifo,lock,audio)
    p1.start()
    p2.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print "stop server"
        for thread in threading.enumerate():
            if thread.isAlive():
                try:
                    thread._Thread__stop()
                except:
                    print 'No se pudo matar todos los threads'
        exit(0)



if __name__ == '__main__' and False:
    audio = Audio(byte=True,seconds=1)
    while 1:
        data = audio.get_chunck()
        d = list(data)
        print 'size',len(d),'bytes 17.28kb'
        hist = huffman.make_hist(d)
        raiz,tree = huffman.make_tree(hist)
        com = huffman.compress(tree,d)
        #print com
        d = huffman.decompress(tree,raiz,com)
        #print 'salida!',d
        t = time.time()
        audio.out_chunck(d)
        elapse = time.time() - t
        print "seconds: %s" % (elapse) 
