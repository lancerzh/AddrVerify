'''
Created on Apr 12, 2016

@author: lancer
'''
import pymysql
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

def searchAddrInVerified(conn, addr):
    result = []
    try:
        with conn.cursor() as cursor:
            # Read a single record
            sql = """SELECT *
            FROM `npiaddress` 
            WHERE verified = 'V'
            and `vp5` = %s
            and `vs` = %s
            and `vc` = %s
            """
            if len(addr.addr1) > 0 :  
                sql += " and `va1` = '" + addr.addr1  + "' ";
            if len(addr.addr2) > 0 : 
                sql += " and `va2` = '" + addr.addr2 + "' ";
            sql += ' limit 0, 10 '
            
            #print (sql)
            
            cursor.execute(sql, (addr.zip5, addr.state, addr.city));
            #print(cursor._last_executed)
            result = cursor.fetchall()

    except :
        conn.close()
        conn = None
    return result;

def searchAddrInOrig(conn, addr):
    result = []
    try:
        with conn.cursor() as cursor:
            # Read a single record
            sql = """SELECT *
            FROM `npiaddress` 
            WHERE `op5` = %s
            and `os` = %s
            and `oc` = %s
            and `oa1` = %s 
            and `oa2` = %s
            limit 0, 10
            """
            
            cursor.execute(sql, (addr.zip5, addr.state, addr.city, addr.addr1, addr.addr2));
            #print(cursor._last_executed)
            result = cursor.fetchall()

    except :
        conn.close()
        conn = None
    return result;

def fetchBlank(conn, npiid, howmany):

    
    try:
        with conn.cursor() as cursor:
            # Read a single record
            sql = """SELECT *
            FROM `npiaddress` 
            WHERE `va1` = '' 
            and `va2` = ''
            and `vs` = ''
            and `vp5` = ''
            and npiid >= %s
            limit 0, %s
            """
            
            cursor.execute(sql, (npiid, howmany));

            result = cursor.fetchall()

            
    except :
        conn.close()
        conn = None
        
    return result;

def searchNameByIds(conn, ids):
    result = []
    try:
        with conn.cursor() as cursor:
            # Read a single record
            sql = """SELECT distinct Provider_Organization_Name, NPI, Entity_Type_Code
                     FROM jms_npi.NPI_ORG
                    where Provider_Organization_Name <> ''
                    and NPI in ( %s )
                    ;
            """
            intList = ','.join(str(e) for e in ids)
            sql = sql % intList;
            
            cursor.execute(sql, ());
            print(cursor._last_executed)

            result = cursor.fetchall()

    except pymysql.InternalError as error :
        print('Got error {!r}, errno is {}'.format(error, error.args[0]))
        conn.close()
        conn = None
        
    return result;

def searchNameByMZSC(conn, ZSCList):
    result = []
    try:
        with conn.cursor() as cursor:
            # Read a single record
            sql1 = """select NPI,
                Provider_Organization_Name, 
                Provider_Other_Organization_Name,
                Provider_First_Line_Business_Mailing_Address, 
                Provider_Second_Line_Business_Mailing_Address,
                Provider_Business_Mailing_Address_City_Name,
                Provider_Business_Mailing_Address_State_Name,
                Provider_Business_Mailing_Address_Postal_Code,
                Provider_First_Line_Business_Practice_Location_Address, 
                Provider_Second_Line_Business_Practice_Location_Address,
                Provider_Business_Practice_Location_Address_City_Name,
                Provider_Business_Practice_Location_Address_State_Name,
                Provider_Business_Practice_Location_Address_Postal_Code,
                Last_Update_Date,
                Is_Sole_Proprietor
                from NPI_ORG
                where Entity_Type_Code = 2
                and ( """

            sql2Temp = """
                ( MAZ5 = '%s' 
                and Provider_Business_Mailing_Address_State_Name = '%s'
                and Provider_Business_Mailing_Address_City_Name = '%s' ) 
                or 
                ( PAZ5 = '%s'
                and Provider_Business_Practice_Location_Address_State_Name = '%s'
                and Provider_Business_Practice_Location_Address_City_Name = '%s' )
                """
                
            sql3 = """);"""
            sql2List = []
            for ezsc in ZSCList:
                sql2List.append( sql2Temp % (ezsc[0], ezsc[1], ezsc[2], ezsc[0], ezsc[1], ezsc[2]))
            sqlStr = sql1 + " or ".join(sql2List) + sql3;
            cursor.execute(sqlStr, ());
            #print(cursor._last_executed)

            result = cursor.fetchall()

    except pymysql.InternalError as error :
        print('Got error {!r}, errno is {}'.format(error, error.args[0]))
        conn.close()
        conn = None
        
    return result;

if __name__ == '__main__':
    
    pass