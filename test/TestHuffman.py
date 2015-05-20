import unittest
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from main import huffman

class TestHuffman(unittest.TestCase):
    def setUp(self):
        self.data = [0,2,2,1,1,1,5,5,5,5,5,5,5,5]
        self.table = huffman.get_clear_data(-1,4,512)
        huffman.set_frequency(self.table,self.data)

    def test_get_clear_data(self):
        table = huffman.get_clear_data(-1,4,512)
        res = (table[0][0],len(table[0]),len(table))
        self.assertEqual(res,(-1,4,512))
    
    def test_get_min(self):
        res = huffman.get_min(self.table)
        
        self.assertEqual(res,0)

    def test_get_mins(self):
        min1,min2 = huffman.get_mins(self.table)
        self.table[0][1] = 256
        self.table[2][1] = 256
        self.table[256][0] = 3

        min3,min4 = huffman.get_mins(self.table)

        self.assertEqual((min1,min2,min3,min4),(0,2,256,1))


    def test_make_tree(self):
        #genera arbol y regresa la raiz
        raiz,tree = huffman.make_tree(self.table)
        self.assertEqual(raiz,258)

    def test_codifica(self):
        raiz,tree = huffman.make_tree(self.table)
        cod = huffman.codifica(tree,[5])
        self.assertEqual(cod[0],'0')

    def test_decodifica(self):
        raiz,tree = huffman.make_tree(self.table)
        dec = huffman.decode(tree,['0'])
        self.assertEqual(dec[0],5)

    def test_codifica_data(self):
        table,comp = huffman.codifica_data(self.data)
        self.assertEqual(comp,['111', '011', '011', '01', '01', '01', '0', '0', '0', '0', '0', '0', '0', '0'])

    def test_decodifica_data(self):
        raiz,tree = huffman.make_tree(self.table)
        res = huffman.decodifica_data(tree,['111', '011', '011', '01', '01', '01', '0', '0', '0', '0', '0', '0', '0', '0'])
        self.assertEqual(res,self.data)

    def test_compress(self):
        hist = huffman.make_hist(self.data)
        raiz,tree = huffman.make_tree(hist)
        comp = huffman.compress(tree,self.data)
        self.assertEqual(comp,'11101101101010100000000')

    def test_decode_string(self):
        hist = huffman.make_hist(self.data)
        raiz,tree = huffman.make_tree(hist)
        res = huffman.decode_string(tree,raiz,'11101101101010100000000')
        self.assertEqual(res,self.data)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestHuffman)
    unittest.TextTestRunner(verbosity=2).run(suite)
