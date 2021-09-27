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
from dbutils_1_2 import *
from flutils import *

from realwater_api_download_utils import *

##################   WORKING CONFIGS  ###############################
# 
# # Ground water Data settings
# 
#     meter_no = "GW967137.1.1"
#     sdate = "20051116000000"
#     edate = "20180819000000"
#     interval = "minute"
#     multiplier = "15"
#     varlist = "110.00,2080.00"
# 
# 
# #     meter_no = "GW967137.2.2"
# #     sdate = "20210101000000"
# #     edate = "20210330000000"
# #     interval = "day"
# #     multiplier = "1"
# #     varlist = "110.00,2080.00"
# 
# 
# # Stream Flow Data settings
# 
# #    meter_no = "203056", "419051"
# #    sdate = "20101027000000"
# #    edate = "20181030234500"
# #    interval = "minute"
# #    multiplier = "15"
# #    varlist = "100.00,141.01"
# 
# 
# 
#     #Varlist 
#     # 1. Bore levels varlist = "100.00,140.01,232"
#     # 2. Streamflow varlist = "100.00,141.01"



def loadData(_data):
    tracelist = []
    varfromlist = []
   
    try:
        waterdata = _data['return']['traces']     #TODO: Trap errors
    except LookupError as e:
        logging.error(inspect.stack()[0][3] + " Lookup Error " + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S') + str(e))
        df = pd.DataFrame(columns=["Time","Variable","Value","Quality"],index=["Time"]) # taken from mergeData()
        return df
    else:     
#    print(waterdata)
        for tracesdict in waterdata:    #traces

            variabledata = tracesdict['varfrom_details']['variable']
#            print("variabledata: ", variabledata)

            tracedata = tracesdict['trace']
            if tracedata != []:
#                print("tracedata ", tracedata)
                for tracedict in tracedata:
                
#                    print("tracedict: ", tracedict)
                    fields = [str(tracedict.get('t')),variabledata,str(tracedict.get('v')),str(tracedict.get('q'))] #
                    tracelist.append(fields)
#                print("tracelist: ", tracelist)

#        for x in tracelist:
#            print(x)

        df = pd.DataFrame(tracelist,columns=["Time","Variable","Value","Quality"]) #

        df = splitData(df)

#    print("tracelist",df)

    return df     



def error_num_check(_data):
    _error_num = _data['error_num']

    if _error_num != 0:
        _error_msg = _data['error_msg']
        logging.error(inspect.stack()[0][3] + ' API ERROR No: ' + str(_error_num) + '. ' + _error_msg + ' ' + \
            datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))

    return _error_num


def download_data(download_url):

    successful = False
    while not successful:
        data = getResponse(download_url)
        if data != None:
            successful = True
        else:
            logging.error(inspect.stack()[0][3] + ' Data download unsuccessful! Re-trying URL: ' + (download_url) + ' ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
            time.sleep(1)

  
    return data    



def get_api_webdata(_mysql, meter_no, meter_type, meter_elev, logs_dir, download_dir):

    result = False
    df = pd.DataFrame()  #(columns=['v','t','q'])
    df1 = pd.DataFrame() #(columns=['v','t','q'])

    # Get the sdate, edate, interval, varlist, multiplier

    interval, varlist, multiplier = get_meter_api_params(_mysql, meter_type)
    sdate = get_last_record(_mysql, meter_no, meter_type)
    edate = datetime.datetime.today() - timedelta(days=1) # yesterday
    edate = convert_date_string(edate)
    ndate = edate

    
    n = get_range(sdate,edate,interval)
    logging.info(inspect.stack()[0][3] + ' ' + meter_no + ' loading started for ' + str(sdate) + ' to ' + str(edate) + ' requiring ' + str(n) + " iterations")

    for i in range(n):
        if i > 0:
            sdate = get_sdate(edate,interval)    # set start date == edate
        
        edate = get_edate(sdate,ndate,interval)  # calculate edate from sdate

        logging.info(inspect.stack()[0][3] + ' Iter ' + str(i) + ' started for ' + str(sdate) + ' to ' + str(edate) + ' ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
#        url = 'https://realtimedata.waternsw.com.au/cgi/webservice.exe?{"function":"get_ts_traces","version":"2","params":{"site_list":'  + ('"{0}","start_time":"{1}","interval":"{2}","var_list":"100.00,140.01,232","datasource":"A","end_time":"{3}","data_type":"mean","rounding"').format(meter_no,sdate,interval,edate)  + ':[{"zero_no_dec":"1","dec_first":"1","sigfigs":"4","variable":"100","decimals":"2"}],' + ('"multiplier":"{0}"').format(multiplier) + '}}'
        url = 'https://realtimedata.waternsw.com.au/cgi/webservice.exe?{"function":"get_ts_traces","version":"2","params":{"site_list":'  + \
            ('"{0}","start_time":"{1}","interval":"{2}","var_list":"{3}","datasource":"CP","end_time":"{4}","data_type":"mean","rounding"').format(meter_no,sdate,interval,varlist,edate)  + \
            ':[{"zero_no_dec":"1","dec_first":"1","sigfigs":"4","variable":"100","decimals":"2"}],' + \
            ('"multiplier":"{0}"').format(multiplier) + '}}'

        print(url)

        data = download_data(url)
        error_num = error_num_check(data)         #TODO: code to check for error messages e.g. {"error_num":125,"error_msg":"No data for specified variable in file"}
        if error_num == 0:
            df = loadData(data)
        else:
            return False

        df1 = df1.append(df, ignore_index=True)

    result = write_data(df1, meter_no, download_dir)
    return result




def load_api_and_write(meter_no, meter_type, meter_elev, params, logs_dir, download_dir):

    setupLogging(meter_no, logs_dir)

    mysql = MySQLUtil()
    mysql.dbConnect()

    result = get_api_webdata(mysql, meter_no, meter_type, meter_elev, logs_dir, download_dir)
    logging.info(inspect.stack()[0][3] + ' API Download ended ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
    
    mysql.dbClose()
    print(result)


