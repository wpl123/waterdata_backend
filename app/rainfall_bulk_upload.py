# INSTRUCTIONS
#
# Download the csv file from;
#   1. http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=136&p_display_type=dailyDataFile&p_startYear=&p_c=&p_stn_num=054151
#   2. http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=136&p_display_type=dailyDataFile&p_startYear=&p_c=&p_stn_num=054021
# Move csv files to data/bulk_load directory
# Edit the lines in main to contain the right csv file and correct meter
# e.g.
#   meter_no = "054151-2"                           #  "054021-1" 
#   csvfile = download_dir + "IDCJAC0009_054151_2022_Data.csv"   
#
# Run this bulk loader script
# move the csv file to bulk_load_hist directory
#
# check rainfall table using adminer


# BOM std rain gauge csv file

# Product code	Bureau of Meteorology station number	Year	Month	Day	Rainfall amount (millimetres)	Period over which rainfall was measured (days)	Quality

#1. import
#2. read in csv to df
# load df into database

import pymysql
import pandas as pd
import numpy as np
import sys, os, glob, inspect
import datetime, csv
import logging
import re

#https://stackoverflow.com/questions/1260792/import-a-file-from-a-subdirectory#%E2%80%A6
sys.path.extend([f'./{name}' for name in os.listdir(".") if os.path.isdir(name)])

from datetime import date, timedelta
from dateutil.parser import parse

from dbutils import *
from flutils import *


def normalizeDate(y,m,d):
   
    return '-'.join((y,m,d))


def rainfall_bulk_load(mysql, meter_no, formatted_csvfile):

    DY_READ1 = 1
    QL_READ1 = "N"
    comments = 'Bulk Load'
    localdate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    creation_date = localdate
    
    logging.info(' Data load started ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
    
    df = pd.read_csv(formatted_csvfile, index_col=False, header=0, na_values="NaN", engine='python')
    df = df.dropna()      #remove records that are NaN
   
    print(df)
   

    i = 0
    with open(formatted_csvfile, 'r', newline='') as csvfile:
        
        for i in range(len(df)):

            
            date_string = normalizeDate(str(df.iloc[i,2]),str(df.iloc[i,3]),str(df.iloc[i,4]))
            # read_date = datetime.date(date_string,'%Y-%m-%d')
            
            sql2 = ('''SELECT id FROM `rainfall` WHERE `meter_no` = '{0}' AND `read_date` = {1}''').format(meter_no, date_string)
            dup_id = checkDuplicates(mysql, sql2)      # check for duplicates
            
            if dup_id == None:
                mid = lastID(mysql, 'rainfall') + 1

                sql3 = (''' INSERT 
                        INTO `rainfall` (`id`, `meter_no`, `read_date`, 
                                `rf_read1`, `dy_read1`, `ql_read1`, `comments`, `creation_date`)
                        VALUES ({0}, '{1}', '{2}', {3}, {4}, '{5}', '{6}', '{7}')
                        ''' ).format(mid, meter_no, date_string, df.iloc[i,5],DY_READ1,QL_READ1,comments,creation_date)
    
                result2 = mysql.execSQL(sql3)          # insert row
                if result2 == False:
                    logging.error(' Insert failed meter_no:' + meter_no + " date:" + date_string + " " + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
            else:
                logging.info(' Skipping duplicate id:' + str(dup_id) + " meter_no:" + meter_no + " date:" + date_string + " " + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
                
    return True


def main():

    download_dir = "/home/admin/dockers/waterdata_backend/data/bulk_upload/"
    logs_dir = "/home/admin/dockers/waterdata_backend/data/bulk_upload/logs/"

    meter_no = "054151-2"                           #  "54151-2" 
    csvfile = download_dir + "IDCJAC0009_054151_2022_Data.csv"     # IDCJAC0009_054021_2021_Data.csv IDCJAC0009_054151_2021_Data.csv

    setupLogging(meter_no, logs_dir)
    
    mysql = MySQLUtil()
    mysql.dbConnect()

    result = rainfall_bulk_load(mysql,meter_no,csvfile) 
    
    if result == True:
        download_hist = download_dir + 'bulk_upload_hist'
        download_file = download_dir + csvfile
        move_download = moveFile(download_file, download_hist)

    return True


if __name__ == "__main__":
    main()