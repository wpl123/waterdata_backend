
import pandas as pd
import sys, inspect
import csv, time 
import datetime
import logging
import fnmatch

from ftplib import FTP
from datetime import timedelta
from flutils import *
from dbutils import *



# meter_no = ""
# download_url = ""
# last_download = datetime.datetime.now()
# downloads_dir = ""
# logs_dir = ""


def write_csv(fname,df_to_csv):

    df_to_csv.to_csv(fname,encoding='utf-8',index=False,mode='w')
    logging.info(inspect.stack()[0][3] + ' Finished writing records to CSV file ' + fname )
    return fname


def get_fname(downloads_dir, meter_no,ldate):
        
    fname = downloads_dir + meter_no + '_' + ldate + '.csv'
    return fname


def load_data(df,meter_no):

    df1 = pd.DataFrame(columns=['IndexNo', 'SensorType', 'SensorDataType', 'SiteIdType', 'SiteId', 'ObservationTimestamp', 'RealValue', 'Unit', 'SensorParam1', 'SensorParam2', 'Quality', 'Comment'])
    df1 = df1.append(df.loc[(df['SiteId']) == meter_no])
    return df1
    


def getFile(ftp, filename):


#     IndexNo SensorType SensorDataType SiteIdType    SiteId  ObservationTimestamp RealValue Unit SensorParam1 SensorParam2 Quality Comment
# 190     190         RN              7        SSR  054021-1  2021-08-13T23:00:00Z         0   mm          NaN        86400       3     NaN
# 191     191         RN              7        SSR  054021-1  2021-08-14T23:00:00Z         0   mm          NaN        86400       3     NaN
# 214     214         RN              7        SSR  054151-2  2021-08-13T23:00:00Z         0   mm          NaN        86400       3     NaN
# 215     215         RN              7        SSR  054151-2  2021-08-14T23:00:00Z         0   mm          NaN        86400       3     NaN    
    
    
    try:
        ftp.retrbinary("RETR " + filename ,open(filename, 'wb').write)
        df = pd.read_csv(filename, skiprows=7,index_col=False, header=None, engine='python',names=['IndexNo', 'SensorType', 'SensorDataType', 'SiteIdType', 'SiteId', 'ObservationTimestamp', 'RealValue', 'Unit', 'SensorParam1', 'SensorParam2', 'Quality', 'Comment'],parse_dates=['ObservationTimestamp']) #, date_parser=mydateparser
        
    except Exception as e:
        df = pd.DataFrame(columns=['IndexNo', 'SensorType', 'SensorDataType', 'SiteIdType', 'SiteId', 'ObservationTimestamp', 'RealValue', 'Unit', 'SensorParam1', 'SensorParam2', 'Quality', 'Comment'])    
        logging.error(inspect.stack()[0][3] + ' FTP of ' + filename + ' failed ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S') + str(e))
    
    return df
    



def ftp_extract(ftp,meter_no,params,downloads_dir):

#    welcome_text = ftp.getwelcome()
#    print(welcome_text)
    ftp.login('anonymous', 'wplaird@bigpond.com')       # user anonymous, passwd anonymous@
    ftp.cwd("/anon/gen/fwo/")
    os.chdir(downloads_dir)                           #changing to /pub/unix            

    files = []
    ftp.retrlines('NLST', files.append)                 # list directory contents 

    for fname in fnmatch.filter(files, params):
        data = getFile(ftp,fname)
        logging.info(inspect.stack()[0][3] + ' Data from file ' + downloads_dir + fname + ' extracted at ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')) 
        df_loaded = load_data(data, meter_no)
        logging.info(inspect.stack()[0][3] + ' Data for meter ' + meter_no + ' loaded at ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')) 

    return df_loaded


def rainfall_scrape_and_write(meter_no, download_url, params, downloads_dir, logs_dir):

    setupLogging(meter_no, logs_dir)
    
    to_day = datetime.datetime.today()
    ldate = (to_day).strftime('%Y%m%d')    # ldate = logfile date   

    ftp = FTP(download_url)        # connect to host, default port
    logging.info(inspect.stack()[0][3] + ' FTP session opened for meter ' + meter_no + ' url ' + download_url + ' at ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')) 
    df_loaded = ftp_extract(ftp,meter_no,params,downloads_dir)
    ftp.quit()
    fname = get_fname(downloads_dir, meter_no,ldate)
    status = write_csv(fname, df_loaded)
   
   
    logging.info(inspect.stack()[0][3] + ' FTP session ended ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))