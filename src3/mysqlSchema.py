'''
Created on Mar 30, 2016

@author: lancer
'''

import xml.dom.minidom


if __name__ == '__main__':
    dom = xml.dom.minidom.parse('../Test_1.22.9.0_FK.dbo.xml');
    #print dom.toprettyxml()
    tables = dom.getElementsByTagName('table');
    count = 0;
    ct = set();
    intct = set();
    for t in tables :
        v = t.getAttribute('name')
        
        if t.getAttribute('name') in ('Facility', 'FacilityAddress', 'Physician', 'BillingAddress', 'FacilityPhysicianAffl') :
            count += 1;
            print('CREATE TABLE', v, '(');
            columns = t.getElementsByTagName('column');
            for child in t.childNodes :
                #print child;
                #print child.__class__.__name__
                
                if isinstance(child, xml.dom.minidom.Element) and child.tagName == 'column' :
                    #print child.toprettyxml();
                    name = child.getAttribute('name')
                    size = child.getAttribute('size')
                    digits = child.getAttribute('digits')
                    columnType = child.getAttribute('type')
                    ct.add(columnType);
                    if columnType in ( 'int', 'decimal'):
                        intct.add(columnType + ':' + size);
                    #print name, size, digits, columnType;
                    print('    ', name, columnType, end=' ') 
                    if columnType in ('varchar', 'char') :
                        print('(', size, '),')
                    if columnType in ('decimal') :
                        print('(', size + ',' + digits, '),')
                    if columnType in ('int', 'datetime', 'date') :
                        print(',')
            print(');')
            pass
    print('total table:', count)
    print('column type set = ', ct)
    print('int column type = ', intct);