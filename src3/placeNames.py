'''
Created on Apr 7, 2016

@author: lancer
'''

allNameFile = '../AllNames_20160201.txt'
dictFileName = '../weball.txt';

placeNameWords = set();
linuxdict = set();

def readLinuxDict():
    if len(linuxdict) > 0 :
        return; 
    dictFile = open(dictFileName, 'rb');
    for line in dictFile :
        w = line.strip();
        if w.isalpha() == False :
            continue;
        if len(w) <= 1 :
            continue; 
        linuxdict.add(w.upper());
    dictFile.close();

def readGeoPlaceNameDict():
    if len(placeNameWords) > 0 :
        return; 
    readLinuxDict();
    pnfile = open(allNameFile, 'rb');
    i = 0;
    for line in pnfile:
        i += 1;
        fields = line.split('|')
        if len(fields) < 1:
            continue;
        name = fields[1].strip().upper();
        words = name.split();
        for w in words :
            if w.isalpha() == False :
                continue;
            if w in linuxdict :
                continue;
            if w in placeNameWords :
                continue;
            placeNameWords.add(w);

readLinuxDict()
readGeoPlaceNameDict();   
    

if __name__ == '__main__':
    print('linuxdict total items = ', len(linuxdict))
    print('placeNameWords total items = ', len(placeNameWords))