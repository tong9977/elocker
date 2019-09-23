import config
import MySQLdb
import config
from datetime import datetime
import random
import sms

def countLockerAvailable():
    db = MySQLdb.connect(host= config.dbhost, user=config.dbuser, passwd=config.dbpassword, db=config.dbname)
    cur = db.cursor()
    sql = "select * from tbLocker where LockerName= '{}' AND Active=true AND FingerprintTemplate IS NULL".format(config.lockerName)
    number_of_rows = cur.execute(sql)
    cur.close()
    db.close ()
    
    return number_of_rows

    
def reserveLockerByFingerprintTemplate(figerprintTemplate):
    db = MySQLdb.connect(host= config.dbhost, user=config.dbuser, passwd=config.dbpassword, db=config.dbname)
    cur = db.cursor()
    sql = "select LockerID from tbLocker where LockerName= '{}' AND Active=true AND FingerprintTemplate IS NULL".format(config.lockerName)

    number_of_rows = cur.execute(sql)
    if number_of_rows == 0:
        cur.close()
        db.close ()
        return -1
    else:
        result = cur.fetchone()
        lockerID = result[0]
        sqlupdate = "UPDATE tbLocker SET FingerprintTemplate = {}, StartTime=now() WHERE lockerID = {}".format(figerprintTemplate,lockerID)
        cur.execute(sqlupdate)
        db.commit()
        cur.close()
        db.close ()
        return lockerID

def releaseLockerByFingerprintTemplate(figerprintTemplate):
    db = MySQLdb.connect(host= config.dbhost, user=config.dbuser, passwd=config.dbpassword, db=config.dbname)
    cur = db.cursor()
    sql = "select LockerID,StartTime,TelNo from tbLocker where LockerName= '{}' AND FingerprintTemplate = {}".format(config.lockerName,figerprintTemplate)

    number_of_rows = cur.execute(sql)
    if number_of_rows == 0:
        cur.close()
        db.close ()
        return -1
    else:
        result = cur.fetchone()
        lockerID = result[0]
        startTime = result[1]
        telNo = result[2]
        sqlupdate = "UPDATE tbLocker SET FingerprintTemplate = NULL , StartTime= NULL WHERE lockerID = {}".format(lockerID)
        cur.execute(sqlupdate)
        
        sqlinsert = "INSERT INTO tbRecord (LockerID, FingerprintTemplate,StartTime,EndTime) VALUES (%s, %s,%s,now(),%s)"
        val = (int(lockerID),int(figerprintTemplate),startTime,telNo)
        cur.execute(sqlinsert, val)
        db.commit()
        cur.close()
        db.close ()
        return lockerID

def releaseLockerByLockerID(lockerId):
    db = MySQLdb.connect(host= config.dbhost, user=config.dbuser, passwd=config.dbpassword, db=config.dbname)
    cur = db.cursor()
    sql = "select LockerID,StartTime,FingerprintTemplate,TelNo from tbLocker where LockerName= '{}' AND LockerID = {}".format(config.lockerName,lockerId)

    number_of_rows = cur.execute(sql)
    if number_of_rows == 0:
        cur.close()
        db.close ()
        return -1
    else:
        result = cur.fetchone()
        lockerID = result[0]
        startTime = result[1]
        figerprintTemplate = result[2]
        telNo = result[3]
        #sqlupdate = "UPDATE tbLocker SET FingerprintTemplate = NULL , StartTime= NULL WHERE LockerID = {}".format(lockerID)
        sqlupdate = "UPDATE tbLocker SET FingerprintTemplate = NULL , StartTime= NULL, TelNo = NULL, OTP = NULL WHERE LockerID = {}".format(lockerID)
        cur.execute(sqlupdate)
        
        #sqlinsert = "INSERT INTO tbRecord (LockerID, FingerprintTemplate,StartTime,EndTime) VALUES (%s, %s,%s,now())"
        sqlinsert = "INSERT INTO tbRecord (LockerID, FingerprintTemplate,StartTime,EndTime, TelNo) VALUES (%s, %s,%s,now(),%s)"
        val = (int(lockerID),int(figerprintTemplate),startTime,telNo)
        cur.execute(sqlinsert, val)
        db.commit()
        cur.close()
        db.close ()
        return lockerID

def searchLockerByFingerprintTemplate(figerprintTemplate):
    db = MySQLdb.connect(host= config.dbhost, user=config.dbuser, passwd=config.dbpassword, db=config.dbname)
    cur = db.cursor()
    sql = "select LockerID from tbLocker where LockerName= '{}' AND FingerprintTemplate = {}".format(config.lockerName,figerprintTemplate)

    number_of_rows = cur.execute(sql)
    if number_of_rows == 0:
        cur.close()
        db.close ()
        return -1
    else:
        result = cur.fetchone()
        lockerID = result[0]
        cur.close()
        db.close ()
        return lockerID


def getBoxNoByLockerID(lockerId):
    db = MySQLdb.connect(host= config.dbhost, user=config.dbuser, passwd=config.dbpassword, db=config.dbname)
    cur = db.cursor()
    sql = "select BoxNo from tbLocker where LockerID = {} AND LockerName= '{}'".format(lockerId,config.lockerName)

    number_of_rows = cur.execute(sql)
    if number_of_rows == 0:
        cur.close()
        db.close ()
        return -1
    else:
        result = cur.fetchone()
        boxno = result[0]

        cur.close()
        db.close ()
        return boxno

def getfingerprintTemplateByLockerID(lockerId):
    db = MySQLdb.connect(host= config.dbhost, user=config.dbuser, passwd=config.dbpassword, db=config.dbname)
    cur = db.cursor()
    sql = "select FingerprintTemplate from tbLocker where LockerID = {} AND LockerName= '{}' AND FingerprintTemplate IS NOT NULL".format(lockerId,config.lockerName)

    number_of_rows = cur.execute(sql)
    if number_of_rows == 0:
        cur.close()
        db.close ()
        return -1
    else:
        result = cur.fetchone()
        fingerprintTemplate = result[0]

        cur.close()
        db.close ()
        return fingerprintTemplate














def checkTelephoneNumber(telNo):
    #Check
    if len(telNo) !=  10:
        return -1
    
    db = MySQLdb.connect(host= config.dbhost, user=config.dbuser, passwd=config.dbpassword, db=config.dbname)
    cur = db.cursor()
    sql = "select LockerID from tbLocker where LockerName= '{}' AND Active=true AND TelNo = '{}'".format(config.lockerName, telNo)

    number_of_rows = cur.execute(sql)
    if number_of_rows > 0:
        cur.close()
        db.close ()
        return -1
    else:
        cur.close()
        db.close ()
        return 1
    
def checkTelephoneNumberForReleaseLocker(telNo):
    #Check
    if len(telNo) !=  10:
        return -1
    
    db = MySQLdb.connect(host= config.dbhost, user=config.dbuser, passwd=config.dbpassword, db=config.dbname)
    cur = db.cursor()
    sql = "select LockerID from tbLocker where LockerName= '{}' AND Active=true AND TelNo = '{}'".format(config.lockerName, telNo)

    number_of_rows = cur.execute(sql)
    if number_of_rows > 0:
        otp = random.randint(100000,999999)
        
        result = cur.fetchone()
        lockerID = result[0]
        sqlupdate = "UPDATE tbLocker SET OTP = {} WHERE lockerID = {}".format(otp,lockerID)
        cur.execute(sqlupdate)
        db.commit()
        
        cur.close()
        db.close ()
        
        sms.sendOTP(str(telNo),str(otp))
                
        return otp
    else:
        cur.close()
        db.close ()
        return -1

def reserveLockerByFingerprintTemplateAndTelNo(figerprintTemplate, telNo):
    db = MySQLdb.connect(host= config.dbhost, user=config.dbuser, passwd=config.dbpassword, db=config.dbname)
    cur = db.cursor()
    sql = "select LockerID from tbLocker where LockerName= '{}' AND Active=true AND FingerprintTemplate IS NULL".format(config.lockerName)

    number_of_rows = cur.execute(sql)
    if number_of_rows == 0:
        cur.close()
        db.close ()
        return -1
    else:
        otp = random.randint(100000,999999)
        
        result = cur.fetchone()
        lockerID = result[0]
        sqlupdate = "UPDATE tbLocker SET FingerprintTemplate = {}, StartTime=now(), TelNo = '{}', OTP = {} WHERE lockerID = {}".format(figerprintTemplate, telNo, otp,lockerID)
        cur.execute(sqlupdate)
        db.commit()
        cur.close()
        db.close ()
        return lockerID


def releaseLockerByOTP(telNo, OTP):
    db = MySQLdb.connect(host= config.dbhost, user=config.dbuser, passwd=config.dbpassword, db=config.dbname)
    cur = db.cursor()
    sql = "select LockerID,StartTime,FingerprintTemplate,TelNo,OTP from tbLocker where LockerName= '{}' AND TelNo = '{}' AND OTP = '{}'".format(config.lockerName,telNo, OTP)

    number_of_rows = cur.execute(sql)
    if number_of_rows == 0:
        cur.close()
        db.close ()
        return -1
    else:
        result = cur.fetchone()
        lockerID = result[0]
        startTime = result[1]
        #figerprintTemplate = result[2]
        #sqlupdate = "UPDATE tbLocker SET FingerprintTemplate = NULL , StartTime= NULL, TelNo = NULL, OTP = NULL WHERE LockerID = {}".format(lockerID)
        #cur.execute(sqlupdate)
        
        #sqlinsert = "INSERT INTO tbRecord (LockerID, FingerprintTemplate,StartTime,EndTime,TelNo) VALUES (%s, %s,%s,now(), %s)"
        #val = (int(lockerID),int(figerprintTemplate),startTime, telNo)
        #cur.execute(sqlinsert, val)
        #db.commit()
        cur.close()
        db.close ()
        return lockerID

