'''
Created on Apr 18, 2016

@author: lancer
'''

import npidb;
from USMailAddress import Address 
import verify_by_usps
from fuzzywuzzy import fuzz, process
import time, sys

begin = 5
totalLine = 50;

class Reporter:
    def __init__(self):
        self.statCount = {}
        self.addrCount = 0;
        self.startTime = time.time();
        self.dotCount = 0;
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

            
    def showStat(self):
        print();
        for item in sorted(self.statCount) :
            print ('total of', item, ': ', self.statCount[item]);
        print ('total cost = {0:.2f} sec'.format((time.time() - self.startTime)))
        print ('total records =', str(totalLine))



def packInfo(record):
    addressKList = []
    name = record[4]
    npi = record[6] 
    facilityId = record[0];
    if record[7] != None :
        addr = Address(record[7], record[8] + ' ' + record[9], record[10], record[11], record[12], record[14])
    else :
        addr = None;
    addressKList.append(addr)  
    conn = npidb.getConnection()
    addrs = npidb.gatFacilityAddress(conn, facilityId);
    for atuple in addrs :
        addressKList.append(Address(atuple[0],atuple[1] + " " + atuple[2],atuple[3],atuple[4], atuple[5]))  
    return (name, npi, addressKList);



def calcDistance(name1, name2):
    if name1 == None or name2 == None :
        return 0
    return fuzz.ratio(name1, name2);

def getNameByIds(npiidList):
    
    return npidb.searchNameByIds(conn, npiidList);

if __name__ == '__main__':
    statReport = Reporter();
    conn = npidb.getConnection()
    facilityTable = npidb.getFacility(conn, begin, totalLine)
    itemCount = 0;
    
    for record in facilityTable :
        npiidList = set()
        itemCount += 1;
        print()
        print (itemCount)
        #print (record)
        (origName, npi, zscList) = packInfo(record);
        print ('ONPI :', npi)
        print ('ON :', origName)
        
        for addr in zscList :
            print ('OF :', addr)
            '''
            if name != None and name != '':
                (npiaddr1, npiaddr2) = checkNameInNpiDB(name)
                calcDistance(address, address)
            if npi != None and npi != '':
                checkNpiInNpiDB(infos.name)
                calcDistance(infos.name, gotName)
                calcDistance(infos.address, address)
            if addr != None:
                checkAddress(infos.address)
                calcDistance(infos.name, gotName)
            '''
            if addr == None :
                statReport.report('0.0 the address is empty')
                continue;
            (rewroteAddress, msg) = verify_by_usps.reqUSPS(addr)
            if rewroteAddress == None:
                statReport.report('0.1 not return the address by USPS')
                continue;
            print ('UA :', rewroteAddress)

            alist = npidb.searchAddrInVerified(conn, rewroteAddress);
            if len(alist) == 0 :
                statReport.report('0.2 not found the address in npi')
                continue;
            for ar in alist :
                print (ar)
                npiidList.add(str(ar[-4]))
        print (npiidList)
        if len(npiidList) == 0 :
            continue;
        resultset = getNameByIds(npiidList)
        for row in resultset :
            dist = calcDistance(row[0], origName)
            score = dist // 10 * 10;
            if score == 100 :
                score = 99;
            statReport.report('9.0' + ' distance in ' + str(score))
            print (row[0], 'DIST :', dist)

            
    conn.close();
    statReport.showStat()
    pass