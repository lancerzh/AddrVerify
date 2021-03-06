#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on Mar 28, 2016

@author: lancer
'''
import verify_by_usps;
import USMailAddress;
import csv, codecs, io;
import time;
import socket
import sys


'''
input npi file which can doanload from http://download.cms.gov/nppes/NPI_Files.html
It include two address infomation. one is used for business mail, other one is used for Practice Location.
This python program extract the two address infomation into a csv format file. This module also try to verify the
address by using usps address verify tool.
output file columns like this
va1, va2, vc, vs, vp5, vp4, oa1, oa2, oc, os, op5, op4, on, oda1, oda2, da, da1, da2, dc, dn, dp5, dp4, npiid, npitype, addrtype, verified

addrtype = (M[ail], P[ractice])
verified = (V[erified], N[otverified], F[oreign], E[mpty])
'''
title = "va1, va2, vc, vs, vp5, vp4, oa1, oa2, oc, os, op5, op4, on, oda1, oda2, da, da1, da2, dc, ds, dp5, dp4, npiid, npitype, addrtype, verified"
title = title.split(', ');


workfor = 10000;
'''
157926,160457， 251029
'''
beginline = 750;
#beginline = 1;


endline = beginline + workfor;

addressFile = '/Users/lancer/workspace/npi/npidata_20050523-20160313.csv'
outputFile = '../DevOut.csv';
addr1Index = (21, 22, 23, 24, 25, 26);
addr2Index = (29, 30, 31, 32, 33, 34);

NotFoundMsg = '../NotFoundMsg.txt'




def extractAddr(row, index):
    if len(row) >= max(index) :
        a1 = row[index[0] - 1];
        a2 = row[index[1] - 1];
        c = row[index[2] - 1];
        s = row[index[3] - 1];
        p = row[index[4] - 1];
        row = row[index[5] - 1];
        return verify_by_usps.Address(a1, a2, c, s, p, row);
    else :
        return None;
    
def prepareCsvRow(uspsAddr, addr, distance, npiid, npitype, addrtype, verifiedType):  
    r = []
    if uspsAddr != None :
        for x in [uspsAddr.addr1, uspsAddr.addr2, uspsAddr.city, uspsAddr.state, uspsAddr.zip5, uspsAddr.zip4]:
            r.append(x)
    else :
        for x in range(6):
            r.append('')
    
    for x in [addr.addr1, addr.addr2, addr.city, addr.state, addr.zip5, addr.zip4, addr.nation, addr.addr1, addr.addr2]:
        r.append(x)
    
    for x in distance:
        r.append(str(x))
    
    r.append(npiid)
    r.append(npitype)
    r.append(addrtype)
    r.append(verifiedType)
    return r

class Reporter:
    def __init__(self, spamreader):
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
        print(stat[0],end='')
        sys.stdout.flush()
        if self.dotCount > 50:
            self.dotCount = 0
            print()
            print('%06d' % spamreader.line_num, end=': ',)
            
    def showStat(self):
        print();
        for item in self.statCount :
            print ('total of', item, ': ', self.statCount[item]);
        print ('total cost = {0:.2f} sec'.format((time.time() - self.startTime)))
        print ('total lines =', str(self.currentLineNum - self.lineBegin))
        print ('total addresses =', str(self.addrCount))

def verify(row, addr, addrtype):
    if addr == None:
        statReport.report('ERROR')
        return None;
    if addr.isEmpty():
        statReport.report('BLANK')
        return None
    elif addr.isForeign():
        statReport.report('Foreign')
        r = prepareCsvRow(None, addr, USMailAddress.calcDistance(None, addr), row[0], row[1], addrtype, 'F')
        return r;
    else:
        try:
            uspsAddr, msg = verify_by_usps.reqUSPS(addr)
        except socket.error :
            time.sleep(5)
            statReport.report('Timeout')
            r = prepareCsvRow(None, addr, USMailAddress.calcDistance(None, addr), row[0], row[1], addrtype, 'T')
            return r
        if uspsAddr == None:
            statReport.report('NotFound')
            r = prepareCsvRow(None, addr, USMailAddress.calcDistance(uspsAddr, addr), row[0], row[1], addrtype, msg[0])
            #print (msg[0] , msg[1])
            nfm.write(msg[0] + " : " + msg[1] + '\row');
            if msg[0] != '-2147219401' :
                nfm.write(addr.__str__()+"\row")
                nfm.write(','.join(row)+'\row')
            nfm.flush();

        else:
            statReport.report('.Verified')
            r = prepareCsvRow(uspsAddr, addr, USMailAddress.calcDistance(uspsAddr, addr), row[0], row[1], addrtype, 'V') #r = prepareCsvRow(None, addr, verify_by_usps.calcDistance(None, addr), row[0], row[1], addrtype, 'E');
        #continue;
    return r
        
if __name__ == '__main__':
    
    nfm = open(NotFoundMsg, 'w', encoding='utf-8');
        
    outf = open(outputFile, 'w', encoding='utf-8');
    writer = csv.writer(outf, delimiter=',', quotechar='"');
    #print ( title);
    writer.writerow(title);
    
    verifiedType = '';
    

    with open(addressFile, 'r', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        statReport = Reporter(spamreader);
        statReport.lineBegin = beginline;
        
        uspsAddr = None
        msg = '';
        countPoint = 0;
                
        for row in spamreader:
            if spamreader.line_num <= beginline:
                continue;

            if spamreader.line_num > endline :
                break;
            
            '''
            first address
            '''
            addr = extractAddr(row, addr1Index);
            addr1 = extractAddr(row, addr2Index);
            if addr1 == addr :
                addrtype = 'MP'
            else :
                addrtype = 'M'
            
            r = verify(row, addr, addrtype)

            #print ','.join(r)
            if r != None :
                writer.writerow(r);
            ''' 
            second address
            '''
            if addrtype == 'MP' :
                continue;
            else :
                addrtype = 'P'

            r = verify(row, addr1, 'P')

            #print ','.join(r)
            if r != None :
                writer.writerow(r);

    outf.close();
    nfm.close();
    
    statReport.showStat();

    pass



