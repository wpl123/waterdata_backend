# download_wrapper.py

import csv
import datetime
import glob, os, sys
import time

import numpy as np
import pandas as pd
import pymysql

#https://stackoverflow.com/questions/1260792/import-a-file-from-a-subdirectory#%E2%80%A6
sys.path.extend([f'./{name}' for name in os.listdir(".") if os.path.isdir(name)])

# print(sys.path)
workingdir = "/home/admin/dockers/waterdata_backend/app/"
#sys.path.append(workingdir + 'loading_scripts')
# print(sys.path)

from datetime import date

import dbconfig

from flutils import *
from emutils import *

from groundwater_2col_upload import *
from groundwater_3col_upload import *
from rainfall_ftp_upload import *
from surfacewater_upload import *




def get_meter_data():

    connection = pymysql.connect(
        host=dbconfig.host,
        user=dbconfig.user, 
        password=dbconfig.psw,
        database=dbconfig.db_name,
        port=dbconfig.port)

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
#    print(df.dtypes)
    return(df)




def load_webdata(df):

    downloads_dir = "/home/admin/dockers/waterdata_backend/data/downloads/"
    uploads_dir = "/home/admin/dockers/waterdata_backend/data/uploads/"
    logs_dir = "/home/admin/dockers/waterdata_backend/data/uploads/logs/"
    logfile = logs_dir + str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')) + ".log"

    check_file_writable(uploads_dir)
    check_file_writable(logs_dir)

    for i in range(len(df)):
    
        # print(i, df.iloc[i, 1])

        if df.iloc[i, 3] == 0:             # test
            pass # print("test_format(df.iloc[i,10], df.iloc[i,11]), workingdir")       
        elif df.iloc[i, 3] == 1:        # Stream flow. Pass meter_no, downloads_dir, uploads_dir, logs_dir
            surfacewaterLoad(df.iloc[i,1], downloads_dir, uploads_dir, logs_dir)
        elif df.iloc[i, 3] == 2:        # Groundwater 2 column
            groundwater2colLoad(df.iloc[i,1], downloads_dir, uploads_dir, logs_dir) 
        elif df.iloc[i, 3] == 3:        # Groundwater 3 column
            groundwater3colLoad(df.iloc[i,1], downloads_dir, uploads_dir, logs_dir)
        elif df.iloc[i, 3] == 4:        # Rainfall column
            rainfallLoad(df.iloc[i,1], df.iloc[i,11],downloads_dir, uploads_dir, logs_dir)
        else:
            pass

        time.sleep(1)    
    return logfile 


def main():
    meter_df = get_meter_data()
    log = load_webdata(meter_df)
    
    if check_logfile(log) == True:
        assemble_email(log, 'ERROR: Waterdata database load errors found')
    # else:
    #     assemble_email(log, 'SUCCESS: Waterdata database load successful')

if __name__ == "__main__":
    main()
