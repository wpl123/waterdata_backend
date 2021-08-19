# download_wrapper.py

import pandas as pd
# import numpy as np
import glob, os
import time
import datetime
import csv
import sys

# print(sys.path)
workingdir = "."
# sys.path.append(workingdir + 'downloading_scripts')
# print(sys.path)

from datetime import date
#from flutils import *

from surfacewater_api_download import *




def load_webdata(meter_no, sdate, edate, interval, varlist, multiplier, logs_dir, download_dir):

    result = False
    ndate = edate
    df = pd.DataFrame()  #(columns=['v','t','q'])
    df1 = pd.DataFrame() #(columns=['v','t','q'])
        
#    check_file_writable(download_dir)
#    check_file_writable(logs_dir)

#    date_1 = datetime.datetime.strptime("2013-09-14", "%Y-%m-%d")   #date("2010-10-27", "%Y-%m-%d")
    
    n = get_range(sdate,edate,interval)
    logging.info(inspect.stack()[0][3] + ' ' + meter_no + ' loading started for ' + str(sdate) + ' to ' + str(edate) + ' requiring ' + str(n) + " iterations")

    for i in range(n):
        if i > 0:
            sdate = get_sdate(edate,interval)    # set start date == edate
        
        edate = get_edate(sdate,ndate,interval)  # calculate edate from sdate

        logging.info(inspect.stack()[0][3] + ' Iter ' + str(i) + ' started for ' + str(sdate) + ' to ' + str(edate) + ' ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
#        url = 'https://realtimedata.waternsw.com.au/cgi/webservice.exe?{"function":"get_ts_traces","version":"2","params":{"site_list":'  + ('"{0}","start_time":"{1}","interval":"{2}","var_list":"100.00,140.01,232","datasource":"A","end_time":"{3}","data_type":"mean","rounding"').format(meter_no,sdate,interval,edate)  + ':[{"zero_no_dec":"1","dec_first":"1","sigfigs":"4","variable":"100","decimals":"2"}],' + ('"multiplier":"{0}"').format(multiplier) + '}}'
        url = 'https://realtimedata.waternsw.com.au/cgi/webservice.exe?{"function":"get_ts_traces","version":"2","params":{"site_list":'  + \
            ('"{0}","start_time":"{1}","interval":"{2}","var_list":"{3}","datasource":"A","end_time":"{4}","data_type":"mean","rounding"').format(meter_no,sdate,interval,varlist,edate)  + \
            ':[{"zero_no_dec":"1","dec_first":"1","sigfigs":"4","variable":"100","decimals":"2"}],' + \
            ('"multiplier":"{0}"').format(multiplier) + '}}'
        data = download_data(url)
        if data != None:
            df = loadData(data)
        else:
            return False

        df1 = df1.append(df, ignore_index=True)

    result = write_data(df1, meter_no, download_dir)
    return result



def main():

    logs_dir = "./app/gibbo_code/downloads/logs/"
    download_dir = "./app/gibbo_code/downloads/"


    meter_no = "GW967137.1.1"
    sdate = "20051116000000"
    edate = "20180819000000"
    interval = "minute"
    multiplier = "15"
    varlist = "110.00,2080.00"


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


    setupLogging(meter_no, logs_dir)
    result = load_webdata(meter_no, sdate, edate, interval, varlist, multiplier, logs_dir, download_dir)
    logging.info(inspect.stack()[0][3] + ' API Download ended ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
    print(result)


if __name__ == "__main__":
    main()