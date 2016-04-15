'''
Created on Mar 22, 2016

@author: lancer
'''

import urllib.request, urllib.parse, urllib.error;
from USMailAddress import Address, AddressLexical, suffixes, prefixes, qualifiers

from xml.dom.minidom import parseString




urlString = '/ShippingAPI.dll?API=Verify&XML=';

    
def buildxml(addr):
    xmlTemplete = '''
<AddressValidateRequest USERID="953JMS002790">
  <IncludeOptionalElements>true</IncludeOptionalElements>
  <ReturnCarrierRoute>true</ReturnCarrierRoute>
  <Address ID="0">  
    <FirmName />   
    <Address1>{0}</Address1>
    <Address2>{1}</Address2>   
    <City>{2}</City>   
    <State>{3}</State>   
    <Zip5>{4}</Zip5>   
    <Zip4>{5}</Zip4> 
  </Address>     
</AddressValidateRequest>
''';
    return xmlTemplete.format(addr.addr1, addr.addr2, addr.city, addr.state, addr.zip5, '')
    

def getText(xmlDoc, tagName):
    tag = xmlDoc.getElementsByTagName(tagName);
    if tag.length > 0 and tag[0].childNodes.length > 0:
        return tag[0].firstChild.nodeValue;
    else :
        return None;

def reqUSPS(addr):
    qs = urlString + urllib.parse.quote(buildxml(addr));

    #print (qs)
    r1 = urllib.request.urlopen("http://production.shippingapis.com/"+qs);
    #conn.request("GET", qs)
    #r1 = conn.getresponse()
    #print (r1.status, r1.reason)
    if r1.status != 200:
        return (None, (r1.status, r1.reason))

    result = r1.read()
    dom = parseString(result);
    #conn.close()
    #print (result)
    
    bb = dom.getElementsByTagName('Error')
    if len(bb) > 0 :
        #print( dom.toprettyxml());
        errCode = getText(dom, 'Number');
        errDesc = getText(dom, 'Description');
        return (None, (errCode, errDesc));
    #print ('********')
    a1 = getText(dom, 'Address2');
    if a1 == None:
        a1 = '';
        
    a2 = getText(dom, 'Address1');
    if a2 == None:
        a2 = '';
    
    c = getText(dom, 'City');
    if c == None:
        c = '';
    
    s = getText(dom, 'State');
    if s == None:
        s = '';
    
    z5 = getText(dom, 'Zip5');
    if z5 == None :
        z5 = '-----';
        
    z4 = getText(dom, 'Zip4');
    if  z4 != None and z4 != '' and len(addr.zip4) == 4 :
        pass
    else :
        z4 = '----'


    #return (Address(a1, a2, c, s, z5 + z4), dom.toprettyxml(), distance);
    return (Address(a1.upper(), a2.upper(), c.upper(), s.upper(), z5.upper() + z4.upper()), '');



if __name__ == '__main__':
    pass