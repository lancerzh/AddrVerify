'''
Created on Apr 7, 2016

@author: lancer
'''
import csv;
import makeSuffixDict;
import placeNames;

addressFile = '../freqdict.csv'



if __name__ == '__main__':

    
    wordMissCount = 0;
    wordMissCountO100 = 0;
    wordNotAlpha = 0;
    with open(addressFile, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            word = row[0];
            freq = int(row[1]);
            if word.isalpha() == False :
                wordNotAlpha += 1;
                continue;
            
            if word in makeSuffixDict.prefixes:
                continue;
            if word in makeSuffixDict.suffixes:
                continue;
            if word in makeSuffixDict.qualifiers:
                continue;
            
            if word in placeNames.linuxdict :
                continue;
            
            if word in placeNames.placeNameWords :
                continue;

            wordMissCount += 1;
            if freq >= 100 :
                wordMissCountO100 += 1;
                print(word, freq);
            pass
        print('wordMissCount = ', wordMissCount);
        print('wordMissCount Over 100 = ', wordMissCountO100);
        print('wordNotAlpha = ', wordNotAlpha);