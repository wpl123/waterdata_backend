import pandas as pd
import numpy as np
import requests
import re
import fnmatch
import csv
from ftplib import FTP




def getFile(filename):
   
    df = pd.read_csv(filename, skiprows=7,names=['IndexNo', 'SensorType', 'SensorDataType', 'SiteIdType', 'SiteId', 'ObservationTimestamp', 'RealValue', 'Unit', 'SensorParam1', 'SensorParam2', 'Quality', 'Comment'],index_col=False, header=None, engine='python')
    return df



def load_data(df,rain_gauge_list):

    df1 = pd.DataFrame(columns=['IndexNo', 'SensorType', 'SensorDataType', 'SiteIdType', 'SiteId', 'ObservationTimestamp', 'RealValue', 'Unit', 'SensorParam1', 'SensorParam2', 'Quality', 'Comment'])
    for station_no in station_nos:
        df1 = df1.append(df.loc[df['SiteId'] == station_no])
    return df1


fname = "IDN65902_20210813060019.hcs"
station_nos = ['054021-1','054151-2']
data = getFile(fname)
status = load_data(data,station_nos)
print(status)


