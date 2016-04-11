'''
Created on Apr 5, 2016

@author: lancer
'''
import unittest
import verify_by_usps;

class Test(unittest.TestCase):
    
    def testIndex(self):
        a = ['P','P','-','S','P']
        
    def test1P1S(self):
        lexical = verify_by_usps.AddressLexical("6400 FANNIN ST STE 3000");
        self.assertEqual(['STE 3000'], lexical.secondary)
        self.assertEqual(['6400 FANNIN ST'], lexical.primary)
        
        lexical = verify_by_usps.AddressLexical("DEPT 3333, 6400 FANNIN ST STE 3000");
        self.assertEqual(['DEPT 3333,', 'STE 3000'], lexical.secondary)
        self.assertEqual(['6400 FANNIN ST'], lexical.primary)
        
        lexical = verify_by_usps.AddressLexical("6400 FANNIN STE 3000");
        self.assertEqual(['STE 3000'], lexical.secondary)
        self.assertEqual(['6400 FANNIN'], lexical.primary)
    
    def test1P1SA(self):
        lexical = verify_by_usps.AddressLexical("6400 FANNIN DEPT 3333, STE 3000");
        self.assertEqual(['DEPT 3333, STE 3000'], lexical.secondary)
        self.assertEqual(['6400 FANNIN'], lexical.primary)
    
    def test1P1SB(self):
        lexical = verify_by_usps.AddressLexical("6400 FANNIN ST DEPT 3333, STE 3000");
        self.assertEqual(['DEPT 3333, STE 3000'], lexical.secondary)
        self.assertEqual(['6400 FANNIN ST'], lexical.primary)

    def test1P1SC(self):
        lexical = verify_by_usps.AddressLexical("DEPT. 52365, PO BOX 950111");
        self.assertEqual(['DEPT. 52365,'], lexical.secondary)
        self.assertEqual(['PO BOX 950111'], lexical.primary)
        pass
    
    def test1P1N(self):
        lexical = verify_by_usps.AddressLexical("601 SOUTH FLOYD STREET #503");
        self.assertEqual([('#503')], lexical.secondary)
        self.assertEqual(['601 SOUTH FLOYD STREET'], lexical.primary)
        
        lexical = verify_by_usps.AddressLexical("601 SOUTH FLOYD STREET MY #503");
        self.assertEqual([('MY #503')], lexical.secondary)
        self.assertEqual(['601 SOUTH FLOYD STREET'], lexical.primary)
        
        pass
    
    def testReplace(self):
        lexical = verify_by_usps.AddressLexical("6400 FANNIN STREET SUITE 3000");
        self.assertEqual(['SUITE 3000'], lexical.secondary)
        self.assertEqual(['6400 FANNIN STREET'], lexical.primary)
        lexical.replaceAbbr()
        self.assertEqual('STE 3000', lexical.addr2)
        self.assertEqual('6400 FANNIN ST', lexical.addr1)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()