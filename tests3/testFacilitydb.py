'''
Created on Apr 18, 2016

@author: lancer
'''
import unittest
import facilitydb
import npidb


class Test(unittest.TestCase):


    def testGetFacility(self):
        print('getFacility');
        conn = facilitydb.getConnection()
        facilityTable = facilitydb.getFacility(conn, 10)
        for record in facilityTable:
            print (record);
        conn.close();
        
        
    def testIds(self):
        print('testIds');
        conn = facilitydb.getConnection()
        ids = ( 1013951813,1033183835,1083652192,1194768226,1245205533,1407824063,1750310199,1891769683,1891892741,1932295516 )
        facilityTable = npidb.searchNameByIds(conn, ids)
        for record in facilityTable:
            print (record);
        conn.close();


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()