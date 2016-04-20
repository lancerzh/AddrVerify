'''
Created on Apr 8, 2016

@author: lancer
'''
import unittest
from USMailAddress import Address , Distance, stripPOBox


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
        print ('testDistance')
        a1 = Address('a', 'b', 'c', 's', 'z', 'n')
        a2 = Address('a', 'b', 'c', 's', 'z', 'n')
        dist = Distance(a1, a2)
        self.assertTrue(dist.isMatched())
        
        a1 = Address('7500 SMOKE RANCH RD STE 200','','LASVEGAS','NV','891280000')
        a2 = Address('500 SMOKE RANCH RD','STE 200','LAS VEGAS','NV','89128,0373')
        dist = Distance(a1, a2)
        print (dist.detail())
        self.assertTrue(dist.isMatched())
        
    def testPOBOXDistance(self):
        print ('testPOBOXDistance')
        a1 = Address('PO BOX 12345', '', 'c', 's', 'z', 'n')
        self.assertTrue(a1.isPOBox())
        a2 = Address('PO BOX 67890', '', 'c', 's', 'z', 'n')
        self.assertTrue(a1.isPOBox())
        dist = Distance(a1, a2)
        print (dist.detail())
        
        a1 = Address('PO BOX 12345', '', 'c', 's', 'z', 'n')
        self.assertTrue(a1.isPOBox())
        a2 = Address('PO BOX 92345', '', 'c', 's', 'z', 'n')
        self.assertTrue(a1.isPOBox())
        dist = Distance(a1, a2)
        print (dist.detail())
        
    def testStripPOBox(self):
        self.assertEqual('12345', stripPOBox('PO BOX 12345'))
        self.assertEqual('67890', stripPOBox('PO BOX 67890'))
        
    def testAddrToKeyStr(self):
        print ('testAddrToKeyStr')
        a1 = Address('PO BOX 12345', 'l2', 'c', 's', 'z', 'n')
        self.assertEqual('12345 BOX C L2 PO S Z0000', a1.tokeystr())
        self.assertEqual('0000 12345 BOX C L2 PO S Z0000', a1.tokeystr(usezip4=True))
        
        a1 = Address('PO BOX 12345', 'l&2', 'c', 's', 'z', 'n')
        self.assertEqual('12345 2 BOX C L PO S Z0000', a1.tokeystr())
        self.assertEqual('0000 12345 2 BOX C L PO S Z0000', a1.tokeystr(usezip4=True))
    
    def testAddrDistance(self):
        print ('testAddrDistance')
        a1 = Address('488 SAINT LUKES DR','','MONTGOMERY','AL','361170000')
        a2 = Address('488 SAINT LUKES DR','','MONTGOMERY','AL','361177104');
        print (Distance(a1, a2).detail())
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()