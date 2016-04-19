'''
Created on Apr 18, 2016

@author: lancer
'''
import facilitydb;
import npidb;
from USMailAddress import Address, calcDistance
import verify_by_usps
from fuzzywuzzy import fuzz, process
import time, sys
import operator

begin = 0
totalLine = 100;

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
    conn = facilitydb.getConnection()
    addrs = facilitydb.gatFacilityAddress(conn, facilityId);
    for atuple in addrs :
        addressKList.append(Address(atuple[0],atuple[1] + " " + atuple[2],atuple[3],atuple[4], atuple[5]))  
    return (name, npi, addressKList);



def strDistance(name1, name2):
    if name1 == None or name2 == None :
        return 0
    #print (name1)
    #print (name2)
    return fuzz.token_set_ratio(name1, name2);

def getNameByIds(npiidList):
    
    return npidb.searchNameByIds(conn, npiidList);

if __name__ == '__main__':
    statReport = Reporter();
    conn = facilitydb.getConnection()
    facilityTable = facilitydb.getFacility(conn, begin, totalLine)
    itemCount = 0;
    
    for record in facilityTable :
        npiidList = set()
        itemCount += 1;
        print()
        print (itemCount)
        #print (record)
        (origName, npi, addrList) = packInfo(record);
        print ('ONPI :', npi)
        print ('ON :', origName)
        addrmap = {};
        for addr in addrList :
            print ('OF :', addr)
            rd = addr
            
            (rd, msg) = verify_by_usps.reqUSPS(rd)
            if rd == None :
                statReport.report('0.0 usps return none ');
                continue;
            print ('UA :', rd)   
            addrmap[rd.zip5+rd.state+rd.city] = rd
            
        print('addrmap length = ', len(addrmap))
        if len(addrmap) == 0:
            statReport.report('0.0 have not rewrite address, jump ');
            continue;
        nameDistance = {}
        nameAddrs = {}
        for key in addrmap.keys():
            addr = addrmap[key]
            nameList = npidb.searchNameByMZSC(conn, addr)
            
            for n in nameList :
                #Provider_Organization_Name
                npiName = n[0]
                #print (n)
                d = strDistance(npiName, origName)
                newAddr = Address(n[1], n[2], addr.city, addr.state, addr.zip5)
                addrDistance = calcDistance(newAddr, addr)
                if npiName in nameDistance.keys() :
                    oldv = nameDistance[npiName]
                    if d > oldv :
                        nameDistance[npiName] = d 
                        nameAddrs[npiName] = (str(newAddr), addrDistance[0], 'p')
                else :
                    nameDistance[npiName] = d 
                    nameAddrs[npiName] = (str(newAddr), addrDistance[0], 'p')
                    
                # Provider_Other_Organization_Name
                npiName = n[3]
                if npiName != '':
                    d = strDistance(npiName, origName)
                    newAddr = Address(n[1], n[2], addr.city, addr.state, addr.zip5)
                    addrDistance = calcDistance(newAddr, addr)
                    if npiName in nameDistance.keys() :
                        oldv = nameDistance[npiName]
                        if d > oldv :
                            nameDistance[npiName] = d 
                            nameAddrs[npiName] = (str(newAddr), addrDistance[0], 'othername')
                    else :
                        nameDistance[npiName] = d 
                        nameAddrs[npiName] = (str(newAddr), addrDistance[0], 'othername')
        sorted_x = sorted(nameDistance.items(), key=operator.itemgetter(1), reverse=True)
        print('total organization = ', len(sorted_x))
        for index, x in enumerate(sorted_x):
            if index > 10 : 
                break
            print (x, nameAddrs[x[0]])
            if index == 0:
                score = x[1] // 10 * 10;
                
                if score == 100 :
                    score = 99;
                statReport.report('9.0 : score ' + str(score));

    conn.close();
    statReport.showStat()
    pass