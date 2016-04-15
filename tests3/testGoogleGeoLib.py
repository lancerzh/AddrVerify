'''
Created on Apr 13, 2016

@author: lancer
'''
import unittest
import string
import verify_by_google
from USMailAddress import Address, calcDistance

addresses = ['207 SOUTH PRINCESS STREET,,SHEPHERDSTOWN,WV,25443,0000',
'USAF ACADEMY,,COLORADO SPRINGS,CO,80920,0000',
'142 COTTAGE ST,1R,PAWTUCKET,RI,02860,3007',
'CALLE DR. RAMON EMETERIO BETANCES #60N POST CENTER,SUITE 207,MAYAGUEZ,PR,00680,0000',
'POST 60-N POST CENTER,SUITE 207,MAYAGUEZ,PR,00680,0000'
]

class Test(unittest.TestCase):
    
    def testReturnFirmName(self):
        print('testReturnFirmName')
        addr = Address('DEPT 52519 PO BOX 950123','','LOUISVILLE','KY','402950000');
        print (addr);
        aa, msg, alt = verify_by_google.reqGoogle(addr);
        for ga in alt:
            print (ga);
            print(calcDistance(addr, ga))

    def testName(self):
        for a in addresses :
            print()
            ws = a.split(',');
            addr = Address(ws[0],ws[1],ws[2],ws[3],ws[4]);
            print (addr)
            aa, msg, alt = verify_by_google.reqGoogle(addr);
            for ga in alt:
                print (ga);
                print(calcDistance(addr, ga))
        pass

    def testTrans(self):
        self.assertEqual('++++++', '+' * 6)
        self.assertEqual('CALLE+DR+RAMON+EMETERIO+BETANCES+60N+POST+CENTER',verify_by_google.replacePunctuationWithPlus('CALLE DR. RAMON EMETERIO BETANCES #60N POST CENTER'));

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()