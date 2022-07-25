
import pymysql
import pandas as pd
import os, glob, inspect
import datetime, csv
import logging
import re

from datetime import date, timedelta
from dateutil.parser import parse

from dbutils import *
from flutils import *


def checkDate(y,m,d):
    # print (y, m, d)
    dte = '-'.join((y, m, d))

    if dte:
        try:
            parse(dte)
            return True
        except:
            return False
    return False

# 2021-08-14T23:00:00Z
def normalizeDate(d):
    return d[0:10]


def rainfallFormat(mysql, meter_no, downloads_dir, uploads_dir):
    
    logging.info(inspect.stack()[0][3] + ' Data format started ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))

    localdate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    ldate = (datetime.datetime.today() - timedelta(days=1)).strftime('%Y%m%d')
    files = glob.glob(downloads_dir + meter_no + '*') #e.g.  /home/admin/dockers/waterdata_backend/data/downloads/54151.*

    if files == []:
        df2 = pd.DataFrame()
        return df2

    df1 = pd.concat([pd.read_csv(fp).assign(filename=os.path.basename(fp)) for fp in files])
    
    # initialise variables
    
    mid = 0
    j = 0
    rf_read1 = 0.0
    DY_READ1 = 1
    QL_READ1 = "N"
    comments = 'Automated Load'
    creation_date = localdate
    fields = []
    rows = []

#    ftp data

#IndexNo,SensorType,SensorDataType,SiteIdType,SiteId,ObservationTimestamp,RealValue,Unit,SensorParam1,SensorParam2,Quality,Comment
#199,RN,7,SSR,054021-1,2021-08-14T23:00:00Z,0,mm,,86400,3,
#200,RN,7,SSR,054021-1,2021-08-15T23:00:00Z,0,mm,,86400,3,

    for i in range(len(df1)):
       
        read_date = normalizeDate(df1.iloc[i, 5])
        rf_read1 = df1.iloc[i, 6]
        dy_read1 = DY_READ1
        ql_read1 = QL_READ1
        mn = df1.iloc[i, 4]
        
        fields = [mid,mn[:12],read_date,rf_read1,dy_read1,ql_read1,comments,creation_date]

        rows.append(fields)

    df2 = pd.DataFrame(rows,columns=['id','meter_no','read_date','rf_read1','dy_read1','ql_read1','comments','creation_date'])
    logging.info(inspect.stack()[0][3] + ' Data format ended ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
    return(df2)



def loadFormatted(mysql, meter_no, df):

    logging.info(inspect.stack()[0][3] + ' Data load started ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
    
    i = 0
        
#    with open(formatted_csvfile, 'r', newline='') as csvfile:
        
    for i in range(len(df)):
        
        sql2 = ('''SELECT `id` FROM `rainfall` WHERE `meter_no` = '{0}' AND `read_date` = '{1}' ''').format(df.iloc[i,1], df.iloc[i,2])
        dup_id = checkDuplicates(mysql, sql2)      # check for duplicates  
        
        if dup_id == None:
            df.iloc[i,0] = lastID(mysql, 'rainfall') + 1

#            print(df2.iloc[i,0], df2.iloc[i,1], df2.iloc[i,2], df2.iloc[i,3],df2.iloc[i,4],df2.iloc[i,5],df2.iloc[i,6],df2.iloc[i,7])
            sql3 = (''' INSERT 
                        INTO `rainfall` (`id`, `meter_no`, `read_date`, 
                                `rf_read1`, `dy_read1`, `ql_read1`, 
                                `comments`, `creation_date`)VALUES ({0}, '{1}', '{2}', {3}, {4}, '{5}', '{6}', '{7}')
                        ''' ).format(df.iloc[i,0], df.iloc[i,1], df.iloc[i,2], df.iloc[i,3],df.iloc[i,4],df.iloc[i,5],df.iloc[i,6],df.iloc[i,7])
            
            result2 = mysql.execSQL(sql3)          # insert row
            if result2 == False:
                logging.error(inspect.stack()[0][3] + ' Insert failed meter_no: {0} date: {1} {2} '.format(df.iloc[i,1],df.iloc[i,2],datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')))
        else:
            logging.info(inspect.stack()[0][3] + ' Skipping duplicate id ' + str(dup_id) + ' for meter_no: ' + df.iloc[i,1] + ' date: ' + str(df.iloc[i,2]) + " " + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
            result2 = False    
    return result2


# Mt Kaputar http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=136&p_display_type=dailyDataFile&p_startYear=&p_c=&p_stn_num=054151
# Mt Lindsay http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=136&p_display_type=dailyDataFile&p_startYear=&p_c=&p_stn_num=054021

def rainfallLoad(meter_no, params, downloads_dir, uploads_dir, logs_dir):

    setupLogging(meter_no, logs_dir)
    
    mysql = MySQLUtil()
    mysql.dbConnect()
    
    df_formatted = rainfallFormat(mysql, meter_no, downloads_dir, uploads_dir)
    
    if df_formatted.empty == False: #not empty
        
        rf_load = loadFormatted(mysql, meter_no, df_formatted)
        
        if rf_load == True:
            upd_meter = updateMeter(mysql, meter_no)     # update meter record with the read date

        download_hist = downloads_dir + 'download_hist'
        download_file = downloads_dir + params
        move_download = moveFile(download_file, download_hist)

#        if meter_no == '054021-1':#TODO: Fix hard coding of last rainfall meter check before moving files
        upload_hist   = uploads_dir + 'upload_hist'
        upload_file   = downloads_dir + meter_no + '*'  
        move_upload   = moveFile(upload_file, upload_hist) # move formatted file and uploaded file to a new directory download_hist and upload_hist subdirectory
    else:
        logging.error(inspect.stack()[0][3] + ' No download file for ' + meter_no + ' ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))

    mysql.dbClose()

