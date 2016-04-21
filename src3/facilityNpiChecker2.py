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

lowestScore = 50;

class VoteBox:
            
    def __init__(self, name, addrList):
        self.origName = name;
        self.origAddrList = addrList;
        self.nameDistanceMap = {}
        self.nameAddrsMap = {}
        
    def uniqZSCList(self):
        aMap = {}
        for addr in self.origAddrList:
            key = addr.zip5 + addr.state + addr.city;
            value = (addr.zip5, addr.state, addr.city);
            aMap[key] = value;
        return aMap.values();

    def add(self, npiid, npiName, newAddrM, newAddrP, msg):
        addrHighScoreM = 0;
        addrHighScoreP = 0;
        addrHighScore = 0
        highScoreCompAddr = None;
        highScoreAddrName = 'Mail'
        #print (npiName)
        #print (newAddr)
        for origAddr in self.origAddrList:
            adM = Distance(newAddrM, origAddr).ad;
            adP = Distance(newAddrP, origAddr).ad;
            #print (key, ': (', origAddr, ') score:', ad)
            if adM > addrHighScoreM :
                addrHighScoreM = adM;
            if adP > addrHighScoreP :
                addrHighScoreP = adP;
        if adM >= adP:
            highScoreCompAddr = newAddrM
            addrHighScore = addrHighScoreM
        else :
            highScoreCompAddr = newAddrP
            addrHighScore = addrHighScoreP
            highScoreAddrName = 'Prct'

        knd, detail = strDistance(npiName, self.origName)
        if knd <= lowestScore:
            return;

        self.nameDistanceMap[npiid] = (knd, addrHighScore, npiName, highScoreCompAddr, highScoreAddrName, detail, msg)
        #print (self.nameDistanceMap[npiid])
    def choice(self):
        sortedResult = sorted(self.nameDistanceMap.items(), key=operator.itemgetter(0), reverse=True)
        sorted_x = []
        avgOfNameDistance = 0;
        count = 0;
        for item in sortedResult:
            avgOfNameDistance += item[1][0];
            count += 1;

        print('name distance > %d, has %d organization name' % (lowestScore, count))
        if count > 0:
            avgOfNameDistance = avgOfNameDistance // count;
            print ('avgOfNameDistance : %02d' % avgOfNameDistance)
            for item in sortedResult:
                if item[1][0] >= avgOfNameDistance:
                    sorted_x.append(item);
            sorted_x = sorted(sorted_x, key=lambda x:(x[1][0] + x[1][1]), reverse=True)
        else :
            print ('no suitable item in result:')
            self.show(sortedResult);
        return sorted_x

    def show(self, nameList):
        for index, x in enumerate(nameList):
            name = x[1][2]
            score = (x[1][0], x[1][1],x[1][5])
            if index > 10 : 
                break
            print (x[0], '(',name, '), (', x[1][3], '), ', x[1][4][:1],',', score, x[1][6])
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
    
    allr = (fuzz.partial_ratio(name1, name2), fuzz.UWRatio(name1, name2), fuzz.partial_token_set_ratio(name1, name2), fuzz.partial_token_sort_ratio(name1, name2));
    return (sum(allr) // len(allr), allr)
    
def getNameByIds(npiidList):
    
    return npidb.searchNameByIds(conn, npiidList);


if __name__ == '__main__':
    statReport = Reporter();
    conn = facilitydb.getConnection()
    facilityTable = facilitydb.getFacility(conn, begin, totalLine)
    itemCount = 0;
    
    for record in facilityTable :
        procRecordStartTime = time.time();
        npiidList = set()
        itemCount += 1;
        print()
        print (itemCount)
        #print (record)
        origAddrList = {}
        (origName, origNpi, addrList) = packInfo(record);
        print ('ONPI :', origNpi)
        print ('ON :', origName)
        for addr in addrList:
            origAddrList[addr.tokeystr()] = addr;
            (rewroteAddress, msg) = verify_by_usps.reqUSPS(addr)
            if rewroteAddress != None and rewroteAddress != addr:
                origAddrList[rewroteAddress.tokeystr()] = rewroteAddress;
        for addr in origAddrList.values():
            print(addr);
        
        vbox = VoteBox(origName, origAddrList.values())

        dbaccessstart = time.time();
        '''
        NPI,
        Provider_Organization_Name, 
        Provider_Other_Organization_Name,
        Provider_First_Line_Business_Mailing_Address, 
        Provider_Second_Line_Business_Mailing_Address,
        Provider_Business_Mailing_Address_City_Name,
        Provider_Business_Mailing_Address_State_Name,
        Provider_Business_Mailing_Address_Postal_Code,
        Provider_First_Line_Business_Practice_Location_Address, 
        Provider_Second_Line_Business_Practice_Location_Address,
        Provider_Business_Practice_Location_Address_City_Name,
        Provider_Business_Practice_Location_Address_State_Name,
        Provider_Business_Practice_Location_Address_Postal_Code
        '''
        resultset = npidb.searchNameByMZSC(conn, vbox.uniqZSCList())
        for row in resultset :
            mailAddr = Address(row[3], row[4], row[5], row[6], row[7])
            practAddr = Address(row[8], row[9], row[10], row[11], row[12])
            lastUdt = row[13]
            isSoleProprietor = row[14]
            
            vbox.add(row[0] + ':P', row[1], mailAddr, practAddr, (lastUdt, isSoleProprietor))
            if row[2] != '':
                vbox.add(row[0] + ':O', row[2], mailAddr, practAddr, (lastUdt, isSoleProprietor))

        print ('total cost for this db access : %6.2f sec' % (time.time() - dbaccessstart));
        result = vbox.choice();
        vbox.show(result);
        print ('total cost for this record : %6.2f sec' % (time.time() - procRecordStartTime));
    conn.close();
    statReport.showStat()
    pass