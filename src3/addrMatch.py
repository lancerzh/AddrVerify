'''
Created on Apr 12, 2016

@author: lancer
'''
from USMailAddress import Address, AddressLexical,Distance
import verify_by_usps
import socket
import time
import sys
import npidb
import USMailAddress
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import re;
import string;


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
        print(stat)
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
        
def rewriteAddr1Addr2(addr):
    newAddr = Address(addr.addr1, addr.addr2, addr.city, addr.state, addr.zip5);
    lex = AddressLexical(addr.addr1, addr.addr2);
    lex.replaceAbbr();
    newAddr.addr1 = lex.addr1;
    newAddr.addr2 = lex.addr2;
    return newAddr;

def splitAlphaNumStr(sentence):
    words = sentence.split();
    for i, word in enumerate(words) :
        word = word.upper();
        '''proc countable digit'''
        p = word[:-3];
        s = word[-3:]
        if s in ['1ST', '2ND', '3RD', '4TH', '5TH', '6TH', '7TH', '8TH', '9TH', '0TH'] and (p == '' or p.isdigit()) :
            words[i] = word;
        else :
            reObj = re.match(r'^([A-Z]*)([0-9]+)([A-Z]*)$', word)
            if reObj :
                words[i] = ' '.join(reObj.groups())
            else :
                words[i] = word;
    return ' '.join(words).strip();

def splitAlphaNum(addr):
    return Address(splitAlphaNumStr(addr.addr1), splitAlphaNumStr(addr.addr2), addr.city, addr.state, addr.zip5);

def useA1only(addr):
    return Address(addr.addr1, '', addr.city, addr.state, addr.zip5);

def swapA1A2(addr):
    return Address(addr.addr2, addr.addr1, addr.city, addr.state, addr.zip5);

def useA2withoutA1(addr):
    return Address(addr.addr2, '', addr.city, addr.state, addr.zip5);

def useA1plugA2(addr):
    return Address(addr.addr1 + ' ' + addr.addr2, '', addr.city, addr.state, addr.zip5);

def useCSZ(addr):
    return Address('', '', addr.city, addr.state, addr.zip5);

def replaceunctuation(addr):
    tranmap = str.maketrans('-#.&', '    ')
    a1 = addr.addr1.translate(tranmap)
    a2 = addr.addr2.translate(tranmap)
    return Address(a1, a2, addr.city, addr.state, addr.zip5 + addr.zip4);

def wrongAbbr(addr):
    a1w = addr.addr1.split();
    replaceWords = {}
    for w in a1w :
        w = w.strip(' .#');
        if len(w) <= 4:
            dt = {};
            for abbr in USMailAddress.suffixes :
                d = fuzz.ratio(w, abbr);
                dt[d] = abbr;
            dmax = max(dt.keys());
            if dmax > 70 and dmax < 100:
                print (dmax, dt[dmax], w)
                replaceWords[w] = dt[dmax]
                continue;
    newstr = addr.addr1;
    for ow in replaceWords :
        nw = replaceWords[ow]
        newstr = newstr.replace(ow, nw);
    newAddr = Address(newstr, addr.addr2, addr.city, addr.state, addr.zip5 + addr.zip4);
    return newAddr;

rewriteMothed = [rewriteAddr1Addr2, 
                 splitAlphaNum, 
                 replaceunctuation, 
                 swapA1A2,
                 useA1plugA2,
                 useA2withoutA1,
                 useA1only,
                 useCSZ]

rewriteMothedName = ['rewriteAddr1Addr2', 
                 'splitAlphaNum', 
                 'replacepunctuation', 
                 'swapA1A2',
                 'useA1plugA2',
                 'useA2withoutA1',
                 'noSecondAddr',
                 'useCSZ']

def verify(addr):
    uspsAddr, msg = verify_by_usps.reqUSPS(addr)

    for index, func in enumerate(rewriteMothed):       
        
        newAddr = func(addr);
        #print(newAddr)
        uspsAddr, msg = verify_by_usps.reqUSPS(newAddr)
        if uspsAddr == None :
            continue;
        return uspsAddr, newAddr, rewriteMothedName[index]
    
    else :
        return None, newAddr, msg;



if __name__ == '__main__':
    statReport = Reporter()
    r = npidb.fetchBlank('1467455782', 300);
    for row in r:
        va, oa = npidb.createAddrFromRow(row)
        print();
        print(row[22], row[24]);
        print (oa)
        a2, la, msg = verify(oa);

        if a2 != None:
            statReport.report(msg)
            print (la)
            print (a2);
            print(Distance(oa, a2))
        else:
            print (la);
            statReport.report(':'.join(msg))

    statReport.showStat()
    pass