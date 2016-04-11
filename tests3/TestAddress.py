'''
Created on Apr 8, 2016

@author: lancer
'''
import unittest
from verify_by_usps import Address 


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


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()