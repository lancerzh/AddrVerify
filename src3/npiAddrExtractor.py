#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on Mar 28, 2016

@author: lancer
'''
import verify_by_usps;
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


workfor = 5000000;
'''
157926,160457， 251029
'''
beginline = 3227050;
#beginline = 1;


endline = beginline + workfor;

addressFile = '/Users/lancer/workspace/npi/npidata_20050523-20160313.csv'
outputFile = '../npiAddr.csv';
addr1Index = (21, 22, 23, 24, 25, 26);
addr2Index = (29, 30, 31, 32, 33, 34);

indexs = addr1Index;

countEmpty = 0;
countForeign = 0;
countLineShort = 0;

totalError = 0;
beginTime = time.time();

def extractAddr(row, index):
    if len(row) >= max(index) :
        a1 = row[index[0] - 1];
        a2 = row[index[1] - 1];
        c = row[index[2] - 1];
        s = row[index[3] - 1];
        p = row[index[4] - 1];
        n = row[index[5] - 1];
        return verify_by_usps.Address(a1, a2, c, s, p, n);
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

        
if __name__ == '__main__':
    
    print (sys.getdefaultencoding())
    
    outf = open(outputFile, 'w', encoding='utf-8');
    writer = csv.writer(outf, delimiter=',', quotechar='"');
    #print ( title);
    writer.writerow(title);
    
    verifiedType = '';
    with open(addressFile, 'r', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        uspsAddr = None
        msg = '';
        countPoint = 0;
                
        for row in spamreader:
            if spamreader.line_num <= beginline:
                continue;
            '''
            print spamreader.line_num, row
            print row[addr1Index[2] -1]
            print type(row[addr2Index[2] -1])
            #print unicode(row[addr1Index[2] -1], "utf-8")
            '''
            '''
            first address
            '''
            addr = extractAddr(row, addr1Index);
            addr1 = extractAddr(row, addr2Index);
            if addr1 == addr :
                addrtype = 'MP'
            else :
                addrtype = 'M'
            
            if addr == None:
                print("error **************")
                print(row);
                countLineShort += 1;
                #continue;
            #print spamreader.line_num, ': ', addr;
            if addr.isEmpty():
                print('E', end='')
                #print row;
                countEmpty += 1;
                #r = prepareCsvRow(None, addr, verify_by_usps.calcDistance(None, addr), row[0], row[1], addrtype, 'E');
                #continue;
            elif addr.isForeign() :
                print('F', end='')
                #print row;
                countForeign += 1;
                r = prepareCsvRow(None, addr, verify_by_usps.calcDistance(None, addr), row[0], row[1], addrtype, 'F');
            else :

                try :
                    (uspsAddr, msg) = verify_by_usps.reqUSPS(addr);
                    #print (uspsAddr)
                except socket.error as error :
                    outf.flush();
                    print(error)
                    print('sleep 5 seconds')
                    time.sleep(5)  
                    break;
                if uspsAddr == None :
                    totalError += 1;
                    print('')
                    print(spamreader.line_num, ': ', addr);
                    #print uspsAddr;
                    print(msg)
                    r = prepareCsvRow(None, addr, verify_by_usps.calcDistance(uspsAddr, addr), row[0], row[1], addrtype, msg)
                else :
                    print('.', end='')
                    countPoint += 1;
                    if countPoint > 50 :
                        countPoint = 0;
                        print();
                        sys.stdout.flush() ;
                    r = prepareCsvRow(uspsAddr, addr, verify_by_usps.calcDistance(uspsAddr, addr), row[0], row[1], addrtype, 'V')

            #print ','.join(r)
            writer.writerow(r);
            ''' 
            second address
            '''
            if addrtype != 'MP' :
                addrtype = 'P'
                addr = addr1;
            else :
                continue;
            
            if addr == None:
                print("error **************")
                print(row);
                countLineShort += 1;
                continue;
            #print spamreader.line_num, ': ', addr;
            if addr.isEmpty():
                print('E', end='')
                countEmpty += 1;
                #r = prepareCsvRow(None, addr, verify_by_usps.calcDistance(None, addr), row[0], row[1], addrtype, 'E');
                continue;
            elif addr.isForeign() :
                print('F', end='')
                countForeign += 1;
                r = prepareCsvRow(None, addr, verify_by_usps.calcDistance(None, addr), row[0], row[1], addrtype, 'F');
            else :
                try :
                    (uspsAddr, msg) = verify_by_usps.reqUSPS(addr);
                except socket.error as error :
                    outf.flush();
                    print(error)
                    print('sleep 5 seconds')
                    time.sleep(5)   
                    break;
                if uspsAddr == None :
                    totalError += 1;
                    print('')
                    print(spamreader.line_num, ': ', addr);
                    #print uspsAddr;
                    print(msg)
                    r = prepareCsvRow(None, addr, verify_by_usps.calcDistance(uspsAddr, addr), row[0], row[1], addrtype, msg)
                else :
                    print('.', end='')
                    countPoint += 1;
                    if countPoint > 50 :
                        countPoint = 0;
                        print();
                        sys.stdout.flush() ;
                    r = prepareCsvRow(uspsAddr, addr, verify_by_usps.calcDistance(uspsAddr, addr), row[0], row[1], addrtype, 'V')

            #print ','.join(r)
            writer.writerow(r);

            if spamreader.line_num > endline :
                break;
        print() 
        print('cost: ', time.time() - beginTime);
        print('totalError:', totalError)
        print('countEmpty:', countEmpty)
        print('countForeign:', countForeign)
        print('countLineShort:', countLineShort)

    outf.close();

    pass


