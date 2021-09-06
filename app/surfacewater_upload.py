
import pymysql
import pandas as pd
import os, glob, datetime, csv
import logging
import inspect


from datetime import date, timedelta
from dbutils import *
from flutils import *

    



def normalize_sw_Date(d):
    return '-'.join(((d[15:19]), d[12:14], d[9:11]))




def surfacewaterFormat(mysql, meter_no, downloads_dir, uploads_dir):
    
    logging.info(inspect.stack()[0][3] + ' Data format started ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))

    localdate = datetime.datetime.now().strftime('%Y-%m-%d')
   
    ldate = (datetime.datetime.today() - timedelta(days=1)).strftime('%Y%m%d')
    files = glob.glob(downloads_dir + meter_no + '*') #e.g.  /home/admin/dockers/waterdata_frontend/data/downloads/GW967137.1.1.*

    if files == []:
        return None

    formatted_csvfile = uploads_dir + 'fmt_' + meter_no + '_' + ldate + '.csv'
    df1 = pd.concat([pd.read_csv(fp, index_col=False, header=None, skiprows=[0], usecols=[0,1,2,3,4,5], \
        engine='python').assign(meter_no=os.path.basename(fp)) for fp in files])

     
    df1.fillna(value=0,inplace=True)
    df1.round({'3' : 2, '5' : 2, '7' : 2})
    
    # initialise variables
    
    # mid = lastID(mysql, 'surfacewater')
    mid = 0
    mn = ''
    sl_read1 = 0.0
    ql_read1 = 0
    sl_read2 = 0.0
    ql_read2 = 0
    sl_read3 = 0.0
    ql_read3 = 0
    comments='Automated Load'
    creation_date = localdate
    fields = []

    with open(formatted_csvfile, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile,dialect='excel')
        
        for i in range(len(df1)):
            
            if df1.iloc[i,2] == " ":    # skip blank lines
                continue

            read_date = normalize_sw_Date(df1.iloc[i, 0])
            sl_read1 = df1.iloc[i, 1]
            ql_read1 = df1.iloc[i, 2]
            sl_read2 = df1.iloc[i, 3]
            ql_read2 = df1.iloc[i, 4]
            mn = df1.iloc[i, 6]
            # mid = mid + 1

            if ql_read1 != '255':   # skip records with quality of "no data"
                fields = [mid,mn[:-13],"'" + read_date + "'",sl_read1,ql_read1,sl_read2,ql_read2,sl_read3,ql_read3,comments,"'" + creation_date + "'"]
                writer.writerow(map(lambda x: x, fields))
            else:
                logging.info(inspect.stack()[0][3] + ' Skipping record with no data for ' + read_date + ' at ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))

    logging.info(inspect.stack()[0][3] + ' Data format of ' + formatted_csvfile + ' ended ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
    return(formatted_csvfile)


def loadFormatted(mysql, meter_no, downloads_dir, uploads_dir, formatted_csvfile):

    logging.info(inspect.stack()[0][3] + ' Data load started ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
    
    df2 = pd.read_csv(formatted_csvfile, index_col=False, header=None, engine='python')

    i = 0
    with open(formatted_csvfile, 'r', newline='') as csvfile:
        
        for i in range(len(df2)):
            
            sql2 = ('''SELECT * FROM `surfacewater` WHERE `meter_no` = '{0}' AND `read_date` = {1}''').format(df2.iloc[i,1], df2.iloc[i,2])
            dup_id = checkDuplicates(mysql, sql2)      # check for duplicates
            
            if dup_id == None:
                df2.iloc[i,0] = lastID(mysql, 'surfacewater') + 1

                sql3 = (''' INSERT 
                        INTO `surfacewater` (`id`, `meter_no`, `read_date`, 
                                `sl_read1`, `ql_read1`, `sl_read2`, `ql_read2`, 
                                `sl_read3`, `ql_read3`, `comments`, `creation_date`)
                        VALUES ({0}, '{1}', {2}, {3}, {4}, {5}, {6}, {7}, {8}, '{9}', {10})
                        ''' ).format(df2.iloc[i,0], df2.iloc[i,1], df2.iloc[i,2], df2.iloc[i,3],df2.iloc[i,4],
                        df2.iloc[i,5],df2.iloc[i,6],df2.iloc[i,7],df2.iloc[i,8],df2.iloc[i,9],df2.iloc[i,10]) 

#INTO `surfacewater` (`id`, `meter_no`, `read_date`, 
#                                `sl_read1`, `ql_read1`, `sl_read2`, `ql_read2`, 
#                                `sl_read3`, `ql_read3`, `comments`, `creation_date`)
#                        VALUES (16849, '419051', '1975-07-15',  , 255,  , 255, 0.0, 0, 'Automated Load', '2021-09-01')
#
# You have an error in your SQL syntax; check the manual that corresponds to your MariaDB server version for the right 
# syntax to use near ' 255,  , 255, 0.0, 0, 'Automated Load', '2021-09-01')' at line 5

                result2 = mysql.execSQL(sql3)          # insert row
                if result2 == False:
                    logging.error(inspect.stack()[0][3] + ' Insert failed meter_no:' + df2.iloc[i,1] + " date:" + df2.iloc[i,2] + " " + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
            else:
                logging.info(inspect.stack()[0][3] + ' Skipping duplicate id:' + str(dup_id) + " meter_no:" + str(df2.iloc[i,1]) + " date:" + str(df2.iloc[i,2]) + " " + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
                
    return





def surfacewaterLoad(meter_no, downloads_dir, uploads_dir, logs_dir):
    
    
    setupLogging(meter_no, logs_dir)
    
    mysql = MySQLUtil()
    mysql.dbConnect(host ='192.168.11.6', user = 'root', psw = 'water', db_name = 'waterdata', port=30000)
    
    
    formatted_csvfile = surfacewaterFormat(mysql, meter_no, downloads_dir, uploads_dir)
    
    if formatted_csvfile != None:
        sw_load = loadFormatted(mysql, meter_no, downloads_dir, uploads_dir, formatted_csvfile)
        upd_meter = updateMeter(mysql, meter_no)     # update meter record with the read date
        
        download_hist = downloads_dir + 'download_hist'
        upload_hist   = uploads_dir + 'upload_hist'
        download_file = downloads_dir + meter_no + '*'
        upload_file   = formatted_csvfile
    
        move_download = moveFile(download_file, download_hist) # move formatted file and uploaded file to a new directory download_hist and upload_hist subdirectory
        move_upload   = moveFile(upload_file, upload_hist) # move formatted file and uploaded file to a new directory download_hist and upload_hist subdirectory
    else:
        logging.error(inspect.stack()[0][3] + ' No formated csvfile for ' + meter_no + ' ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))

    mysql.dbClose()

