#!/usr/bin/python
import struct

class Packet(object):
    
    def __init__(self):
        pass

    def str2int(self,string):
        ls = []
        size = len(string)
        for i in range(0,size,8):
            st = string[i:i+8] 
            ls.append(int(st,2))

        if len(st) < 8:
            ls.append(len(st))
        else:
            ls.append(0)

        return ls
            
    def int2str(self,ls):
        res = ''
        last = ls[-1]
        for i,v in enumerate(ls[:-1]):
            tmp = str(bin(v))[2:]
            if len(tmp) < 8:
                add = 8
                if i == len(ls)-2 and last != 0 :
                    add = last
                    
                for i in range(len(tmp),add):
                    tmp = '0'+tmp
            res += tmp
        return res

    def pack(self,fs,bs,bc,data):
        ls = self.str2int(data)
        size = len(ls)
        d = struct.pack('!'+str(size)+'B',*ls)
        pack = struct.pack("!iBh",fs,bs,bc)#header
        pack += d
        return pack

    def unPackHeader(self,packet):
        headerP = packet[:7]
        header = struct.unpack('!iBh',headerP)
        return header

    def unPackBody(self,packet):#solo el cuerpo
        size = len(packet)
        dataInt = struct.unpack('!'+str(size)+'B',packet)
        data = self.int2str(dataInt)
        return data

    def unPackByType(self,packet):
        headerP = packet[:7]
        dataP = packet[7:]
        size = len(dataP)
        header = struct.unpack('!iBh',headerP)
        hist = False
        if header[1] == 0:#hist
            d = self.unPackHistBody(dataP)
            hist = True
        else:
            d = self.unPackBody(dataP)
        return hist,header,d

    def unPack(self,packet):#header+cuerpo
        headerP = packet[:7]
        dataP = packet[7:]
        size = len(dataP)
        header = struct.unpack('!iBh',headerP)
        dataInt = struct.unpack('!'+str(size)+'B',dataP)
        data = self.int2str(dataInt)
        return header,data

    def packHist(self,fs,bs,bc,m):
        ls = []
        for l in m:
            ls.append(l[0])
        
        size = len(ls)
        d = struct.pack('!'+str(size)+'h',*ls)
        pack = struct.pack("!iBh",fs,bs,bc)#header
        pack += d
        return pack

    def unPackHistBody(self,packet):#solo body cuando es hist
        size = len(packet)/2
        dataInt = struct.unpack('!'+str(size)+'h',packet)
        res = []
        for i in dataInt:
            res.append([i,-1,-1,-1])
            
        return res 

    def unPackHist(self,packet):#header+body
        headerP = packet[:7]
        dataP = packet[7:]
        size = len(dataP)/2
        header = struct.unpack('!iBh',headerP)
        dataInt = struct.unpack('!'+str(size)+'h',dataP)
        res = []
        for i in dataInt:
            res.append([i,-1,-1,-1])
            
        return header,res 
