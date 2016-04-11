'''
Created on Apr 6, 2016

@author: lancer
'''
import unittest
from analysisWordFreq import isdoorplate, procPOBOX;
import re;


class Test(unittest.TestCase):
    
    def testStrReplace(self):
        self.assertEqual('12345987', re.sub(r"[^\w\s]", '', '123#45-987'))


    def testIsDoorPlate(self):
        self.assertTrue(isdoorplate('12345'));
        self.assertTrue(isdoorplate('12345-987'));
        self.assertTrue(isdoorplate('123#45-987'));
        self.assertTrue(isdoorplate('12345A'));
        self.assertTrue(isdoorplate('A12345'));
        self.assertTrue(isdoorplate('A-12345'));
        self.assertTrue(isdoorplate('#12345'));
        self.assertFalse(isdoorplate('A'));
        self.assertFalse(isdoorplate('AB12345'));
        self.assertFalse(isdoorplate('A12345B'));
        pass
    
    def testMatch(self):
        r2 = r"(.*) P[. ]*O[. ]*BOX[.]?\s?(.*)$";
        self.assertTrue(re.match(r2, 'SUITE 201 PO BOX 11'));
        self.assertTrue(re.match(r2, 'SUITE 201, PO BOX 11'));
        

    
    def testProcPOBOX(self):
        standardStr = 'PO BOX 2';
        self.assertEqual(standardStr, procPOBOX('PO BOX 2'))
        self.assertEqual(standardStr, procPOBOX('P.O. BOX 2'))
        self.assertEqual(standardStr, procPOBOX('PO. BOX. 2'))
        self.assertEqual(standardStr, procPOBOX('P. O. BOX 2'))
        self.assertEqual(standardStr, procPOBOX('P.O.BOX. 2'))
        
        standardStr = '1 PO BOX 2';
        self.assertEqual(standardStr, procPOBOX('1 PO BOX 2'))
        self.assertEqual(standardStr, procPOBOX('1 P.O. BOX 2'))
        self.assertEqual(standardStr, procPOBOX('1 PO. BOX. 2'))
        self.assertEqual(standardStr, procPOBOX('1 P. O. BOX 2'))
        self.assertEqual(standardStr, procPOBOX('1 P.O.BOX. 2'))
        # warning:
        self.assertEqual('1 DUP O BOX 2', procPOBOX('1 DUP O BOX 2'))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testIsDoorPlate']
    unittest.main()