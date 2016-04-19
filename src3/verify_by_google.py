'''
Created on Mar 22, 2016

@author: lancer
'''

import urllib.request, urllib.parse;
import json
import string
import time, sys
import npidb;
from USMailAddress import Address, AddressLexical, Distance

serverHead = 'https://maps.googleapis.com/'
urlreqHead = 'maps/api/geocode/json?address='
urlreqMiddle = '1600+Amphitheatre+Parkway,+Mountain+View,+CA'
urlreqTail = '&key=AIzaSyCuKahvpDpHsjec6YWLurhED26GD_gfavg'

class Reporter:
    def __init__(self):

        self.statCount = {}
        self.addrCount = 0;
        self.startTime = time.time();
        self.dotCount = 0;
        print('000000', end=': ',)
        pass
    def report(self, stat):
        self.addrCount += 1;
        if stat in self.statCount:
            self.statCount[stat] += 1;
        else : 
            self.statCount[stat] = 1;
        self.dotCount += 1;
        #print(stat)
        sys.stdout.flush()
        if self.dotCount > 50:
            self.dotCount = 0
            print()
            
    def showStat(self):
        print();
        for item in self.statCount :
            print ('total of', item, ': ', self.statCount[item]);
        print ('total cost = {0:.2f} sec'.format((time.time() - self.startTime)))
        print ('total addresses =', str(self.addrCount))

def replacePunctuationWithPlus(origStr):
    tranmap = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
    a = origStr.translate(tranmap)
    b = a.split()
    return '+'.join( urllib.parse.quote(x) for x in b)

def buildGoogleReq(addr):
    addrElements = []
    if len(addr.addr1) >0 :
        addrElements.append(replacePunctuationWithPlus(addr.addr1))
    if len(addr.addr2) >0 :
        addrElements.append(replacePunctuationWithPlus(addr.addr2))
    if len(addr.city) >0 :
        addrElements.append(replacePunctuationWithPlus(addr.city))
    if len(addr.state) >0 :
        addrElements.append(replacePunctuationWithPlus(addr.state))
        '''
    if len(addr.zip5) > 0 and addr.zip5 != '00000' :
        addrElements.append(addr.zip5) '''
    #print (addrElements)
    ue = urlreqHead + ','.join(addrElements) + urlreqTail
    #print(ue)
    #ueq = urllib.parse.quote(urlreqHead + ','.join(addrElements) + urlreqTail)
    #print(ueq)
    url = serverHead + ue
    return url


''' return (prefectAddr, msg, alternative) '''
def reqGoogle(addr):
    
    qs = buildGoogleReq(addr);
    #print ("qs = ", qs)

    #print (qs)
    r1 = urllib.request.urlopen(qs);
    #conn.request("GET", qs)
    #r1 = conn.getresponse()
    #print (r1.status, r1.reason)
    if r1.status != 200:
        return (None, (r1.status, r1.reason), [])

    #b'aaa'.encode(encoding='utf_8')
    result = r1.read().decode("utf-8")
    print(result)
    resp = json.loads(result);
    
    #print (resp['status'])
    allReturnAddr = []
    for r in resp['results'] :
        #print ( r['formatted_address'])
        words =  r['formatted_address'].upper().split(',');
        #print (words)
        if len(words) < 4 : 
            print()
            print (addr)
            print (words)
            print ('This is not detail address, ignored.');
            continue;
        nation = words[-1].strip()
        sp5 = words[-2].strip().split();
        if len(sp5) >= 1 :
            s = sp5[0].strip()
        else :
            s = '--'
        if len(sp5) >= 2 :
            p5 = sp5[1].strip()
        else :
            p5 = '00000'
        city = words[-3].strip()
        addr = words[-4].strip()
        newAddr = Address(addr, '', city, s, p5, nation)
        allReturnAddr.append(newAddr);

    if len(allReturnAddr) > 0:
        selected = allReturnAddr[0];
    else :
        selected = None;
    return (selected, 'OK', allReturnAddr);

if __name__ == '__main__':
    statReport = Reporter()
    conn = npidb.getConnection()
    r = npidb.fetchBlank(conn, '', 10);
    for row in r:
        va, oa = npidb.createAddrFromRow(row)

        print();
        print(row[22], row[24]);
        print (oa)
        
        if oa.isPOBox() :
            print ('is a Post Mail Box')
            statReport.report('Post Mail Box')
            continue;
        
        a2, msg, alt = reqGoogle(oa);

        statReport.report(len(alt))
        for ga in alt:
            print (ga);
            print(Distance(oa, ga))

    statReport.showStat()

    
    