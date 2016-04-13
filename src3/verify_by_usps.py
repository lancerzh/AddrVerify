'''
Created on Mar 22, 2016

@author: lancer
'''

import urllib.request, urllib.parse, urllib.error;

from xml.dom.minidom import parseString
from makeSuffixDict import suffixes, prefixes, qualifiers ;
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

class AddressLexical:

    def __init__(self, addr1, addr2 = '', addr3 = ''):
        
        self.primary = [ ];
        self.secondary = [ ];
        self.addr1 = addr1;
        self.addr2 = addr2;
        self.addr3 = addr3;
        address = " ".join((addr1, addr2, addr3));
        words = address.split();
        
        lex = [];
        for w in words :
            w = w.strip('.,').upper();
            if w == '' :
                lex.append('B');
                continue;
            if w in list(prefixes.keys()) :
                lex.append('P');
                continue;
            if w in list(suffixes.keys()) :
                lex.append('S');
                continue;
            if w in list(qualifiers.keys()) :
                lex.append('Q');
                continue;
            lex.append('-');
        #print address
        #print lex
            
        # find index of last prefix from left, 
        index1 = 0;
        index2 = len(words);
        for i, posw in enumerate(lex) :
            if posw != 'P' :
                index1 = i;
                break;
        #find index of first prefix or last suffix from right
        lex.reverse();
        for i, posw in enumerate(lex) :
            if i >= len(words) - index1 : 
                break;
            if posw == 'S' :
                index2 = len(words) - i;
                break;
            if posw == 'P' :
                index2 = len(words) - i - 1;
                continue;
        
        # split first level address from second level address
        if index1 > 0:
            index1 += 1;
            self.secondary.append(' '.join(words[0:index1]));
        if index2 < len(words) :
            self.secondary.append(' '.join(words[index2:]));
        #print index1, index2
        self.primary.append(' '.join(words[index1:index2]));
        
    def __str__(self):
        return self.primary[0] + "|" + ' '.join(self.secondary);
    
    def replaceAbbr(self):
        a = '';
        for p in self.primary:
            if len(p.strip()) == 0 :
                continue;
            w = p.split()[-1]
            #print 'pri w' + w
            if w in list(suffixes.keys()):
                #print 'pri w', w, suffixes[w][0]
                p = p.replace(w, suffixes[w][0]);
            a += ' ' + p
        self.addr1 = a.strip();
        a = '';
        for p in self.secondary:
            if len(p.strip()) == 0 :
                continue;
            w = p.split()[0]
            #print 'sec w' + w
            if w in list(prefixes.keys()):
                #print 'sec w', w, prefixes[w][1]
                p = p.replace(w, prefixes[w][1]);
            a += ' ' + p
        self.addr2 = a.strip();
        
class Address:
    def __init__(self, a1, a2, c, s, z, n='US'):
        
        self.addr1 = a1;
        self.addr2 = a2;
        '''
        lex = AddressLexical(a1, a2);
        lex.replaceAbbr();
        self.addr1 = lex.addr1;
        self.addr2 = lex.addr2;
        '''
        self.city = c;
        self.state = s;
        self.nation = n;
        z = z.strip();
        if len(z) >=5 :
            self.zip5 = z[0:5];
            self.zip4 = z[5:];
        else :
            self.zip5 = z;
            self.zip4 = ''
        self.zip4 = self.zip4.strip(' -');
        if len(self.zip5) < 5:
            self.zip5 = '{:0<5s}'.format(self.zip5);
        if len(self.zip4) < 4:
            self.zip4 = '{:0<4s}'.format(self.zip4);
            
    def __eq__(self, other):
        if other == None:
            return False;
        if not isinstance(other, Address) :
            return False
        if self.nation != other.nation :
            return False
        if self.city == other.city and self.state == other.state and self.zip5 == other.zip5 :
            return (self.addr1 == other.addr1 and self.addr2 == other.addr2) or (self.addr1 == other.addr2 and self.addr2 == other.addr1) 
        else :
            return False
        
        
    def __str__(self) :
        return ','.join((self.addr1, self.addr2, self.city, self.state, self.zip5, self.zip4));
    
    def getSortStr(self):
        return ','.join((self.zip5, self.zip4, self.state, self.city, self.addr1, self.addr2)) ;
    
    def buildxml(self):
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
        return xmlTemplete.format(self.addr1, self.addr2, self.city, self.state, self.zip5, '')
    
    def isEmpty(self):
        if len((self.addr1 + self.addr2).strip()) > 0 : 
            return False
        else :
            return True
        
    def isForeign(self):
        if self.nation == 'USA' :
            return False
        if len(self.state) > 0 : 
            return False
        else :
            return True;

urlString = '/ShippingAPI.dll?API=Verify&XML=';

def getText(xmlDoc, tagName):
    tag = xmlDoc.getElementsByTagName(tagName);
    if tag.length > 0 and tag[0].childNodes.length > 0:
        return tag[0].firstChild.nodeValue;
    else :
        return None;

def reqUSPS(addr):
    qs = urlString + urllib.parse.quote(addr.buildxml());

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
        z5 = '00000';
        
    z4 = getText(dom, 'Zip4');
    if  z4 != None and z4 != '' and len(addr.zip4) == 4 and addr.zip4 !='0000':
        pass
    else :
        z4 = '0000'


    #return (Address(a1, a2, c, s, z5 + z4), dom.toprettyxml(), distance);
    return (Address(a1, a2, c, s, z5 + z4), '');

def calcDistance(a1, a2):
    if a1 == None or a2 == None :
        return [0, 0, 0, 0, 0, 0, 0]
    
    a1d = fuzz.ratio(a1.addr1, a2.addr1);
    
    a2d = fuzz.ratio(a1.addr2, a2.addr2);

    ad = fuzz.token_set_ratio(a1.addr1 + ' ' + a1.addr2, a2.addr1 + ' ' + a2.addr2);

    cd = fuzz.ratio(a1.city, a2.city)
    
    sd = fuzz.ratio(a1.state, a2.state)

    z5d = fuzz.ratio(a1.zip5, a2.zip5);
        
    z4d = fuzz.ratio(a1.zip4, a2.zip4);

    return [ad, a2d, a1d, cd, sd, z5d, z4d];

if __name__ == '__main__':
    pass