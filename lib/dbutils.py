import pymysql
import time
import datetime
import inspect

from datetime import date

import dbconfig
from flutils import *

class MySQLUtil():

    def dbConnect(self): #,host,user,psw,db_name,charset,port
        self.db = pymysql.connect(host=dbconfig.host, 
            user=dbconfig.user, 
            password=dbconfig.psw, 
            db=dbconfig.db_name, charset='utf8', 
            port=dbconfig.port)
            
        logging.info(inspect.stack()[0][3] + ' Database opened ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
   
   
    def dbClose(self):
        self.db.close()
        logging.info(inspect.stack()[0][3] + ' Database closed ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
        

    
    def execSQL(self, sql):

        # logging.info(inspect.stack()[0][3] + ' execSQL ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            self.db.commit()
            cursor.close()
            return True  
        except Exception as e:
            self.db.rollback()
            logging.error(inspect.stack()[0][3] + ' execSQL failed ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S') + sql)
            logging.error(inspect.stack()[0][3] + ' execSQL failed ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S') + str(e))

            return False


    def execQuery(self, sql):
        
        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()
            return results
        except Exception as e:
            logging.error(inspect.stack()[0][3] + ' Search failed ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S') + str(e))
            return None

   
   
    def execOne(self, sql):
        
        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            results = cursor.fetchone()
            cursor.close()
            return results
        except Exception as e:
            logging.error(inspect.stack()[0][3] + ' Query String was ' + sql)
            logging.error(inspect.stack()[0][3] + ' Search failed ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S') + str(e))
            
            return None

#end class MySQLUtil



def checkDuplicates(mysql, sql):  
    
    result = mysql.execOne(sql)
    if result == None:  # empty tuple
        return None
    else:
#        logging.error(inspect.stack()[0][3] + ' Duplicate found. ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S') + ' ' + sql)
        return result[0]                   # returns value from the list
        




def check_start_end_dates(tablename, meter_no, days_offset=1):
    
#   Function finds the last record in the daabase table 'tablename'. If there is no record in the database, the function checks
#   the last_download date from the meters file and returns that

    sdate = datetime.datetime.today()
    
    mysql = MySQLUtil()
    mysql.dbConnect()
    
    sql1  = "SELECT `read_date` FROM `{0}` WHERE `meter_no` = '{1}' ORDER BY `read_date` DESC LIMIT 1".format(tablename, meter_no)
    sql2 = "SELECT `last_download` FROM `{0}` WHERE `meter_no` = '{1}' ORDER BY `last_download` DESC LIMIT 1".format("meters", meter_no)
    qdate = mysql.execQuery(sql1)
    
    if not qdate:   # i.e No records in tablename. First time the program has run for this meter - tuple is null
        qdate = mysql.execQuery(sql2) # look up last download in the meter table
        sdate = qdate[0]
        logging.info(inspect.stack()[0][3] + " No downloaded data yet. Using meters last_download of " + str(sdate[0]) + " " + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
    else:    
    #print ("qdate: {0} sdate: {1} sdate[0]: {2}".format(qdate, sdate, sdate[0]))
        sdate = qdate[0]
        logging.info(inspect.stack()[0][3] + " Resuming from last download record with offset of " + str(days_offset) + " days from " + str(sdate[0]) + " " + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
    mysql.dbClose()
    return (sdate[0] - datetime.timedelta(days=days_offset))



def getDuplicate(mysql, sql):  
    
    result = mysql.execOne(sql)
    if result == None:  # empty tuple
        return None
    else:
#        logging.error(inspect.stack()[0][3] + ' Duplicate found. ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S') + ' ' + sql)
        return result                   # returns value from the list
        


def lastID(mysql, tablename):
    
    sql = 'SELECT `id` FROM `{0}` ORDER BY `ID` DESC LIMIT 1'.format(tablename)
    result = mysql.execQuery(sql)
    last_id = [x[0] for x in result]  # extract list from tuple
    if not last_id:  # list is empty
        return 0
    else:
        return last_id[0]                   # returns value from the list



def updateMeter(mysql, meter_no):
    sql = "UPDATE `meters` SET `last_download` = '{0}' WHERE `meter_no` = '{1}'".format(datetime.datetime.now(), meter_no)
    result = mysql.execSQL(sql)
    return result

