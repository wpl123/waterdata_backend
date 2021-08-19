# download_wrapper.py

import pymysql
import pandas as pd
import numpy as np
import glob, os
import time
import datetime
import csv
import sys

# print(sys.path)
workingdir = "/home/admin/dockers/waterdata_backend/app/"
# sys.path.append(workingdir + 'downloading_scripts')
# print(sys.path)

from datetime import date
from flutils import *


from surfacewater_download import *
from groundwater_2col_download import *
from groundwater_3col_download import *
from rainfall_ftp_download import *         
# from app.downloading_scripts.sw_download import *



def get_meter_data():                       # read in all the active meters

    connection = pymysql.connect(

        host='192.168.11.6',
        user='root', 
        password='water',
        database='waterdata',
        port=30000)

    try:
        with connection.cursor() as cursor:

            sql = ('''  SELECT *  
                        FROM   
                            `meters`   
                        WHERE  
                            `get_data` = 1
                        ''')

        df = pd.read_sql_query(sql, connection, parse_dates=['read_date','%Y-%m-%d'], coerce_float=True)

    except:
        print("Error: unable to convert the data")

    connection.close()
    
    return(df)



def scrape_webdata(df):

    download_dir = "/home/admin/dockers/waterdata_backend/data/downloads/"
    logs_dir = "/home/admin/dockers/waterdata_backend/data/downloads/logs/"
    
    check_file_writable(download_dir)
    check_file_writable(logs_dir)

    for i in range(len(df)): #TODO: build loop for more than 1000 days
    
        # print(i, df.iloc[i, 3])   # i.e. meter_type

        if df.iloc[i, 3] == 0:             # test
            pass  # print("test_format(df.iloc[i,10], df.iloc[i,11]), workingdir")        #TODO
        elif df.iloc[i, 3] == 1:        # Stream flow Pass meter_no, download_url, last_download, download_dir, logs_dir
            surfacewater_scrape_and_write(df.iloc[i,1],df.iloc[i,10],df.iloc[i,12],download_dir, logs_dir)
        elif df.iloc[i, 3] == 2:        # Groundwater 2 column. Pass meter_no, download_url, last_download, download_dir, logs_dir
            groundwater_2col_scrape_and_write(df.iloc[i,1],df.iloc[i,10],df.iloc[i,12],download_dir, logs_dir)
        elif df.iloc[i, 3] == 3:        # Groundwater 3 column. Pass meter_no, download_url, last_download, download_dir, logs_dir
            groundwater_3col_scrape_and_write(df.iloc[i,1],df.iloc[i,10],df.iloc[i,12],download_dir, logs_dir)
        elif df.iloc[i, 3] == 4:        # Rainfall column
            rainfall_scrape_and_write(df.iloc[i,1],df.iloc[i,10],df.iloc[i,11],df.iloc[i,12],download_dir, logs_dir)
        else:
            pass

        time.sleep(5)    
        

def main():
    meter_df = get_meter_data()
    scrape_webdata(meter_df)


if __name__ == "__main__":
    main()