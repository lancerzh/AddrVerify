'''
Created on Mar 22, 2016

@author: lancer
'''

import http.client;
import urllib.request, urllib.parse, urllib.error;
import csv;
import time;
from xml.dom.minidom import parseString

class Address:
    addr1 = '';
    addr2 = '';
    city = '';
    state = '';
    zip5 = '';
    zip4 = '';
    def __init__(self, a1, a2, c, s, z):
        self.addr1 = a1;
        self.addr2 = a2;
        self.city = c;
        self.state = s;
        self.zip5 = z;
        self.zip4 = z;
        
    def __str__(self) :
        return ','.join((self.addr1, self.addr2, self.city, self.state, self.zip5, self.zip4));

urlString = '/ShippingAPI.dll?API=Verify&XML=';
xmlString = '''
<AddressValidateRequest USERID="953JMS002790">
  <IncludeOptionalElements>true</IncludeOptionalElements>
  <ReturnCarrierRoute>true</ReturnCarrierRoute>
  <Address ID="0">  
    <FirmName />   
    <Address1 />   
    <Address2>205 bagwell ave</Address2>   
    <City>nutter fort</City>   
    <State>wv</State>   
    <Zip5></Zip5>   
    <Zip4></Zip4> 
  </Address>     
    <Address ID="1">  
    <FirmName />   
    <Address1 />   
    <Address2>216 bagwell ave</Address2>   
    <City>nutter fort</City>   
    <State>wv</State>   
    <Zip5></Zip5>   
    <Zip4></Zip4> 
  </Address>  
</AddressValidateRequest>
''';

xmlTemplete = '''
<AddressValidateRequest USERID="953JMS002790">
  <IncludeOptionalElements>true</IncludeOptionalElements>
  <ReturnCarrierRoute>true</ReturnCarrierRoute>
  <Address ID="0">  
    <FirmName />   
    <Address1>@@ADDRESS1@@</Address1>
    <Address2>@@ADDRESS2@@</Address2>   
    <City>@@CITY@@</City>   
    <State>@@STATE@@</State>   
    <Zip5>@@ZIP5@@</Zip5>   
    <Zip4></Zip4> 
  </Address>     
</AddressValidateRequest>
''';

xmlString1='<AddressValidateRequest%20USERID="953JMS002790">%20<IncludeOptionalElements>true</IncludeOptionalElements>%20<ReturnCarrierRoute>true</ReturnCarrierRoute>%20<Address%20ID="0">%20<FirmName%20/>%20<Address1%20/>%20<Address2>205%20bagwell</Address2>%20<City>nutter%20fort</City>%20<State>wv</State>%20<Zip5></Zip5>%20<Zip4></Zip4>%20</Address>%20</AddressValidateRequest>';

def reqUSPS(xmlReqStr):
    qs = urlString + urllib.parse.quote(xmlReqStr);

    conn = http.client.HTTPConnection("production.shippingapis.com")
    conn.request("GET", qs)
    r1 = conn.getresponse()
    print(r1.status, r1.reason)

    result = r1.read()
    conn.close()
    if  '<Error>' in result:
        return result;
    dom = parseString(result);
    print(dom.toprettyxml());
    a = dom.getElementsByTagName('Address');
    print(a[0].toprettyxml());
    
    a1 = a[0].getElementsByTagName('Address1');
    if len(a1) > 0:
        print(a1[0].toprettyxml());
        a1 = a1[0].childNodes[0].data;
        print(a1)
        
    a2 = a[0].getElementsByTagName('Address2');
    if len(a2) > 0:
        print(a2[0].toprettyxml());
        a2 = a2[0].childNodes[0].data
        print(a2)
    return result;
#reqUSPS(xmlString);

def buildxml(a1, a2, c, s, z5):
    result = xmlTemplete.replace('@@ADDRESS1@@', a1)
    result = result.replace('@@ADDRESS2@@', a2)
    result = result.replace('@@CITY@@', c)
    result = result.replace('@@STATE@@', s)
    result = result.replace('@@ZIP5@@', z5)
    return result;

totalError = 0;
beginTime = time.time();

workfor = 3;
beginline = 10000;
endline = beginline + workfor;
with open('../facilityaddress.csv', 'rb') as csvfile:
    spamreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    #line = 0;
    for row in spamreader:
        if spamreader.line_num < beginline :
            continue;
        print(spamreader.line_num, ': ------------')
        pc = row['PostalCode']
        if len(pc) >= 5:
            pc = pc[0:5];
        
        addm = row['Address1'] + row['Address2'];
        if len(addm.strip()) == 0:
            print(row['Address1'], row['Address2'], row['City'], row['States'], pc)
            print('blank address, jump to next');
            continue;
        req = buildxml(row['Address1'], row['Address2'], row['City'], row['States'], pc);
        #print req;
        respon = reqUSPS(req);
        if  '<Error>' in respon:
            totalError += 1
            print(req)
            dom = parseString(respon);
            print(dom.toprettyxml());
        #line += 1
        if spamreader.line_num > endline :
            break;
        
print('cost: ', time.time() - beginTime);
print('****** total error: ',  totalError)

if __name__ == '__main__':
    pass