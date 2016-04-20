'''
Created on Mar 22, 2016

@author: lancer
'''
import unittest
import verify_by_usps;
from xml.dom.minidom import parseString
import string



testFile='';


class Test(unittest.TestCase):

    def testPunctuation(self):
        self.assertEqual(len(string.punctuation), len(' ' * len(string.punctuation)));
        alist = []
        self.assertEqual(0, len(alist));
        alist.append('a')
        self.assertEqual(1, len(alist));
        alist.append(['a'])
        self.assertEqual(2, len(alist));
        alist = alist + ['a', 'b']
        self.assertEqual(4, len(alist));

    def testAddressZip(self):
        addr1 = verify_by_usps.Address('', '', '', '', '123456789');
        self.assertEqual('12345', addr1.zip5)
        self.assertEqual('6789', addr1.zip4)
        addr1 = verify_by_usps.Address('', '', '', '', '12345-6789 ');
        self.assertEqual('12345', addr1.zip5)
        self.assertEqual('6789', addr1.zip4)
        addr1 = verify_by_usps.Address('', '', '', '', '12345');
        self.assertEqual('12345', addr1.zip5)
        self.assertEqual('0000', addr1.zip4)
        addr1 = verify_by_usps.Address('', '', '', '', '1234567');
        self.assertEqual('12345', addr1.zip5)
        self.assertEqual('6700', addr1.zip4)
        addr1 = verify_by_usps.Address('', '', '', '', '12');
        self.assertEqual('12000', addr1.zip5)
        self.assertEqual('0000', addr1.zip4)
        pass
    
    def testList(self):
        indexs = (21, 22, 23, 24, 25);
        self.assertEqual(21, indexs[0]);
        self.assertEqual(2, len('"\"'))
        
    def testXmlRead(self):
        xmlTemplete = '''<?xml version="1.0" ?>
<AddressValidateRequest USERID="953JMS002790">
  <IncludeOptionalElements>true</IncludeOptionalElements>
  <ReturnCarrierRoute>true</ReturnCarrierRoute>
  <Address ID="0">  
    <FirmName />
    <Address2>Newbury PI</Address2>   
    <City>TROY</City>   
    <State>MI</State>   
    <Zip5>00000</Zip5>   
    <Zip4/>
  </Address>     
</AddressValidateRequest>
''';
        dom = parseString(xmlTemplete);
        print(dom.toprettyxml()) 
        
        a1 = dom.getElementsByTagName('Address1');
        self.assertEqual(0, a1.length)
        
        z5 = dom.getElementsByTagName('Zip5');
        self.assertEqual(1, z5.length)
        self.assertEqual('00000', z5[0].firstChild.nodeValue)
         
        z4 = dom.getElementsByTagName('Zip4');
        self.assertEqual(1, z4.length)
        self.assertEqual(0, z4[0].childNodes.length)

        self.assertEqual('00000', verify_by_usps.getText(dom, 'Zip5'));
        self.assertEqual(None, verify_by_usps.getText(dom, 'Zip4'));
        self.assertEqual(None, verify_by_usps.getText(dom, 'Address1'));

    def testSort(self):
        l = []
        l.append(('1', (100, 90, 'PrimaryName')));
        l.append(('2', (90, 100, 'PrimaryName')));
        
        sorted_list = sorted(l, key=lambda x:x[1][1], reverse=True)
        for item in sorted_list:
            print(item)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testAv1']
    unittest.main()