'''
Created on Apr 9, 2016

@author: lancer
'''
import unittest
import MySQLdb


class Test(unittest.TestCase):


    def testName(self):
        db=MySQLdb.connect(host="localhost",user="jms",passwd="jms",db="jms_npi")

        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()