import pymysql
import time
import datetime
import inspect

from datetime import date
from flutils import *

class MySQLUtil():

    def dbConnect(self, host, user, psw, db_name, port):
        self.db = pymysql.connect(host=host, user=user, password=psw, db=db_name, charset='utf8', port=port)
        logging.info(inspect.stack()[0][3] + ' Database opened ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
   
   
    def dbClose(self):
        self.db.close()
        logging.info(inspect.stack()[0][3] + ' Database closed ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
        

    
    def execSQL(self, sql):

        logging.info(inspect.stack()[0][3] + ' execSQL ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
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
        




def get_last_date(_mysql, _tablename, _meter_no, _format='%d/%m/%Y'):
    
#    mysql = MySQLUtil()
#    mysql.dbConnect(host ='192.168.11.6', user = 'root', psw = 'water', db_name = 'waterdata', port=30000)
    
    sql = "SELECT `read_date` FROM `{0}` WHERE `meter_no` = '{1}' ORDER BY `read_date` DESC LIMIT 1".format(_tablename, _meter_no)
    qdate = _mysql.execQuery(sql)  # returns a unique tuple
    sdate = qdate[0]
    #print ("qdate: {0} sdate: {1} sdate[0]: {2}".format(qdate, sdate, sdate[0]))
   
    return sdate[0].strftime(_format)       # extract date from the SQLtuple



def lastID(mysql, tablename):
    
    sql = 'SELECT `id` FROM `{0}` ORDER BY `ID` DESC LIMIT 1'.format(tablename)
    result = mysql.execQuery(sql)
    last_id = [x[0] for x in result]  # extract list from tuple
    return last_id[0]                   # returns value from the list



def updateMeter(mysql, meter_no):
    sql = "UPDATE `meters` SET `last_download` = '{0}' WHERE `meter_no` = '{1}'".format(datetime.datetime.now(), meter_no)
    result = mysql.execSQL(sql)
    return result

