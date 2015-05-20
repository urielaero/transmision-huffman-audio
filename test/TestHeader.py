import unittest
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from main import header

class TestHeader(unittest.TestCase):
    pass

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestHeader)
    unittest.TextTestRunner(verbosity=2).run(suite)
