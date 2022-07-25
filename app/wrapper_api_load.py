# wrapper_api_load.py

import csv
import datetime
import glob, os, sys
import time
import inspect
from cv2 import multiply

import numpy as np
import pandas as pd
import pymysql
from sklearn import multiclass

#https://stackoverflow.com/questions/1260792/import-a-file-from-a-subdirectory#%E2%80%A6
sys.path.extend([f'./{name}' for name in os.listdir(".") if os.path.isdir(name)])

workingdir = "/home/admin/dockers/waterdata_backend/app/"
logs_dir = "/home/admin/dockers/waterdata_backend/data/api/logs/"

from datetime import date
from flutils import *
from emutils import *
import dbconfig

from water_api_processing import *
from rainfall_ftp_load import *
from ws_ftp_ws_load import *

#from rainfall_ftp_download import *
#from rainfall_ftp_upload import *

logfile = logs_dir + str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')) + ".log"
logger = logging
logger.basicConfig(filename=logfile,level=logging.INFO)
logger.info('-' * 80)
logger.info(inspect.stack()[0][3] + ' Logging started at ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
logger.info('-' * 80)

#API Info
#
# Info available here --> https://kisters.com.au/doco/hydllp.htm
# https://realtimedata.waternsw.com.au/cgi/webservice.exe?{"function":"get_variable_list","version":"1","params":{"site_list":"GW967137.1.1","datasource":"A"}}




def set_api_url(meter_no, url, varlist, tablename):

#    shorturl = 'https://realtimedata.waternsw.com.au/cgi/webservice.exe?{"function":"get_ts_traces","version":"2","params":{"site_list":"SITELIST","start_time":"SDATE","interval":"INTERVAL","var_list":"VARLIST","datasource":"A","end_time":"EDATE","data_type":"mean","rounding":[{"zero_no_dec":"1","dec_first":"1","sigfigs":"4","variable":"100","decimals":"2"}],"multiplier":"MULTIPLIER"}}'
#    meter_no = "GW967137.1.1"
#    sdate = "20051116000000"
#    edate = "20180819000000"
#    interval = "minute"
#    multiplier = "15"
#    varlist = "110.00,115.00,2080.00"
#    source = "CP" or "A" or "B"

#    meter_no = "GW967137.2.2"
#    sdate = "20210101000000"
#    edate = "20210330000000"
#    interval = "day"
#    multiplier = "1"
#    varlist = "110.00,2080.00"

#    meter_no = "203056"
#    sdate = "20101027000000"
#    edate = "20181030234500"
#    interval = "minute"
#    multiplier = "15"
#    varlist = "100.00,141.01"

    #Varlist 
    # 1. Bore levels varlist = "100.00,140.01,232"
    # 2. Streamflow varlist = "100.00,141.01" 
        
    interval = "day"  #TODO: use database values
    multiplier = "1"
    
    day_offset = 7                  #REFRESH DB day_offset = 20000
    edt = date.today()
    sdate = edt
    sdate = check_start_end_dates(tablename, meter_no, day_offset)
    #sdate = sdate - datetime.timedelta(days=7)
    sdate = sdate.strftime('%Y%m%d%H%M%S')       # extract date from the SQLtuple

    #sdate = convert_date_string(datetime.datetime.combine(sdt, datetime.datetime.min.time()))
    edate = convert_date_string(datetime.datetime.combine(edt, datetime.datetime.min.time()))
    #sitelist = meter_no[:-4] # strip off the "_API" from the meter_no
    sitelist = meter_no
    
    url1 = url.replace("INTERVAL", interval)
    url2 = url1.replace("MULTIPLIER", multiplier)
    url3 = url2.replace("VARLIST", str(varlist))
    url4 = url3.replace("SDATE", sdate)
    url5 = url4.replace("EDATE", edate)
    url6 = url5.replace("SITELIST", sitelist)
    
    logger.info(inspect.stack()[0][3] + " Found for " + meter_no + ' URL ' + url6 + ' ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
    
    return(url6)
    
    


def download_data(df,download_dir):
    
    # TODO: Integrate ftp downloads dir with the api downloads structure
    
    downloads_dir = "/home/admin/dockers/waterdata_backend/data/downloads/"
    uploads_dir = "/home/admin/dockers/waterdata_backend/data/uploads/"
        
    for i in range(len(df)): 
    
    #Note:    
    #    meter_no   = df.iloc[i,1]
    #    meter_type = df.iloc[i,3]
    #    url        = df.iloc[i,10]
    #    params     = df.iloc[i,11]
    #    varlist    = df.iloc[i,15]
    #    elevation  = df.iloc[i,6]
        
        #print("inside api_execute", df.iloc[i,3])    
        if df.iloc[i,3] == 0:             # test
            pass  # print("test_format(df.iloc[i,10], df.iloc[i,11]), workingdir")        
        elif df.iloc[i,3] == 11:        # Stream flow. Pass url, meter_no, download_dir
            url = set_api_url(df.iloc[i,1], df.iloc[i,10], df.iloc[i,15], "surfacewater")
            df_download = execute_api(url, df.iloc[i,1], download_dir, "surfacewater")
            
        elif df.iloc[i,3] == 12:        # Groundwater 2 column. Pass url, meter_no, download_dir
            url = set_api_url(df.iloc[i,1], df.iloc[i,10], df.iloc[i,15], "groundwater")
            df_download = execute_api(url, df.iloc[i,1], download_dir, "groundwater")
            
        elif df.iloc[i,3] == 13:        # Groundwater 3 column. Pass url, meter_no, download_dir
            url = set_api_url(df.iloc[i,1], df.iloc[i,10], df.iloc[i,15], "groundwater")
            df_download = execute_api(url, df.iloc[i,1], download_dir, "groundwater")
            
        elif df.iloc[i, 3] == 4:        # Rainfall column
            rainfall_ftp_write(df.iloc[i,1],df.iloc[i,10],df.iloc[i,11],download_dir, logs_dir)
        
        elif df.iloc[i, 3] == 8:        # BOM WS
            ws_ftp_write(df.iloc[i,1],df.iloc[i,10],df.iloc[i,11],download_dir, logs_dir)
    #        pass    
        else:
            pass

    return    



def get_meter_data():                       # read in all the active meters

    connection = pymysql.connect(host=dbconfig.host, 
        user=dbconfig.user, 
        password=dbconfig.psw, 
        db=dbconfig.db_name, 
        charset='utf8', 
        port=dbconfig.port)

    try:
        with connection.cursor() as cursor:  # order by meter_type to make sure rainfall loads first


            sql = ('''SELECT `A`.*, `B`.`interval`, `B`.`varlist`, `B`.`multiplier`
                        FROM   
                            `meters` AS `A`
                        INNER JOIN
                            `meter_types` `B` ON (`B`.`meter_type` = `A`.`meter_type`) 
                        WHERE  
                            `A`.`get_data` = 1  
                        ORDER BY 
                            `A`.`meter_type` DESC                
                        ''')
        
        df = pd.read_sql_query(sql, connection, parse_dates=['read_date','%Y-%m-%d'], coerce_float=True)
        
    except:
        print("Error: unable to get meter data")

    connection.close()
    return(df)



def main():
    
    download_dir = "/home/admin/dockers/waterdata_backend/data/api/"
    
    
    check_file_writable(download_dir)
    check_file_writable(logs_dir)
    
    meter_df = get_meter_data()    
    download_data(meter_df,download_dir)
    logger.info(inspect.stack()[0][3] + ' SUCCESS: Finished water download at ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
   
    if check_logfile(logfile) == True:
        assemble_email(logfile, 'ERROR: Waterdata download errors found')
#    else:
#        assemble_email(logfile, 'SUCCESS: Waterdata download successful')



if __name__ == "__main__":
    main()