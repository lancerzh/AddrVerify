'''
Created on Mar 28, 2016

@author: lancer
'''
import verify_by_usps;
import csv;
import time;

workfor = 2000;
beginline = 1;
endline = beginline + workfor;

addressFile = '../billingnoverified.csv';
wordFreqDB = '../wordFrqDB.csv';
# addr1, addr2, city, states, postalCode
#indexs = (6,7,9,10,11); # for facilityaddress
indexs = (4, 5, 3, 2, 0); # for billingaddress

countEmpty = 0;
countForeign = 0;

totalError = 0;
beginTime = time.time();

verifiedFile = '../verified.csv';
nopassFile = '../noverified.csv';

if __name__ == '__main__':
    vf = open(verifiedFile, 'wb');
    nvf = open(nopassFile, 'wb');
    #nvf.write('' + '\n');
    with open(addressFile, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            if spamreader.line_num <= beginline:
                continue;
            if len(row) < max(indexs):
                break;
            
            lex = verify_by_usps.AddressLexical(row[indexs[0] - 1], row[indexs[1]  - 1]);
            #print lex.__str__()
            #addr = verify_by_usps.Address(lex.primary[0], ' '.join(lex.secondary), row[indexs[2]  - 1], row[indexs[3]  -1], row[indexs[4]  - 1]);
            addr = verify_by_usps.Address(lex.primary[0], '', row[indexs[2]  - 1], row[indexs[3]  -1], row[indexs[4]  - 1]);
            #print addr.__str__()
            #print spamreader.line_num, ': ', addr;
            if addr.isEmpty():
                print('')
                print('Empty:')
                print(', '.join(row));
                countEmpty += 1;
                continue;
            if addr.isForeign() :
                print('')
                print('Foreign:')
                print(', '.join(row));
                countForeign += 1;
                continue;
            (uspsAddr, msg) = verify_by_usps.reqUSPS(addr);
            if uspsAddr == None :
                totalError += 1;
                print('')
                print('Error:')
                print(spamreader.line_num, ': ', addr, 'Lex.secondary: ', ' '.join(lex.secondary));
                #print uspsAddr;
                #print msg
                nvf.write(addr.__str__() + ',' + str(spamreader.line_num) + '\n');
            else :
                print('.', spamreader.line_num, end=' ')
                vf.write(uspsAddr.getSortStr() + 
                         ',"' + ', '.join([row[indexs[0] - 1], row[indexs[1]  - 1], row[indexs[2]  - 1], row[indexs[3]  -1], row[indexs[4]  - 1]]) + 
                         '",' + str(spamreader.line_num) + '\n')
            if spamreader.line_num > endline :
                break;
            
        print('');
        print('cost: ', time.time() - beginTime);
        print('totalError:', totalError)
        print('countEmpty:', countEmpty)
        print('countForeign:', countForeign)
            
    csvfile.close();
    vf.close();
    nvf.close();
    pass