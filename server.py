#!/usr/bin/python

from audio import Audio
from huffman import compress, decompress

if __name__ == '__main__':
    audio = Audio(byte=True,seconds=5)
    data = audio.get_chunck()
    table,com = compress(data)
    #print com
    d = decompress(table,com)
    audio.out_chunck(d)
    #table, hist = codified_dat(data)

