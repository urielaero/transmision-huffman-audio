import unittest
import struct
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from main import packet

class TestPacket(unittest.TestCase):
    
    def setUp(self):
        self.data = '00111011011010100010000'#16
        #self.data = '00111011011010101000000'#64
        #00111011 01101010 1000000,111
        self.packet = packet.Packet()

    def test_str2int(self):
        res = self.packet.str2int(self.data)
        self.assertEqual(res,[59,106,16,7])#el ultimo dice cuanto ocupa el penultimo

    def test_int2str(self):
        res = self.packet.int2str([59,106,16,7])
        self.assertEqual(res,self.data)

    def test_pack(self):
        res = self.packet.pack(5,4,1,self.data)
        ls = self.packet.str2int(self.data)
        size = len(ls)
        ints = struct.unpack('!iBh'+str(size)+'B',res)
        header = ints[:3]
        content = ints[3:]
        data = self.packet.int2str(content)
        self.assertEqual((header,data),((5,4,1),self.data))

    def test_unPackHeader(self):
        pack = self.packet.pack(5,4,1,self.data) 
        res = self.packet.unPackHeader(pack)
        self.assertEqual(res,(5,4,1))

    def test_unPackBody(self):
        pack = self.packet.pack(5,4,1,self.data) 
        packBody = pack[7:]
        res = self.packet.unPackBody(packBody)
        self.assertEqual(res,(self.data))
        

    def test_unPack(self):
        pack = self.packet.pack(5,4,1,self.data) 
        res = self.packet.unPack(pack)
        self.assertEqual(res,((5,4,1),self.data))

    def test_packHist(self):
        m = [[1459, -1, -1, -1], [1228, -1, -1, -1], [817, -1, -1, -1]]#-1,0.-3.0,1,2
        size = len(m)
        res = self.packet.packHist(5,6,1,m)
        ints = struct.unpack('!iBh'+str(size)+'h',res)
        header = ints[:3]
        content = ints[3:]
        self.assertEqual((header,content),((5,6,1),(1459,1228,817)))

    def test_unPackHist(self):
        m = [[5,-1,-1,-1],[4,-1,-1,-1]]#-1,0.-3.0,1,2
        pack = self.packet.packHist(5,6,1,m)
        res = self.packet.unPackHist(pack)
        self.assertEqual(res,((5,6,1),m))

    def test_unPackHistBody(self):
        m = [[1459, -1, -1, -1], [1228, -1, -1, -1], [817, -1, -1, -1]]#-1,0.-3.0,1,2
        pack = self.packet.packHist(5,6,1,m)
        body = pack[7:]
        res = self.packet.unPackHistBody(body)
        self.assertEqual(res,(m))

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPacket)
    unittest.TextTestRunner(verbosity=2).run(suite)
