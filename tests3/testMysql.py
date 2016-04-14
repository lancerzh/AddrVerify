'''
Created on Apr 9, 2016

@author: lancer
'''
import unittest
import npidb as db

class Test(unittest.TestCase):
    def testConn(self):
        conn = db.getConnection()
        self.assertIsNotNone(conn)
        print (conn)
        pass
    
'''
    def testnpidb(self):
        r = npidb.fetchBlank('', 100);
        self.assertEqual(100, len(r));
        for row in r:
            va, od = npidb.createAddrFromRow(row)
            print (od)
            '''

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()