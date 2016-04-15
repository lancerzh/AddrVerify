#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on Apr 6, 2016

@author: lancer
'''

import csv;
from verify_by_usps import AddressLexical, Address
from collections import defaultdict
import time;

import operator;
import string
import re


addressFile = '/Users/lancer/workspace/npi/npidata_20050523-20160313.csv'
#indexs = (21, 29, 23, 24, 25);
indexs = (29, 30, 31, 32, 33, 34);

#addressFile = '../billingverified.csv'
#indexs = (4,5,3,2,0);

wordFreqDB = '../wordFreqDB.csv'



keyNotFound = 0;

wordUsage = defaultdict(int);

countComplexWords = defaultdict(int);

def isdoorplate(word):
    if word.isdigit():
        return True
    if re.sub(r"[^\w\s]", '', word).isdigit():
        return True;
    if re.match('^[A-Z]{0,1}-?[0-9]+$', word):
        return True;
    if re.match('^[0-9]+-?[A-Z]{0,1}$', word):
        return True;
    return False;

def check(word):
    word = word.strip(string.punctuation);
    if word == '' :
        return;
    if isdoorplate(word):
        return
    if word.isalnum():
        if word in wordUsage:
            wordUsage[word] += 1;
        else :
            wordUsage[word] = 1;
    else :
        #print '???>', word
        if word in countComplexWords:
            countComplexWords[word] += 1;
        else :
            countComplexWords[word] = 1;

def procPOBOX(addr):
    #print addr
    r1 = r"P[. ]*O[. ]*BOX\.? ?(.*)$";
    r2 = r"(.*) P[. ]*O[. ]*BOX\.? ?(.*)$";
    p1 = r"POST OFFICE BOX";
    p2 = r'MAILBOX'
    reObj = re.match(r1, addr);
    if reObj :
        return 'PO BOX ' + reObj.group(1);
    
    reObj = re.match(r2, addr);
    if reObj :
        return reObj.group(1) + ' PO BOX ' + reObj.group(2);
    
    if addr.find(p1) >= 0 :
        return addr.replace("POST OFFICE BOX", "PO BOX");
    #if addr.find(p2) >= 0 :
    #    return addr.replace("MAILBOX", "PO BOX");

    #print addr;
    return addr;

def procAddr(addr):
    standardPOBOXstr = 'PO BOX';
    addr = addr.strip().upper();
    if addr.find('BOX') > 0 :
        addr = procPOBOX(addr);
        addr = addr.replace(standardPOBOXstr, '');
        check(standardPOBOXstr)
    for w in addr.split() :
        check(w);
    

if __name__ == '__main__':
    workfor = 5000000;
    beginline = 1;
    endline = beginline + workfor;

    beginTime = time.time();
    with open(addressFile, 'r', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            if spamreader.line_num <= beginline:
                continue;
            if len(row) <= max(indexs):
                continue;
            businessAddr1 = row[indexs[0] - 1];
            practiceAddr1 = row[indexs[1] - 1];
            if spamreader.line_num < 100:
                print("businessAddr1:", businessAddr1, 'practiceAddr1:', practiceAddr1);
                
            if len(businessAddr1) > 0 :
                procAddr(businessAddr1);
            
            if len(practiceAddr1) > 0 :
                procAddr(practiceAddr1);
            
            if spamreader.line_num > endline :
                break;
            if spamreader.line_num % 100000 == 0 :
                print(spamreader.line_num, '... ...', 'cost: ', time.time() - beginTime);
            
        print('************************')
        
    fdt = open('../freqdict.csv', 'w');
    sorted_x = sorted(list(wordUsage.items()), key=lambda x:x[1])
    sorted_x.reverse();
    print('total countOfWords = ', len(sorted_x));
    a = sorted_x[0];
    print(a[0], a[1])
    for a in sorted_x:
        '''
        if a[1] > 1 :
            print a[0], a[1]
            '''
        fdt.write('"' + a[0] + '",' + str(a[1]) + '\n');
    fdt.close();
    '''
    for a1 in  wordUsage.items():
        print a1[0],
        print len(a1[0]);
    '''
    fdt = open('../freqdictByLength.csv', 'w');
    sorted_x = sorted(list(wordUsage.items()), key=lambda x:(len(x[0]), x[0]), reverse=True)
    sorted_x.reverse();
    a = sorted_x[0];
    print(a[0], a[1])
    for a in sorted_x:
        fdt.write('"' + a[0] + '",' + str(a[1]) + '\n');
    fdt.close();
    
    fdt = open('../freqComplexWords.csv', 'w',  encoding='utf-8');
    print('************************')
    sorted_x = sorted(list(countComplexWords.items()), key=lambda x:x[1])
    sorted_x.reverse();
    print('total countComplexWords = ', len(sorted_x));
    a = sorted_x[0];
    print(a[0], a[1])
    for a in sorted_x :
        
        if a[1] > 1 :
            print (a[0], a[1]);
            
        fdt.write('"' + a[0] + '",' + str(a[1]) + '\n');
    fdt.close();
    pass