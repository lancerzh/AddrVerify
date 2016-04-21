'''
Created on Apr 20, 2016

@author: lancer
'''
import unittest
from fuzzywuzzy import fuzz
from USMailAddress import Address, Distance

class Test(unittest.TestCase):


    def testFuzzy(self):
        print('ratio', fuzz.ratio('MISSION HOSPITAL', 'MISSION HOSPITAL REGIONAL MEDICAL CENTER'))
        print('ratio', fuzz.ratio('MISSION HOSPITAL REGIONAL MEDICAL CENTER', 'MISSION HOSPITAL'))
        
        print('partial_ratio', fuzz.partial_ratio('MISSION HOSPITAL', 'MISSION HOSPITAL REGIONAL MEDICAL CENTER'))
        print('partial_ratio', fuzz.partial_ratio('MISSION HOSPITAL REGIONAL MEDICAL CENTER','MISSION HOSPITAL'))
        
        print('token_sort_ratio', fuzz.token_sort_ratio('MISSION HOSPITAL', 'MISSION HOSPITAL REGIONAL MEDICAL CENTER'))
        print('token_sort_ratio', fuzz.token_sort_ratio('MISSION HOSPITAL REGIONAL MEDICAL CENTER', 'MISSION HOSPITAL'))
        
        print('partial_token_sort_ratio', fuzz.partial_token_sort_ratio('MISSION HOSPITAL', 'MISSION HOSPITAL REGIONAL MEDICAL CENTER'))
        print('partial_token_sort_ratio', fuzz.partial_token_sort_ratio('MISSION HOSPITAL REGIONAL MEDICAL CENTER', 'MISSION HOSPITAL', ))
        
        print('token_set_ratio', fuzz.token_set_ratio('MISSION HOSPITAL', 'MISSION HOSPITAL REGIONAL MEDICAL CENTER'))
        print('token_set_ratio', fuzz.token_set_ratio('MISSION HOSPITAL REGIONAL MEDICAL CENTER', 'MISSION HOSPITAL'))
        
        print('partial_token_set_ratio', fuzz.partial_token_set_ratio('MISSION HOSPITAL', 'MISSION HOSPITAL REGIONAL MEDICAL CENTER'))
        print('partial_token_set_ratio', fuzz.partial_token_set_ratio('MISSION HOSPITAL REGIONAL MEDICAL CENTER', 'MISSION HOSPITAL', ))
        
        print('QRatio', fuzz.QRatio('MISSION HOSPITAL', 'MISSION HOSPITAL REGIONAL MEDICAL CENTER'))
        print('QRatio', fuzz.QRatio('MISSION HOSPITAL REGIONAL MEDICAL CENTER', 'MISSION HOSPITAL'))
        
        print('UQRatio', fuzz.UQRatio('MISSION HOSPITAL', 'MISSION HOSPITAL REGIONAL MEDICAL CENTER'))
        print('UQRatio', fuzz.UQRatio('MISSION HOSPITAL REGIONAL MEDICAL CENTER', 'MISSION HOSPITAL'))
        
        print('WRatio', fuzz.WRatio('MISSION HOSPITAL', 'MISSION HOSPITAL REGIONAL MEDICAL CENTER'))
        print('WRatio', fuzz.WRatio('MISSION HOSPITAL REGIONAL MEDICAL CENTER', 'MISSION HOSPITAL', ))
        
        print('UWRatio', fuzz.UWRatio('MISSION HOSPITAL', 'MISSION HOSPITAL REGIONAL MEDICAL CENTER'))
        print('UWRatio', fuzz.UWRatio('MISSION HOSPITAL REGIONAL MEDICAL CENTER', 'MISSION HOSPITAL'))
        
        pass

    def testAddrDistance(self):
        a1 = Address('90 MEMORIAL DR','','PINEHURST','NC','28374')
        a2 = Address('205 PAGE RD','','PINEHURST','NC','28374')
        print (Distance(a1, a2).detail())

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testFuzzy']
    unittest.main()