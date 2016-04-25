'''
Created on Apr 25, 2016

@author: lancer
'''
import unittest
import verify_by_usps;
from USMailAddress import Address 


class Test(unittest.TestCase):
    """
'-2147219396', '397'
'-2147219399', '1166'
'-2147219400', '417'
'-2147219401', '213868'
'-2147219402', '1284'
'-2147219403', '16087'
'-2147221202', '71'
'80040B18', '230'
'80040B19', '16868'
'T', '45'
'V', '6483502'

"""

    """ otn:
'AG', '1'
'AI', '1'
'AQ', '1'
'AZ', '1'
'BB', '1'
'BT', '1'
'CC', '1'
'CD', '1'
'DZ', '1'
'FI', '1'
'GD', '1'
'GM', '1'
'GN', '1'
'LA', '1'
'LS', '1'
'LU', '1'
'LV', '1'
'MG', '1'
'MO', '1'
'MS', '1'
'NE', '1'
'PL', '1'
'SC', '1'
'SD', '1'
'SV', '1'
'TM', '1'
'UZ', '1'
'VC', '1'
'VU', '1'
'AM', '2'
'BD', '2'
'BG', '2'
'BO', '2'
'CY', '2'
'CZ', '2'
'GA', '2'
'GG', '2'
'GH', '2'
'GY', '2'
'HT', '2'
'IR', '2'
'JE', '2'
'LY', '2'
'MT', '2'
'MW', '2'
'NA', '2'
'OM', '2'
'RU', '2'
'RW', '2'
'SH', '2'
'TT', '2'
'UY', '2'
'VN', '2'
'ZM', '2'
'AL', '3'
'AN', '3'
'CM', '3'
'CR', '3'
'DK', '3'
'HK', '3'
'HN', '3'
'HU', '3'
'ID', '3'
'IO', '3'
'KH', '3'
'MA', '3'
'MY', '3'
'UA', '3'
'CL', '4'
'CS', '4'
'DM', '4'
'GE', '4'
'SE', '4'
'AT', '5'
'ET', '5'
'GT', '5'
'KW', '5'
'NP', '5'
'PG', '5'
'RO', '5'
'EC', '6'
'KE', '6'
'BM', '7'
'BS', '7'
'JM', '7'
'KP', '7'
'NO', '7'
'ZA', '7'
'AF', '8'
'JO', '8'
'NG', '8'
'PE', '8'
'VG', '8'
'AR', '9'
'EG', '9'
'UG', '9'
'VE', '9'
'IS', '10'
'PT', '10'
'KY', '11'
'PA', '11'
'CO', '12'
'IQ', '12'
'AX', '13'
'FR', '13'
'NL', '13'
'QA', '13'
'CH', '14'
'CU', '15'
'SG', '15'
'LB', '16'
'BH', '17'
'BR', '17'
'GR', '18'
'BE', '19'
'DO', '20'
'TW', '20'
'CN', '21'
'NZ', '21'
'TH', '26'
'AE', '35'
'TR', '37'
'ES', '40'
'AU', '41'
'PK', '41'
'IE', '50'
'PH', '62'
'SA', '63'
'IL', '93'
'IN', '103'
'IT', '204'
'GB', '213'
'KR', '276'
'MX', '390'
'JP', '418'
'DE', '998'
'CA', '1007'
'UM', '1729'
'US', '6727472'

    """

    ''''''
    def test2147219396(self):
        print("test2147219396");
        addr = Address('1 MEDICAL CENTER BLVD', 'POB I, SUITE 407', 'CHESTER', 'PA', '19013');
        result, msg = verify_by_usps.reqUSPS (addr);
        print (result)
        print(msg)
        self.assertEqual('-2147219396', msg[0])
        self.assertEqual('Invalid Address.  ', msg[1])


    def test2147219399(self):
        print("test2147219399");
        addr = Address('CONTRA CORNOLEO 11', '', 'VICENZA', 'VICENZA', '36100');
        result, msg = verify_by_usps.reqUSPS (addr);
        print (result)
        print(msg)
        self.assertEqual('-2147219399', msg[0])
        self.assertEqual('Invalid Zip Code.  ', msg[1])
            
        addr = Address('VIA VINCENZO DI MARCO #29', '', 'PALERMO', 'PA', '90143');
        result, msg = verify_by_usps.reqUSPS (addr);
        print (result)
        print(msg)
        self.assertEqual('-2147219399', msg[0])
        self.assertEqual('Invalid Zip Code.  ', msg[1])
    
        
    def test2147219400(self):
        print("test2147219400");
        addr = Address('131-1 KAMEYACHO KOJINGUCHIDORI, VANTARISE 1-E', 'KAMIGYOKU', 'KYOTO', 'KYOTO', '60208');
        result, msg = verify_by_usps.reqUSPS (addr);
        print (result)
        print(msg)
        self.assertEqual('-2147219400', msg[0])
        self.assertEqual('Invalid City.  ', msg[1])
        
        addr = Address('100 N ACADEMY AVE', '', 'PENNSYLVANIA', 'PA', '17822');
        result, msg = verify_by_usps.reqUSPS (addr);
        print (result)
        print(msg)
        self.assertEqual('-2147219400', msg[0])
        self.assertEqual('Invalid City.  ', msg[1])

    def test2147219401(self):
        print("test2147219401");
        addr = Address('113 HILLCREST DRE', '', 'SANFORD', 'NC', '27330');
        result, msg = verify_by_usps.reqUSPS (addr);
        print (result)
        print(msg)
        self.assertEqual('-2147219401', msg[0])
        self.assertEqual('Address Not Found.  ', msg[1])
        
    def test2147219402(self):
        print("test2147219402");
        addr = Address('872 RED OAK AVE', '', 'LONDON', 'ONTARIO', 'N6H 5');
        result, msg = verify_by_usps.reqUSPS (addr);
        print (result)
        print(msg)
        self.assertEqual('-2147219402', msg[0])
        self.assertEqual('Invalid State Code.  ', msg[1])
        
        addr = Address('HHC 121ST GENERAL HOSPITAL', 'BOX 675', 'APO', 'KOREA', 'AP000');
        result, msg = verify_by_usps.reqUSPS (addr);
        print (result)
        print(msg)
        self.assertEqual('-2147219402', msg[0])
        self.assertEqual('Invalid State Code.  ', msg[1])

        
    def test2147219403(self):
        print("test2147219403");
        addr = Address('CARR. 21 S3 LAS LOMAS BO. MONACILLOS', 'OFFICE # 2', 'SAN JUAN', 'PR', '00956');
        result, msg = verify_by_usps.reqUSPS (addr);
        print (result)
        print(msg)
        self.assertEqual('-2147219403', msg[0])
        self.assertEqual('Multiple addresses were found for the information you entered, and no default exists.', msg[1])
        
        addr = Address('1218 SOUTH OLIVE AVE.', '', 'WEST PALM BEACH', 'FL', '33401');
        result, msg = verify_by_usps.reqUSPS (addr);
        print (result)
        print(msg)
        self.assertEqual('-2147219403', msg[0])
        self.assertEqual('Multiple addresses were found for the information you entered, and no default exists.', msg[1])
        
        addr = Address('1218 S OLIVE AVE.', '', 'WEST PALM BEACH', 'FL', '33401');
        result, msg = verify_by_usps.reqUSPS (addr);
        print (result)
        print(msg)
        self.assertEqual('-2147219403', msg[0])
        self.assertEqual('Multiple addresses were found for the information you entered, and no default exists.', msg[1])
        
        addr = Address('25 N. WINFIELD RD.', '', 'WINFIELD', 'IL', '60190');
        result, msg = verify_by_usps.reqUSPS (addr);
        print (result)
        print(msg)
        self.assertEqual('-2147219403', msg[0])
        self.assertEqual('Multiple addresses were found for the information you entered, and no default exists.', msg[1])
        
        addr = Address('25 WINFIELD RD.', '', 'WINFIELD', 'IL', '60190');
        result, msg = verify_by_usps.reqUSPS (addr);
        print (result)
        print(msg)
        self.assertEqual('-2147219403', msg[0])
        self.assertEqual('Multiple addresses were found for the information you entered, and no default exists.', msg[1])
                
    def test2147221202(self):
        print("test2147221202");
        addr = Address('UPC CHILDREN&APOS;S HOSPITAL', '3901 BEAUBIEN 4TH FLOOR CARLS BLDG', 'DETROIT', 'MI', '48201');
        result, msg = verify_by_usps.reqUSPS (addr);
        print (result)
        print(msg)
        self.assertEqual('-2147221202', msg[0])
        self.assertEqual("Reference to undeclared entity 'APOS'. Line 6, position 28.", msg[1])
        
        addr = Address('UPC CHILDREN APOS HOSPITAL', '3901 BEAUBIEN 4TH FLOOR CARLS BLDG', 'DETROIT', 'MI', '48201');
        result, msg = verify_by_usps.reqUSPS (addr);
        print (result)
        print(msg)
        self.assertEqual('-2147219401', msg[0])
        self.assertEqual("Address Not Found.  ", msg[1])
        
    def test80040B18(self):
        print("test80040B18");
        addr = Address('112 N 7TH ST', 'CHAMBERSBURG HOSPITAL-PHYSICAL MEDICINE DEPARTMENT', 'CHAMBERSBURG', 'PA', '17201');
        result, msg = verify_by_usps.reqUSPS (addr);
        print (result)
        print(msg)
        #self.assertEqual('-80040B18', msg[0])
        #self.assertEqual('????', msg[1])
        
    def test80040B19(self):
        print("test80040B19");
        addr = Address('US HWY 160 & NAVAJO ROUTE 25 - RED MESA', '', 'TEECNOSPOS', 'AZ', '86514');
        result, msg = verify_by_usps.reqUSPS (addr);
        print (result)
        print(msg)
        self.assertEqual('80040B19', msg[0])
        self.assertEqual("XML Syntax Error: Please check the XML request to see if it can be parsed.", msg[1])
        
        addr = Address('US HWY 160 and NAVAJO ROUTE 25 - RED MESA', '', 'TEECNOSPOS', 'AZ', '86514');
        result, msg = verify_by_usps.reqUSPS (addr);
        print (result)
        print(msg)

    
    def testT(self):
        print("testT");
        addr = Address('1014 NE 7TH ST', '', 'GRANTS PASS', 'OR', '97526');
        result, msg = verify_by_usps.reqUSPS (addr);
        print (result)
        print(msg)
            
    def testF(self):
        print("testF");
        addr = Address('680 S WILTON PL', '', 'LOS ANGELES', 'CA', '90005');
        result, msg = verify_by_usps.reqUSPS (addr);
        print (result)
        print(msg)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()