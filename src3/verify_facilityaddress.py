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

workfor = 100;
beginline = 200;
endline = beginline + workfor;

addressFile = '../billingaddress.csv';
verifiedFile = '../verified.csv';
nopassFile = '../noverified.csv';
# addr1, addr2, city, states, postalCode
#indexs = (6,7,9,10,11); # for facilityaddress
indexs = (5,6,9, 11, 8); # for billingaddress

countEmpty = 0;
countForeign = 0;

totalError = 0;
beginTime = time.time();

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
        print(stat)
        sys.stdout.flush()
        if self.dotCount > 50:
            self.dotCount = 0
            print()
            print('%06d' % spamreader.line_num, end=': ',)
            
    def showStat(self):
        print();
        for item in self.statCount :
            print (self.statCount[item], 'total of', item);
        print ('total cost = {0:.2f} sec'.format((time.time() - self.startTime)))
        print ('total lines =', str(self.currentLineNum - self.lineBegin))
        print ('total addresses =', str(self.addrCount))


if __name__ == '__main__':
    #vf = open(verifiedFile, 'w');
    #nvf = open(nopassFile, 'w');
    #nvf.write('' + '\n');
    conn = npidb.getConnection();
    lineCount = 0;
    with open(addressFile, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        statReport = Reporter(spamreader);
        statReport.lineBegin = beginline;
        
        for row in spamreader:
            
            if spamreader.line_num <= beginline:
                continue;
            if spamreader.line_num > endline :
                break;
            print (spamreader.line_num, beginline, endline)
            #print row[indexOfZip - 1], row[indexOfState -1], row[indexOfCity - 1], row[indexOfAddr2 - 1], row[indexOfAddr1 - 1]
            addr = USMailAddress.Address(row[indexs[0] - 1], row[indexs[1]  - 1], row[indexs[2]  - 1], row[indexs[3]  -1], row[indexs[4]  - 1]);
            print('OF :', addr)
            #print spamreader.line_num, ': ', addr;
            if addr.isEmpty():
                statReport.report('BLANK')
                continue;
            elif addr.isForeign():
                statReport.report('Foreign')
                continue;
            
            r = npidb.searchAddr(conn, addr);
            if len(r) > 0 :
                statReport.report('Orig Address Found In Verified Addr')
                continue;
            (uspsAddr, msg ) = verify_by_usps.reqUSPS(addr);
            if uspsAddr != None :
                r = npidb.searchAddr(conn, uspsAddr);
                print('UA :', uspsAddr)
                if len(r) > 0 :
                    statReport.report('usps address Found In Verified DB')
                else :
                    statReport.report('usps address Not Found In Verified Addr')
                continue;
            (ga, msg, al) = verify_by_google.reqGoogle(addr)
            statReport.report('request the address to google map')
            if ga != None :
                print('GA :', ga)
                (gua, msg ) = verify_by_usps.reqUSPS(ga);
                if gua == None :
                    statReport.report('google address Not Found In USPS')
                    continue;
                print('GU :', gua)
                r = npidb.searchAddr(conn, gua);
                if len(r) > 0 :
                    statReport.report('GUA address Found In Verified DB:')
                else :
                    statReport.report('GUA no found in Verified DB' )
                continue;
            else :
                statReport.report('google not return a address' )
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