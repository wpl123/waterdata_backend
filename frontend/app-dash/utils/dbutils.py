import pymysql
import time
import datetime

from datetime import date
from utils.flutils import *

class MySQLUtil():

    def dbConnect(self, host, user, psw, db_name, port):
        self.db = pymysql.connect(host=host, user=user, password=psw, db=db_name, charset='utf8', port=port)
        logging.info(' Database opened ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
   
   
    def dbClose(self):
        self.db.close()
        logging.info(' Database closed ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
        

    def execQuery(self, sql):

        # logging.info('execQuery ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()
            return results
        except:
#            logging.info('execQuery failed ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S') + sql)
            return None


    def execSQL(self, sql):

        logging.info('execSQL ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            self.db.commit()
            cursor.close()
            return True  
        except Exception as e:
            self.db.rollback()
            logging.error(' execSQL failed ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S') + sql)
            logging.error(' execSQL failed ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S') + str(e))

            return False

#end class MySQLUtil



def checkDuplicates(mysql, sql):
    
    result = mysql.execQuery(sql)
    if result == ():                    # empty tuple
        return None
    else:
        dup_id = [x[0] for x in result]  # extract list from tuple
        return dup_id[0]                 # returns value from the list



def check_start_end_dates(tablename, meter_no):
    
    mysql = MySQLUtil()
    mysql.dbConnect(host ='192.168.11.6', user = 'root', psw = 'water', db_name = 'waterdata', port=30000)
    
    sql = "SELECT `read_date` FROM `{0}` WHERE `meter_no` = '{1}' ORDER BY `read_date` DESC LIMIT 1".format(tablename, meter_no)
    qdate = mysql.execQuery(sql)  # returns a unique tuple
    sdate = qdate[0]
    #print ("qdate: {0} sdate: {1} sdate[0]: {2}".format(qdate, sdate, sdate[0]))

    mysql.dbClose()
    return sdate[0].strftime('%d/%m/%Y')       # extract date from the SQLtuple



def lastID(mysql, tablename):
    
    sql = 'SELECT `id` FROM `{0}` ORDER BY `ID` DESC LIMIT 1'.format(tablename)
    result = mysql.execQuery(sql)
    last_id = [x[0] for x in result]  # extract list from tuple
    return last_id[0]                   # returns value from the list



def updateMeter(mysql, meter_no):
    sql = "UPDATE `meters` SET `last_download` = '{0}' WHERE `meter_no` = '{1}'".format(datetime.datetime.now(), meter_no)
    result = mysql.execSQL(sql)
    return result

