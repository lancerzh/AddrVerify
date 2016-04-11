'''
Created on Apr 5, 2016

@author: lancer
'''
import csv;
from verify_by_usps import AddressLexical, Address

#addressFile = '/Users/lancer/workspace/npi/npi1000.csv'
#indexs = (21, 22, 23, 24, 25);
addressFile = '../billingaddress.csv'
indexs = (5,6,9, 11, 8);

workfor = 10;
beginline = 1;
endline = beginline + workfor;

keyNotFound = 0;


if __name__ == '__main__':
    with open(addressFile, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            if spamreader.line_num <= beginline:
                continue;
            
            addr1 = row[indexs[0] - 1];
            addr2 = row[indexs[1]  - 1];
            #print
            #print addr1
            #print addr2
            lex = AddressLexical(addr1, addr2);

            print(addr1, addr2)
            #print lex
            print('lex.primary:', lex.primary)
            print('lex.secondary:', lex.secondary)
            if spamreader.line_num > endline :
                break;
            print()
        print("keyNotFound: ", keyNotFound)
    pass