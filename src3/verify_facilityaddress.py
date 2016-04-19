#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on Mar 28, 2016

@author: lancer
'''
import verify_by_usps;
import verify_by_google;
import npidb;
import USMailAddress
import csv;
import time,sys;
import io;

workfor = 100;
beginline = 4500;
endline = beginline + workfor;

# addr1, addr2, city, states, postalCode
#addressFile = '../billingaddress.csv';
#indexs = (5,6,9, 11, 8); # for billingaddress
addressFile = '../facilityaddress.csv'
#addressFile = '../xad'

indexs = (6,7,9,10,11); # for facilityaddress

verifiedFile = '../verified.csv';
nopassFile = '../noverified.csv';

countEmpty = 0;
countForeign = 0;

totalError = 0;
beginTime = time.time();

class Reporter:
    def __init__(self, spamreader, outputFlags = []):
        self.outputFlags = outputFlags;
        self.reader = spamreader;
        self.lineBegin = spamreader.line_num;
        self.currentLineNum = spamreader.line_num;
        self.statCount = {}
        self.addrCount = 0;
        self.startTime = time.time();
        self.dotCount = 0;
        print('000000', end=': ',)
        pass
    def report(self, stat):
        self.currentLineNum = spamreader.line_num;
        self.addrCount += 1;
        if stat in self.statCount:
            self.statCount[stat] += 1;
        else : 
            self.statCount[stat] = 1;
        self.dotCount += 1;
        for s in self.outputFlags:
            if stat.startswith(s):
                print(stat)
        sys.stdout.flush()

            
    def showStat(self):
        print();
        for item in sorted(self.statCount.keys()) :
            print (self.statCount[item], 'total of', item);
        print ('total cost = {0:.2f} sec'.format((time.time() - self.startTime)))
        print ('total addresses =', str(self.currentLineNum - self.lineBegin))

def checkDistance(msg, origAddr, rewriteAddr):
    statReport.report('distance calc');
    dtsr = USMailAddress.Distance(origAddr, rewriteAddr);
    if dtsr.isMatched() == False :
        statReport.report('distance not match');
        print ('OF :', origAddr)
        print (msg, rewriteAddr)
        print (dtsr.detail())
        
def readAddrFrom(row):
    a1 = row[indexs[0] - 1].upper()
    a2 = row[indexs[1] - 1].upper()
    c = row[indexs[2]  - 1].upper()
    s = row[indexs[3]  - 1].upper()
    z = row[indexs[4]  - 1].upper()
    return USMailAddress.Address(a1, a2, c, s, z);

if __name__ == '__main__':
    #vf = open(verifiedFile, 'w');
    #nvf = open(nopassFile, 'w');
    #nvf.write('' + '\n');
    conn = npidb.getConnection();
    lineCount = 0;
    with io.open(addressFile, 'r', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        statReport = Reporter(spamreader, ['3.1', '3.4']);
        statReport.lineBegin = beginline;
        
        for row in spamreader:
            
            if spamreader.line_num <= beginline:
                continue;
            if spamreader.line_num > endline :
                break;
            print (spamreader.line_num, beginline, endline)
            #print (row);
            #print row[indexOfZip - 1], row[indexOfState -1], row[indexOfCity - 1], row[indexOfAddr2 - 1], row[indexOfAddr1 - 1]
            addr = readAddrFrom(row)
            #print('OF :', addr)
            #print spamreader.line_num, ': ', addr;
            if addr.isEmpty():
                statReport.report('0. BLANK')
                continue;
            elif addr.isForeign():
                statReport.report('0. Foreign')
                continue;
            
            ro = npidb.searchAddrInOrig(conn, addr);
            if len(ro) > 0  :
                statReport.report('1.1 Directly:Tested Address Found In Orig Addr')
                continue;
            r = npidb.searchAddrInVerified(conn, addr);
            if len(r) > 0 :
                statReport.report('1.2 Directly:Tested Address Found In Verified Addr')
                continue;
            (uspsAddr, msg ) = verify_by_usps.reqUSPS(addr);
            statReport.report('2.0 usps:request the address to US Postal Office')
            if uspsAddr != None :
                r = npidb.searchAddrInVerified(conn, uspsAddr);
                if len(r) > 0 :
                    statReport.report('2.1 usps:address Found In Verified DB')
                else :
                    statReport.report('2.2 usps:address Not Found In Verified Addr')
                    checkDistance('UA :', addr, uspsAddr)
                continue;
            if addr.isPOBox() :
                statReport.report('3.9 google:Postal Office Box, dont request to google')
                continue;
            (ga, msg, al) = verify_by_google.reqGoogle(addr)
            statReport.report('3.0 google:request the address to google map')
            if ga != None :
                (gua, msg ) = verify_by_usps.reqUSPS(ga);
                if gua == None :
                    print('OF :', addr)
                    print('GA :', ga)
                    print('MSG:', msg)
                    statReport.report('3.1 google:address Not Found In USPS')
                    checkDistance('UG :', addr, ga)
                    continue;
                r = npidb.searchAddrInVerified(conn, gua);
                if len(r) > 0 :
                    statReport.report('3.2 google:address Found In Verified DB:')
                else :
                    statReport.report('3.3 google:no found in Verified DB' )
                    checkDistance('GU :', addr, gua)
                continue;
            else :
                print('OF :', addr)
                statReport.report('3.4 google:not return a address' )
            #distance = USMailAddress.calcDistance(addr, uspsAddr);

            #nvf.write(addr.__str__() + ',' + str(spamreader.line_num) + '\n');

    '''
    vf.write(uspsAddr.getSortStr() + 
             ',"' + ', '.join([row[indexs[0] - 1], row[indexs[1]  - 1], row[indexs[2]  - 1], row[indexs[3]  -1], row[indexs[4]  - 1]])
              + '",' + ','.join(distance) 
              + ','  + str(spamreader.line_num) + '\n')
    
    
    distance.reverse();
    
    vf.write(uspsAddr.getSortStr() + ', ' 
             + addr.getSortStr() 
             + ',' + ','.join(str(x) for x in distance)
             + '\n');
             '''

    conn.close();
    
    statReport.showStat();

    #vf.close();
    #nvf.close();

    pass