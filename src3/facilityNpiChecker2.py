#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on Apr 18, 2016

@author: lancer


'''

import npidb;
from USMailAddress import Address, Distance
import verify_by_usps
from fuzzywuzzy import fuzz, process
import time, sys
import operator
import io, csv

begin = 5000
totalLine = 100;
isOutputToFile = True;

not_print = ['9']
lowestScore = 60;

outputcsvfile = '../checked.csv'

class FileReport:
    def __init__(self):
        self.csvfile = open(outputcsvfile, 'w', encoding='utf-8')
        self.spamrwriter = csv.writer(self.csvfile, delimiter=',', quotechar='"')
        
    def setCurrInfo(self, facilityId, origName, origNpi, zscList, totalPhysician):
        self.curr = (facilityId, origName, origNpi, zscList, totalPhysician);
    
    def report(self, votebox, rhampion):
        row = [];
        row.append(self.curr[0])
        row.append(self.curr[1])
        row.append(self.curr[2])
        countOfAddr = len(self.curr[3])
        for i in range(countOfAddr):
            row.append(self.curr[3][i])
        for i in range(3 - countOfAddr):
            row.append('')
        row.append(self.curr[4])
        #((x[0], name, x[1][4][:4], x[1][3], score[0], score[1], x[1][6]))
        row.append(rhampion[0])
        row.append(rhampion[1])
        row.append(rhampion[2])
        row.append(rhampion[3])
        row.append(rhampion[4])
        row.append(rhampion[5])
        row.append(rhampion[6])
        row.append(rhampion[7])

        self.spamrwriter.writerow(row);
        
    def close(self):
        self.csvfile.close();

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
            
    def __init__(self, name, zscList):
        self.origName = name;
        self.origAddrList = zscList;
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
        highScoreAndAddr = (0, None, '-')
        
        #print (npiName)
        #print (newAddr)
        for origAddr in self.origAddrList:
            adM = Distance(newAddrM, origAddr).ad;
            adP = Distance(newAddrP, origAddr).ad;

            if newAddrM == newAddrP :
                if adM > highScoreAndAddr[0]:
                    highScoreAndAddr = (adM, newAddrM, 'Both')
            else :
                if adM > highScoreAndAddr[0]:
                    highScoreAndAddr = (adM, newAddrM, 'Mail')
                if adP > highScoreAndAddr[0]:
                    highScoreAndAddr = (adP, newAddrP, 'Prct')

        knd, detail = strDistance(npiName, self.origName)
        if knd <= lowestScore:
            return;

        self.nameDistanceMap[npiid] = (knd, highScoreAndAddr[0], npiName, highScoreAndAddr[1], highScoreAndAddr[2], detail, msg)
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
                if item[1][0] >= 0:  #avgOfNameDistance:
                    sorted_x.append(item);
            sorted_x = sorted(sorted_x, key=lambda x:(x[1][0] + x[1][1]), reverse=True)
            #sorted_x = sorted(sorted_x, key=lambda x:(x[1][0]), reverse=True)

        else :
            statReport.report('0.0 : no suitable record be found');
        return sorted_x

    def show(self, nameList):
        maxNameScore = 0;
        maxAddrScore = 0;
        for index, x in enumerate(nameList):  
            name = x[1][2]
            #score = (x[1][0], x[1][1],x[1][5])
            score = (x[1][0], x[1][1]) # no detail
            print (x[0], '(',name,')', x[1][4][:4]+':(',x[1][3],')', score, x[1][6])
            if index == 0:
                nameScore = score[0] // 10 * 10;                
                addrScore = score[1] // 10 * 10; 
                statReport.report('9.0 : name score %03d' % nameScore);
                statReport.report('9.1 : addr score %03d' % addrScore);

                maxNameScore = score[0];
                maxAddrScore = score[1];
                if maxNameScore > 80 and maxAddrScore > 90:
                    statReport.report('9.2 : maxNameScore > 80 and maxAddrScore > 90');
                if isOutputToFile:
                    w = x[0].split(',')
                    #print (w[0], w[1].strip(' :'), name, x[1][4], x[1][3], score[0], score[1], x[1][6], x[1][6][0])
                    fileReport.report(self, ((w[0], w[1].strip(' :'), name, x[1][4], x[1][3], score[0], score[1], x[1][6][0])));

            if score[0] < maxNameScore -5 or score[1] < maxAddrScore - 5 or index > 10:
                break;
        if isOutputToFile and len(nameList) == 0:
            fileReport.report(self, ('','','','','','','',''));
    
def packInfo(record):
    addressKList = []
    name = record[4]
    npi = record[6] 
    facilityId = record[0];
    totalPhysicians = record[15];
    if record[7] != None :
        addr = Address(record[7], record[8] + ' ' + record[9], record[10], record[11], record[12], record[14], msg='BillingAddress')
    else :
        addr = None;
    addressKList.append(addr)  
    conn = npidb.getConnection()
    addrs = npidb.gatFacilityAddress(conn, facilityId);
    for atuple in addrs :
        addressKList.append(Address(atuple[0],atuple[1] + " " + atuple[2],atuple[3],atuple[4], atuple[5], msg='FacilityAddress'))  
    return (facilityId, name, npi, addressKList, totalPhysicians);



def strDistance(name1, name2):
    if name1 == None or name2 == None :
        return 0
    
    allr = (fuzz.partial_ratio(name1, name2), fuzz.UWRatio(name1, name2), fuzz.partial_token_set_ratio(name1, name2), fuzz.partial_token_sort_ratio(name1, name2));
    return (sum(allr) // len(allr), allr)
    
def getNameByIds(npiidList):
    
    return npidb.searchNameByIds(conn, npiidList);


if __name__ == '__main__':
    statReport = Reporter();
    conn = npidb.getConnection()
    facilityTable = npidb.getFacility(conn, begin, totalLine)
    itemCount = 0;
    if isOutputToFile : 
        fileReport = FileReport();
    
    for record in facilityTable :
        procRecordStartTime = time.time();
        npiidList = set()
        itemCount += 1;
        print()
        origAddrList = {}
        (facilityId, origName, origNpi, zscList, totalPhysician) = packInfo(record);
        if isOutputToFile :
            fileReport.setCurrInfo(facilityId, origName, origNpi, zscList, totalPhysician);
        print (itemCount, ':', facilityId)
        print ('ONPI :', origNpi)
        print ('ON :', origName)
        print('totalPhysician :', totalPhysician)
        for addr in zscList:
            #print(addr);
            (rewroteAddress, msg) = verify_by_usps.reqUSPS(addr)
            if rewroteAddress == None : # USPS don't understand this address
                addr.msg += " (WARNING:This address can't checkout from USPS)"
                origAddrList[addr.tokeystr()] = addr;
            elif  rewroteAddress.isEmpty() : # at least, city/state is right
                origAddrList[addr.tokeystr()] = addr;
            elif rewroteAddress != addr:
                origAddrList[addr.tokeystr()] = addr;
                rewroteAddress.msg = addr.msg+'/USPS';
                origAddrList[rewroteAddress.tokeystr()] = rewroteAddress;
            else : # rewroteAddress == addr
                origAddrList[addr.tokeystr()] = addr;
        for addr in origAddrList.values():
            #print('filted by tokeystr (', addr, ')');
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
        zscList = vbox.uniqZSCList();
        print ('check in %d city/state/zip5 group' % len(zscList))
        resultset = npidb.searchNameByMZSC(conn, zscList)
        for row in resultset :
            mailAddr = Address(row[3], row[4], row[5], row[6], row[7])
            practAddr = Address(row[8], row[9], row[10], row[11], row[12])
            lastUdt = row[13]
            isSoleProprietor = row[14]
            
            vbox.add(row[0] + ', PN:', row[1], mailAddr, practAddr, (lastUdt, isSoleProprietor))
            if row[2] != '':
                vbox.add(row[0] + ', ON:', row[2], mailAddr, practAddr, (lastUdt, isSoleProprietor))

        print ('total cost for this db access : %6.2f sec' % (time.time() - dbaccessstart));
        result = vbox.choice();
        vbox.show(result);
        print ('total cost for this record : %6.2f sec' % (time.time() - procRecordStartTime));
    conn.close();
    statReport.showStat()
    if isOutputToFile : 
        fileReport.close();
    pass