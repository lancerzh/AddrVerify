'''
Created on Apr 8, 2016

@author: lancer
'''
import unittest
from USMailAddress import Address , Distance


class Test(unittest.TestCase):


    def testEq(self):
        self.assertEqual('a', 'a')
        self.assertNotEqual('a', 'b')
        a1 = Address('a', 'b', 'c', 's', 'z', 'n')
        a2 = Address('a', 'b', 'c', 's', 'z', 'n')
        a3 = Address('b', 'a', 'c', 's', 'z', 'n')
        a4 = Address('c', 'a', 'c', 's', 'z', 'n')
        self.assertEqual(a1, a2)
        self.assertEqual(a1, a3)
        self.assertEqual(a2, a3)
        self.assertNotEqual(a1, a4)
        self.assertNotEqual(Address('a', 'b', 'c1', 's', 'z', 'n'), Address('a', 'b', 'c', 's', 'z', 'n'))
        self.assertNotEqual(Address('a', 'b', 'c', 's1', 'z', 'n'), Address('a', 'b', 'c', 's', 'z', 'n'))
        self.assertNotEqual(Address('a', 'b', 'c', 's', 'z1', 'n'), Address('a', 'b', 'c', 's', 'z', 'n'))
        self.assertNotEqual(Address('a', 'b', 'c', 's', 'z', 'n1'), Address('a', 'b', 'c', 's', 'z', 'n'))
        self.assertNotEqual(Address('a', 'b', 'c1', 's', 'z', 'n'), Address('a', 'b', 'c', 's', 'z'))
        self.assertNotEqual(Address('a', 'b', 'c', 's', 'z', 'n'), 'a')
        self.assertNotEqual(Address('a', 'b', 'c', 's', 'z', 'n'), None)
        self.assertNotEqual(None, Address('a', 'b', 'c', 's', 'z', 'n'))
        pass

    def testDistance(self):
        a1 = Address('a', 'b', 'c', 's', 'z', 'n')
        a2 = Address('a', 'b', 'c', 's', 'z', 'n')
        dist = Distance(a1, a2)
        self.assertTrue(dist.isMatched())
        
        a1 = Address('7500 SMOKE RANCH RD STE 200','','LASVEGAS','NV','891280000')
        a2 = Address('500 SMOKE RANCH RD','STE 200','LAS VEGAS','NV','89128,0373')
        dist = Distance(a1, a2)
        print (dist.detail())
        self.assertTrue(dist.isMatched())

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()