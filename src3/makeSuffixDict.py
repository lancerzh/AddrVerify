'''
Created on Apr 5, 2016

@author: lancer
'''
import csv;

"""
all Secondary unit is a prefix
all street is a suffix
all geographic directional is a qualifier
"""

if __name__ == '__main__':
    dictFile = '../1.csv'
    with open(dictFile, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        last1 = ''
        last2 = ''
        for row in spamreader:
            #print row[0], row[1], row[2], row[3]
            print("suffixes['" + row[0] + "']=", end=' ')
            if row[1] != '' :
                last1 = row[1].strip();
                last2 = row[2].strip();
                last3 = row[3].upper().strip();
            print("('" + "','".join((last1, last2, last3)) + "')")
    
    pass