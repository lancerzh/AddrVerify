'''
Created on Apr 12, 2016

@author: lancer
'''
import pymysql.cursors
import verify_by_usps

connection = None;

def getConnection():
    connection = pymysql.connect(host='localhost',
                     user='jms',
                     password='jms',
                     db='jms_npi',
                     charset='utf8',
                     cursorclass=pymysql.cursors.Cursor)
    return connection;

def insert(conn, addr, npiid, npitype, addrtype):
    sql = """insert into `npiaddress` 
            set
            oa1 = %s,
            oa2 = %s,
            oc = %s,
            os = %s,
            op5 = %s,
            op4 = %s,
            ont = %s,
            npiid = %s,
            npitype = %s,
            addrtype = %s,
            verified = '-'
            """
            
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (addr.addr1, addr.addr2, addr.city, addr.state, addr.zip5, addr.zip4, addr.nation, npiid, npitype, addrtype ));
        connection.commit();
    except :
        conn.close()
        conn = None

def createAddrFromRow(dbrow):
    vaddr = verify_by_usps.Address(dbrow[0], dbrow[1], dbrow[2], dbrow[3], dbrow[4] + dbrow[5]);
    oaddr = verify_by_usps.Address(dbrow[6], dbrow[7], dbrow[8], dbrow[9], dbrow[10] + dbrow[11], dbrow[12]);
    return vaddr, oaddr


def fetchBlank(npiid, howmany):

    # Connect to the database
    connection = getConnection();
    
    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = """SELECT *
            FROM `npiaddress` 
            WHERE `va1` = '' 
            and `va2` = ''
            and `vs` = ''
            and `vp5` = ''
            and npiid > %s
            limit 0, %s
            """
            
            cursor.execute(sql, (npiid, howmany));

            result = cursor.fetchall()

            
    finally:
        connection.close()
        connection = None
        
    return result;

if __name__ == '__main__':
    
    pass