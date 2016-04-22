'''
Created on Apr 18, 2016

@author: lancer
'''
import pymysql.cursors

def getConnection():
    connection = pymysql.connect(host='localhost',
                     user='jms',
                     password='jms',
                     db='jms_npi',
                     charset='utf8',
                     cursorclass=pymysql.cursors.Cursor)
    return connection;

def gatFacilityAddress(conn, ficilityId):
    result = []
    try:
        with conn.cursor() as cursor:
            sql = '''select fa.Address1, fa.Address2, fa.Address3, 
                     fa.city, fa.states, fa.postalcode, 
                     fa.county, fa.country 
                    from FacilityAddress fa 
                    where FacilityID = %s ;
            '''
            cursor.execute(sql, (ficilityId));
            result = cursor.fetchall()
    except :
        conn.close()
        conn = None
    return result;

def getFacility(conn, begin=0, limit=100):
    result = []
    try:
        with conn.cursor() as cursor:
            # Read a single record
            sql = """SELECT f.FacilityID,
                    f.TaxID, 
                    f.TaxIDType, 
                    f.`Status`, 
                    f.FacilityName, 
                    f.BillingAddrID,
                    f.NationalProviderID , 
                     ba.Address1, 
                     ba.Address2, 
                     ba.Address3, 
                     ba.city, ba.states, ba.postalcode, 
                     ba.county, ba.country,
                     fpac.c
                    FROM jms_npi.Facility f
                    left join BillingAddress ba
                    on f.BillingAddrID = ba.BillingAddrID, 
                        (
                        SELECT count(*) c, FacilityID 
                        FROM jms_npi.FacilityPhysicianAffl
                        group by FacilityID
                        ) fpac
                    where `status` = 'A'
                    and f.BillingAddrID <> 0
                    and f.FacilityName <> ''
                    and f.FacilityID = fpac.FacilityID
                    order by ba.states, ba.city, f.FacilityName
                    limit %s, %s
            """  
            '''and fpac.c <= 2'''
            
            cursor.execute(sql, (begin, limit));
            result = cursor.fetchall()

    except :
        conn.close()
        conn = None
    return result;