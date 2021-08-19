# download_wrapper.py

import csv
import datetime
import glob
import os
import sys
import time

import numpy as np
import pandas as pd
import pymysql

# print(sys.path)
workingdir = "/home/admin/dockers/waterdata_backend/ml/"
#sys.path.append(workingdir + 'loading_scripts')
# print(sys.path)

from datetime import date
from flutils import *

# from groundwater_2col_model import *
# from groundwater_3col_model import *
# from rainfall_model import *
from surfacewater_model import *




def get_meter_data():

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
                            `get_data` = 2
                        ''')

        df = pd.read_sql_query(sql, connection, parse_dates=['read_date','%Y-%m-%d'], coerce_float=True)

    except:
        print("Error: unable to convert the data")

    connection.close()
#    print(df.dtypes)
    return(df)




def run_models(df):

    downloads_dir = "/home/admin/dockers/waterdata_backend/data/downloads/"  #TODO: direcory structure for csvs
    uploads_dir = "/home/admin/dockers/waterdata_backend/data/uploads/"
    logs_dir = "/home/admin/dockers/waterdata_backend/data/uploads/logs/"
    
    check_file_writable(uploads_dir)
    check_file_writable(logs_dir)

    for i in range(len(df)):
    
        # print(i, df.iloc[i, 1])

        if df.iloc[i, 3] == 100:             # test
            pass # print("test_format(df.iloc[i,10], df.iloc[i,11]), workingdir")        #TODO
        elif df.iloc[i, 3] == 101:        # Stream flow. Pass meter_no, downloads_dir, uploads_dir, logs_dir
            surfacewaterModel(df.iloc[i,1], downloads_dir, uploads_dir, logs_dir)
        elif df.iloc[i, 3] == 102:        # Groundwater 2 column
            pass # groundwater2colLoad(df.iloc[i,1], downloads_dir, uploads_dir, logs_dir) 
        elif df.iloc[i, 3] == 103:        # Groundwater 3 column
            pass # groundwater3colLoad(df.iloc[i,1], downloads_dir, uploads_dir, logs_dir)
#        elif df.iloc[i, 3] == 4:        # Rainfall column
#            rainfallLoad(df.iloc[i,1], downloads_dir, uploads_dir, logs_dir)
        else:
            pass

    #    time.sleep(1)    



def main():
    meter_df = get_meter_data()
    run_models(meter_df)


if __name__ == "__main__":
    main()
