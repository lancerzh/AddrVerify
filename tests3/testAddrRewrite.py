'''
Created on Apr 12, 2016

@author: lancer
'''
import unittest
import verify_by_usps
import addrMatch
import re
'''
Calle 3
Aguadilla, 00603
Puerto Rico
'''
addresses = ["11756 OLIVE STREET RD,,CREVE COEUR,MO,63141", 
             "11756 STREET RD,,CREVE COEUR,MO,63141",
             "11756 OLD OLIVE STREET RD,,CREVE COEUR,MO,63141",
             "11756 OLD OLIVE,,CREVE COEUR,MO,63141"
]
addresses = ["0.3 CARR 110,CEIBA BAJA,AGUADILLA,PR,006030000", 
             "003 CARR 110, CEIBA BAJA,AGUADILLA,PR,006030000", 
             "Calle 3 Aguadilla, CEIBA BAJA, Puerto Rico, PR, 00603"]

addresses = ["1108 City Park Ave,,Columbus, OH, 43206",
             "1108 CITY PARK AVE,FL2,COLUMBUS,OH,43206",
             "999 E MURRAY HOLLADAY RD,SUITE 102,SALT LAKE CITY,UT,841174901"
             ]
addresses = ['2727 W. MARTIN LUTHER KING BLVD.,SUITE 310,TAMPA,FL,33607',
             '2727 W MARTIN LUTHER KING BLVD,,TAMPA,FL,33607',
             "2727 West Drive Martin Luther King Jr Boulevard, Suite 310, Tampa, FL, 33607"]

rwaddresses = [
             ['1800 HARRISON ST FL 7', '', 'OAKLAND', 'CA', '94612'],
             ['1800 HARRISON ST', 'FL 7', 'OAKLAND', 'CA', '94612'],
             ['3495 PIEDMONT RD NE BLDG 9', '', 'ATLANTA', 'GA', '30305', '486'],
             ['3495 PIEDMONT RD NE', 'BLDG 9', 'ATLANTA', 'GA', '30305', '486'],
             ['933 BRADBURY DR SE STE 2222', '', 'ALBUQUERQUE', 'NM', '87106', '413'],
             ['933 BRADBURY DR SE', 'STE 2222', 'ALBUQUERQUE', 'NM', '87106', '413']
]

def displaymatch(match):
    if match is None:
        return None
    return '<Match: %r, groups=%r>' % (match.group(), match.groups())

class Test(unittest.TestCase):
    
    def testAddrWithFirmName(self):
        print('testAddrWithFirmName');
        #1818 ALBION ST,METROPOLITAN NASHVILLE GENERAL HOSPITAL EMERGENCY,NASHVILLE,TN,37208
        a = verify_by_usps.Address('1818 ALBION ST', 'METROPOLITAN NASHVILLE GENERAL HOSPITAL EMERGENCY', 'NASHVILLE', 'TN', '37208')
        v, msg= verify_by_usps.reqUSPS(a);
        self.assertEqual(['1818 ALBION ST', 'METROPOLITAN NASHVILLE GENERAL HOSPITAL EMERGENCY', 'NASHVILLE', 'TN', '37208'], [v.addr1, v.addr2, v.city, v.state, v.zip5])
        
        a = verify_by_usps.Address('METROPOLITAN NASHVILLE GENERAL HOSPITAL EMERGENCY', '1818 ALBION ST', 'NASHVILLE', 'TN', '37208')
        v, msg= verify_by_usps.reqUSPS(a);
        self.assertEqual(['1818 ALBION ST', 'METROPOLITAN NASHVILLE GENERAL HOSPITAL EMERGENCY', 'NASHVILLE', 'TN', '37208'], [v.addr1, v.addr2, v.city, v.state, v.zip5])
        
        a = verify_by_usps.Address('1818 ALBION ST', '', 'NASHVILLE', 'TN', '37208')
        v, msg= verify_by_usps.reqUSPS(a);
        self.assertEqual(['1818 ALBION ST', '', 'NASHVILLE', 'TN', '37208'], [v.addr1, v.addr2, v.city, v.state, v.zip5])
    
        a = verify_by_usps.Address('', '1818 ALBION ST', 'NASHVILLE', 'TN', '37208')
        v, msg= verify_by_usps.reqUSPS(a);
        self.assertEqual(['1818 ALBION ST', '', 'NASHVILLE', 'TN', '37208'], [v.addr1, v.addr2, v.city, v.state, v.zip5])
    
        a = verify_by_usps.Address('METROPOLITAN NASHVILLE GENERAL HOSPITAL EMERGENCY', '', 'NASHVILLE', 'TN', '37208')
        v, msg= verify_by_usps.reqUSPS(a);
        self.assertIsNone(v)
    
        a = verify_by_usps.Address('', 'METROPOLITAN NASHVILLE GENERAL HOSPITAL EMERGENCY', 'NASHVILLE', 'TN', '37208')
        v, msg= verify_by_usps.reqUSPS(a);
        self.assertIsNone(v)
        
    def testRewriteAddrInfluenceUSPS(self):
        print('testRewriteAddrInfluenceUSPS');
        a = verify_by_usps.Address('1800 HARRISON ST FL 7', '', 'OAKLAND', 'CA', '94612')
        v, msg= verify_by_usps.reqUSPS(a);
        self.assertEqual(['1800 HARRISON ST FL 7', '', 'OAKLAND', 'CA', '94612'], [v.addr1, v.addr2, v.city, v.state, v.zip5])
        a = verify_by_usps.Address('1800 HARRISON ST', 'FL 7', 'OAKLAND', 'CA', '94612')
        v, msg= verify_by_usps.reqUSPS(a);
        self.assertEqual(['1800 HARRISON ST FL 7', '', 'OAKLAND', 'CA', '94612'], [v.addr1, v.addr2, v.city, v.state, v.zip5])
        
        a = verify_by_usps.Address('3495 PIEDMONT RD NE BLDG 9', '', 'ATLANTA', 'GA', '30305')
        v, msg= verify_by_usps.reqUSPS(a);
        print(msg)
        self.assertEqual(['3495 PIEDMONT RD NE', 'BLDG 9', 'ATLANTA', 'GA', '30305'], [v.addr1, v.addr2, v.city, v.state, v.zip5])
        a = verify_by_usps.Address('3495 PIEDMONT RD NE', 'BLDG 9', 'ATLANTA', 'GA', '30305')
        v, msg= verify_by_usps.reqUSPS(a);
        print(msg)
        self.assertEqual(['3495 PIEDMONT RD NE', 'BLDG 9', 'ATLANTA', 'GA', '30305'], [v.addr1, v.addr2, v.city, v.state, v.zip5])
        
        a = verify_by_usps.Address('933 BRADBURY DR SE STE 2222', '', 'ALBUQUERQUE', 'NM', '87106')
        v, msg= verify_by_usps.reqUSPS(a);
        print(msg)
        self.assertEqual(['933 BRADBURY DR SE', 'STE 2222', 'ALBUQUERQUE', 'NM', '87106'], [v.addr1, v.addr2, v.city, v.state, v.zip5])
        a = verify_by_usps.Address('933 BRADBURY DR SE', 'STE 2222', 'ALBUQUERQUE', 'NM', '87106')
        v, msg= verify_by_usps.reqUSPS(a);
        print(msg)
        self.assertEqual(['933 BRADBURY DR SE', 'STE 2222', 'ALBUQUERQUE', 'NM', '87106'], [v.addr1, v.addr2, v.city, v.state, v.zip5])
        a = verify_by_usps.Address('STE 2222, 933 BRADBURY DR SE', '', 'ALBUQUERQUE', 'NM', '87106')
        v, msg= verify_by_usps.reqUSPS(a);
        print(msg)
        self.assertIsNone(v)

    def testAddress(self):
        print('testAddress');
        for a in addresses:
            al = a.split(',')
            addr = verify_by_usps.Address(al[0],al[1],al[2],al[3],al[4])
            print(addr)
            va, msg= verify_by_usps.reqUSPS(addr);
            
            print (va)
            print (msg)
            #self.assertIsNotNone(va)
            
    def testSplitAlphaNum(self):
        print('testSplitAlphaNum');
        self.assertEqual('1ST', addrMatch.splitAlphaNumStr("1ST"))
        m = re.compile(r"^([A-Z]*)([0-9]+)([A-Z]*)$")

        print(displaymatch(m.match('STE1000')));
        print (re.match(r"^[A-Z]+$", 'STE').group(0))
        self.assertEqual('STE 1000', addrMatch.splitAlphaNumStr('STE1000'))

    def testReplacePunctuation(self):
        addr = verify_by_usps.Address('500 OLD YORK ROAD','SUITE #108','JENKINTOWN','PA','19046')
        newaddr = addrMatch.replaceunctuation(addr);
        self.assertEqual('500 OLD YORK ROAD', newaddr.addr1)
        self.assertEqual('SUITE  108', newaddr.addr2)
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test1']
    unittest.main()