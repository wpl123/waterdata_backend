import pandas as pd
import numpy as np
import requests
import re
import fnmatch
import datetime

from ftplib import FTP



def load_data(df,station_nos):

    df1 = pd.DataFrame(columns=['IndexNo', 'SensorType', 'SensorDataType', 'SiteIdType', 'SiteId', 'ObservationTimestamp', 'RealValue', 'Unit', 'SensorParam1', 'SensorParam2', 'Quality', 'Comment'])
    for station_no in station_nos:
        print(station_no, type(station_no))
        df1 = df1.append(df.loc[(df['SiteId']) == station_no])
    return df1


def mydateparser(string_list):
    string_list1 = string_list.replace('T',' ')
    string_list2 = string_list1.replace('Z','')
    
    return string_list2


def getFile(ftp, filename):

#     IndexNo SensorType SensorDataType SiteIdType    SiteId  ObservationTimestamp RealValue Unit SensorParam1 SensorParam2 Quality Comment
# 190     190         RN              7        SSR  054021-1  2021-08-13T23:00:00Z         0   mm          NaN        86400       3     NaN
# 191     191         RN              7        SSR  054021-1  2021-08-14T23:00:00Z         0   mm          NaN        86400       3     NaN
# 214     214         RN              7        SSR  054151-2  2021-08-13T23:00:00Z         0   mm          NaN        86400       3     NaN
# 215     215         RN              7        SSR  054151-2  2021-08-14T23:00:00Z         0   mm          NaN        86400       3     NaN    
    
    
    #mydateparser = lambda x: pd.datetime.strptime(x, "%Y-%m-%d'T'%H:%M:%S'Z'")
    try:
        ftp.retrbinary("RETR " + filename ,open(filename, 'wb').write)
        df = pd.read_csv(filename, skiprows=7,index_col=False, header=None, engine='python',names=['IndexNo', 'SensorType', 'SensorDataType', 'SiteIdType', 'SiteId', 'ObservationTimestamp', 'RealValue', 'Unit', 'SensorParam1', 'SensorParam2', 'Quality', 'Comment'],parse_dates=['ObservationTimestamp']) #, date_parser=mydateparser
#        df = pd.read_csv(filename, skiprows=7,index_col=False, header=None, engine='python',names=['IndexNo', 'SensorType', 'SensorDataType', 'SiteIdType', 'SiteId', 'ObservationTimestamp', 'RealValue', 'Unit', 'SensorParam1', 'SensorParam2', 'Quality', 'Comment'],parse_dates=['ObservationTimestamp'], infer_datetime_format=True)
        
    except Exception as e:
        df = pd.DataFrame(columns=['IndexNo', 'SensorType', 'SensorDataType', 'SiteIdType', 'SiteId', 'ObservationTimestamp', 'RealValue', 'Unit', 'SensorParam1', 'SensorParam2', 'Quality', 'Comment'])    
            #logging.error(' execSQL failed ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S') + sql)
            #logging.error(' execSQL failed ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S') + str(e))
        print("Error" + str(e))    
    
    return df


station_nos = ['054021-1','054151-2']
ftp = FTP('ftp.bom.gov.au')                         # connect to host, default port
welcome_text = ftp.getwelcome()
print(welcome_text)
ftp.login('anonymous', 'wplaird@bigpond.com')       # user anonymous, passwd anonymous@
ftp.cwd("/anon/gen/fwo/")                           #changing to /pub/unix            

files = []
ftp.retrlines('NLST', files.append)                 # list directory contents 


for fname in fnmatch.filter(files, "IDN65902_*.hcs*"):
#    print(fname)
    data = getFile(ftp,fname)
#    print(data)
    df_loaded = load_data(data,station_nos)

    print(df_loaded)


ftp.quit()