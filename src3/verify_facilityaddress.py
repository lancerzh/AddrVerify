'''
Created on Mar 28, 2016

@author: lancer
'''
import verify_by_usps;
import USMailAddress
import csv;
import time;

workfor = 10000;
beginline = 1;
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

if __name__ == '__main__':
    vf = open(verifiedFile, 'wb');
    nvf = open(nopassFile, 'wb');
    #nvf.write('' + '\n');
    with open(addressFile, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            if spamreader.line_num <= beginline:
                continue;
            #print row[indexOfZip - 1], row[indexOfState -1], row[indexOfCity - 1], row[indexOfAddr2 - 1], row[indexOfAddr1 - 1]
            addr = USMailAddress.Address(row[indexs[0] - 1], row[indexs[1]  - 1], row[indexs[2]  - 1], row[indexs[3]  -1], row[indexs[4]  - 1]);
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
            (uspsAddr, msg, distance) = verify_by_usps.reqUSPS(addr);
            if uspsAddr == None :
                totalError += 1;
                print('')
                print('Error:')
                print(spamreader.line_num, ': ', addr);
                #print uspsAddr;
                print(msg)
                nvf.write(addr.__str__() + ',' + str(spamreader.line_num) + '\n');
            else :
                print('.', spamreader.line_num, end=' ')
                '''
                vf.write(uspsAddr.getSortStr() + 
                         ',"' + ', '.join([row[indexs[0] - 1], row[indexs[1]  - 1], row[indexs[2]  - 1], row[indexs[3]  -1], row[indexs[4]  - 1]])
                          + '",' + ','.join(distance) 
                          + ','  + str(spamreader.line_num) + '\n')
                '''

                distance.reverse();

                vf.write(uspsAddr.getSortStr() + ', ' 
                         + addr.getSortStr() 
                         + ',' + ','.join(str(x) for x in distance)
                         + '\n');
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