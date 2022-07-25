# download_wrapper.py

import pymysql
import pandas as pd
import numpy as np
import glob, sys, os
import time
import datetime
import csv

#https://stackoverflow.com/questions/1260792/import-a-file-from-a-subdirectory#%E2%80%A6
sys.path.extend([f'./{name}' for name in os.listdir(".") if os.path.isdir(name)])

workingdir = "/home/admin/dockers/waterdata_backend/app/"

from datetime import date

from flutils import *
from emutils import *
import dbconfig


from surfacewater_download import *
from groundwater_2col_download import *
from groundwater_3col_download import *
from rainfall_ftp_download import *         
# from app.downloading_scripts.sw_download import *


def get_meter_data():                       # read in all the active meters

    connection = pymysql.connect(host=dbconfig.host, 
        user=dbconfig.user, 
        password=dbconfig.psw, 
        db=dbconfig.db_name, 
        charset='utf8', 
        port=dbconfig.port)

    try:
        with connection.cursor() as cursor:  # order by meter_type to make sure rainfall loads first

            sql = ('''  SELECT *      #TODO: Find intervals, multipliers etc in the meter_type table
                        FROM   
                            `meters`   
                        WHERE  
                            `get_data` = 1 
                        ORDER BY `meter_type` DESC     
                        ''')

        df = pd.read_sql_query(sql, connection, parse_dates=['read_date','%Y-%m-%d'], coerce_float=True)
        
    except:
        print("Error: unable to get meter data")

    connection.close()
    
    return(df)


def check_loaded(_meter_no, _download_dir, _last_download):
    _result = False
    _today = datetime.datetime.today()
    _ldate = (_today).strftime('%Y%m%d')
    _ddate = (_last_download).strftime('%Y%m%d')
    _csvfile = _download_dir + _meter_no + '_' + _ldate + '.csv'
    
    if _ddate == _ldate:                        # check if download failed
        _result = True
    elif os.path.exists(_csvfile) == True:     # check if upload failed
        _result = True
    else:
        _result = False
        
    return _result    
 


def scrape_webdata(df):

    download_dir = "/home/admin/dockers/waterdata_backend/data/downloads/"
    logs_dir = "/home/admin/dockers/waterdata_backend/data/downloads/logs/"
    logfile = logs_dir + str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')) + ".log"
    fp = open(logfile, 'x')
    fp.close()
    
    check_file_writable(download_dir)
    check_file_writable(logs_dir)
    del_files(logs_dir + '/screenshots/', '*.png')

    for i in range(len(df)): #TODO: build loop for more than 1000 days
    
        # print('Processing download for meter ' + df.iloc[i,1] + ' at ' + df.iloc[i,10] )
        #check if file already exists for today
        if check_loaded(df.iloc[i,1], download_dir, df.iloc[i,12]) == True:
            continue
        

        if df.iloc[i, 3] == 0:             # test
            pass  # print("test_format(df.iloc[i,10], df.iloc[i,11]), workingdir")        
        elif df.iloc[i, 3] == 1:        # Stream flow Pass meter_no, download_url, last_download, download_dir, logs_dir
            surfacewater_scrape_and_write(df.iloc[i,1],df.iloc[i,10],download_dir, logs_dir)
        elif df.iloc[i, 3] == 2:        # Groundwater 2 column. Pass meter_no, download_url, last_download, download_dir, logs_dir
            groundwater_2col_scrape_and_write(df.iloc[i,1],df.iloc[i,10],download_dir, logs_dir)
        elif df.iloc[i, 3] == 3:        # Groundwater 3 column. Pass meter_no, download_url, last_download, download_dir, logs_dir
            groundwater_3col_scrape_and_write(df.iloc[i,1],df.iloc[i,10],download_dir, logs_dir)
        elif df.iloc[i, 3] == 4:        # Rainfall column
            rainfall_scrape_and_write(df.iloc[i,1],df.iloc[i,10],df.iloc[i,11],download_dir, logs_dir)
        else:
            pass

        time.sleep(5)    
    return logfile    

def main():
    meter_df = get_meter_data()
    log = scrape_webdata(meter_df)
    
    if check_logfile(log) == True:
        assemble_email(log, 'ERROR: Waterdata download errors found')
    # else:
    #     assemble_email(log, 'SUCCESS: Waterdata download successful')


if __name__ == "__main__":
    main()