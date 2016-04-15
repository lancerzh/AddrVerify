'''
Created on Apr 9, 2016

@author: lancer
'''
import unittest
import npidb 
from USMailAddress import Address

class Test(unittest.TestCase):
    def testConn(self):
        conn = npidb.getConnection()
        self.assertIsNotNone(conn)
        pass
    def testSearchAddrVerified(self):
        conn = npidb.getConnection();
        
        anAddr = Address('2615 NE LOOP 286', '', 'PARIS', 'TX', '75460')
        r = npidb.searchAddrInVerified(conn, anAddr);
        self.assertTrue(len(r) > 0);
        ra = r[0]
        
        anAddr = Address("601 CHATHAM MEDICAL PARK","","ELKIN","NC","28621");
        r = npidb.searchAddrInVerified(conn, anAddr);
        self.assertTrue(len(r) == 0);
        print(ra)
        
    def testSearchAddrOrig(self):
        conn = npidb.getConnection();
        
        anAddr = Address('2615 NE LOOP 286', '', 'PARIS', 'TX', '75460')
        r = npidb.searchAddrInOrig(conn, anAddr);
        self.assertTrue(len(r) > 0);
        ra = r[0]
        
        anAddr = Address("601 CHATHAM MEDICAL PARK","","ELKIN","NC","28621");
        r = npidb.searchAddrInOrig(conn, anAddr);
        self.assertTrue(len(r) == 0);
        print(ra)

    def testnpidb(self):
        r = npidb.fetchBlank(npidb.getConnection(), '', 100);
        self.assertTrue(len(r) > 0);
        self.assertEqual(100, len(r));
        '''
        for row in r:
            va, od = npidb.createAddrFromRow(row)
            print (od)
            '''
            

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()