
import pymysql
import pandas as pd
import os, glob, datetime, csv
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
    




def rainfallFormat(mysql, meter_no, downloads_dir, uploads_dir):
    
    logging.info(' Data format started ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))

    localdate = datetime.datetime.now().strftime('%Y-%m-%d')
    
    ldate = (datetime.datetime.today() - timedelta(days=1)).strftime('%Y%m%d')
    files = glob.glob(downloads_dir + meter_no + '*') #e.g.  /home/admin/dockers/waterdata_backend/data/downloads/54151.*

    if files == []:
        return None

    formatted_csvfile = uploads_dir + 'fmt_' + meter_no + '_' + ldate + '.csv'

    df1 = pd.concat([pd.read_csv(fp, skiprows=[1,2,35,36]).assign(filename=os.path.basename(fp)) for fp in files])
    
    #print(df1)
    # initialise variables
    
    mid = 0
    j = 0
    rf_read1 = 0.0
    DY_READ1 = 1
    QL_READ1 = "N"
    comments = 'Automated Load'
    creation_date = localdate
    yr = 0
    fields = []
    df11 = pd.DataFrame(columns=['read_date','rf_read1','dy_read1','ql_read1','comments','creation_date']) 

    with open(formatted_csvfile, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile,dialect='excel')

        for i in range(1,32):               #read the rows i.e. day
            
            search_year = re.findall(r'_[12][0-9][0-9][0-9]_',df1.iloc[i,12])
            yr = search_year[0].replace('_','') # get the year of record        
            
            for c in range(1,13):   #read the columns i.e. month

                if pd.isna(df1.iloc[(i - 1),(c - 1)]) == True:   # Skip nans
                    continue

                if checkDate(yr,str((c)),str(i)) == False:   #strip off bad dates e.g. 31.02.2020
                    logging.info(' Skipping bad loop date ' + str(yr) + '-' + str(c) + '-' + str(i))
                    continue

                read_dte = datetime.datetime(int(yr),c,i).strftime('%Y-%m-%d')
                rf = df1.iloc[(i - 1),(c - 1)]              # columns = date counters - 1

                df11.loc[j] = [read_dte,rf,DY_READ1,QL_READ1,comments,creation_date] 
                # print(read_dte,rf,QL_READ1,comments,creation_date)
                j = j + 1
        df11 = df11.sort_values(by=['read_date'],axis=0)
#        print(df11)
       
        mid = mid + 1

        for i in range(len(df11)):
            
            row = [mid,meter_no,df11.iloc[i,0],df11.iloc[i,1], df11.iloc[i,2],df11.iloc[i,3],df11.iloc[i,4],df11.iloc[i,5]]

            writer.writerow(map(lambda x: x, row))

    logging.info(' Data format ended ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
    return(formatted_csvfile)




def loadFormatted(mysql, meter_no, downloads_dir, uploads_dir, formatted_csvfile):

    logging.info(' Data load started ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
    
    df2 = pd.read_csv(formatted_csvfile, index_col=False, header=None, skiprows=2,engine='python')

    i = 0
        
#    with open(formatted_csvfile, 'r', newline='') as csvfile:
        
    for i in range(len(df2)):
        
        sql2 = ('''SELECT * FROM `rainfall` WHERE `meter_no` = '{0}' AND `read_date` = {1}''').format(df2.iloc[i,1], df2.iloc[i,2])
        dup_id = checkDuplicates(mysql, sql2)      # check for duplicates  
        
        if dup_id == None:
            df2.iloc[i,0] = lastID(mysql, 'rainfall') + 1

#            print(df2.iloc[i,0], df2.iloc[i,1], df2.iloc[i,2], df2.iloc[i,3],df2.iloc[i,4],df2.iloc[i,5],df2.iloc[i,6],df2.iloc[i,7])
            sql3 = (''' INSERT 
                        INTO `rainfall` (`id`, `meter_no`, `read_date`, 
                                `rf_read1`, `dy_read1`, `ql_read1`, 
                                `comments`, `creation_date`)VALUES ({0}, '{1}', '{2}', {3}, {4}, '{5}', '{6}', '{7}')
                        ''' ).format(df2.iloc[i,0], df2.iloc[i,1], df2.iloc[i,2], df2.iloc[i,3],df2.iloc[i,4],df2.iloc[i,5],df2.iloc[i,6],df2.iloc[i,7])
            
            result2 = mysql.execSQL(sql3)          # insert row
            if result2 == False:
                logging.error(' Insert failed meter_no: {0} date: {1} {2} '.format(df2.iloc[i,1],df2.iloc[i,2],datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')))
        else:
            logging.info(' Skipping duplicate id:' + str(dup_id) + " meter_no:" + df2.iloc[i,1] + " date:" + str(df2.iloc[i,2]) + " " + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
                
    return result2




def rainfallLoad(meter_no, downloads_dir, uploads_dir, logs_dir):

    setupLogging(meter_no, logs_dir)
    
    mysql = MySQLUtil()
    mysql.dbConnect(host ='192.168.11.6', user = 'root', psw = 'water', db_name = 'waterdata', port=30000)
    
    formatted_csvfile = rainfallFormat(mysql, meter_no, downloads_dir, uploads_dir)
    
    if formatted_csvfile != None:
        
        rf_load = loadFormatted(mysql, meter_no, downloads_dir, uploads_dir, formatted_csvfile)
        
        if rf_load == True:
            upd_meter = updateMeter(mysql, meter_no)     # update meter record with the read date

            download_hist = downloads_dir + 'download_hist'
            upload_hist   = uploads_dir + 'upload_hist'
            download_file = downloads_dir + meter_no + '*'
            upload_file   = formatted_csvfile
            move_upload   = moveFile(upload_file, upload_hist) # move formatted file and uploaded file to a new directory download_hist and upload_hist subdirectory
    else:
        logging.error('No download file for ' + meter_no + ' ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))

    mysql.dbClose()

