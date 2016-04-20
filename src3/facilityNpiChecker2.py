#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on Apr 18, 2016

@author: lancer


'''
import facilitydb;
import npidb;
from USMailAddress import Address, Distance
import verify_by_usps
from fuzzywuzzy import fuzz, process
import time, sys
import operator

begin = 3320
totalLine = 500;

not_print = ['9']

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
        if stat[0:1] not in not_print :
            print(stat)
        sys.stdout.flush()

            
    def showStat(self):
        print();
        for item in sorted(self.statCount) :
            print ('total of', item, ': ', self.statCount[item]);
        print ('total cost = {0:.2f} sec'.format((time.time() - self.startTime)))
        print ('total records =', str(totalLine))

class VoteBox:
    def __init__(self, name, amap):
        self.origName = name;
        self.addrMap = amap;
        self.nameDistanceMap = {}
        self.nameAddrsMap = {}

    def add(self, npiName, newAddr, comments=''):
        highScore = 0;
        highScoreCompAddr = None;
        #print (npiName)
        #print (newAddr)
        for key in self.addrMap:
            v = self.addrMap[key]
            ad = Distance(newAddr, v).ad;
            #print (key, ': (', v, ') score:', ad)
            if ad > highScore :
                highScore = ad;
                highScoreCompAddr = v;
        #print (newAddr, highScoreCompAddr, highScore)
        #self.nameAddrsMap[npiName] = (str(newAddr), 'vs', str(highScoreCompAddr))
        self.nameAddrsMap[npiName] = (str(newAddr))

        nameDistance = strDistance(npiName, self.origName)
        if npiName in self.nameDistanceMap.keys():
            if highScore > self.nameDistanceMap[npiName][1]:
                self.nameDistanceMap[npiName] = (nameDistance, highScore, comments)
        else:
            self.nameDistanceMap[npiName] = (nameDistance, highScore, comments)
        #print (nameDistance, highScore, comments)
        #print (self.nameDistanceMap[npiName])
    def choice(self):
        lowestScore = 50;
        print('total found organization name = ', len(self.nameDistanceMap))
        sortedResult = sorted(self.nameDistanceMap.items(), key=operator.itemgetter(1), reverse=True)
        sorted_x = []
        avgOfNameDistance = 0;
        count = 0;
        for item in sortedResult:
            if item[1][0] > lowestScore:
                avgOfNameDistance += item[1][0];
                count += 1;
            else :
                break;
        print('name distance > %d, has %d' % (lowestScore, count))
        if count > 0:
            avgOfNameDistance = avgOfNameDistance // count;
            print ('avgOfNameDistance : %02d' % avgOfNameDistance)
            for item in sortedResult:
                if item[1][0] >= avgOfNameDistance:
                    sorted_x.append(item);
            sorted_x = sorted(sorted_x, key=lambda x:x[1][1], reverse=True)
        else :
            print ('no suitable item in result:')
            self.show(sortedResult);
        return sorted_x

    def show(self, nameList):
        for index, x in enumerate(nameList):
            name = x[0]
            score = x[1]
            if index > 10 : 
                break
            print ('name:(',name, '), addr: (', self.nameAddrsMap[name], '), score: ', score)
            if index == 0:
                score = score[0] // 10 * 10;
                
                if score == 100 :
                    score = 99;
                statReport.report('9.0 : score ' + str(score));


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
        (origName, origNpi, addrList) = packInfo(record);
        print ('ONPI :', origNpi)
        print ('ON :', origName)
        addrmap = {};
        for addr in addrList :
            print ('OF :', addr)
            addrmap[addr.tokeystr()] = addr
            (rd, msg) = verify_by_usps.reqUSPS(addr)
            if rd == None :
                statReport.report('0.0 usps return none');
            else :
                print ('UA :', rd)   
                addrmap[rd.tokeystr()] = rd
            
        print('addrmap length = ', len(addrmap))
        
        vbox = VoteBox(origName, addrmap)

        searchKeySet = set();
        for key in addrmap.keys():
            addr = addrmap[key]
            searchKey = addr.zip5+addr.state+addr.city
            if searchKey not in searchKeySet:
                searchKeySet.add(searchKey)
                resultset = npidb.searchNameByMZSC(conn, addr)
                print(searchKey, ': result set have ', len(resultset), 'records')
            else :
                print ('this search is done!', searchKey)
                continue;
            for row in resultset :
                #Provider_Organization_Name row[0]
                #print (row)
                vbox.add(row[0], Address(row[1], row[2], addr.city, addr.state, addr.zip5), ('PrimaryName', row[4]))
                
                # Provider_Other_Organization_Name row[3]
                if row[3] != '':
                    vbox.add(row[3], Address(row[1], row[2], addr.city, addr.state, addr.zip5), ('OtherName', row[4]))
        result = vbox.choice();
        vbox.show(result);
        
    conn.close();
    statReport.showStat()
    pass