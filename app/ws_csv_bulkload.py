import pymysql
import pandas as pd
import numpy as np
import sys, os, io
import csv, time 
import datetime
import inspect
import requests
import json
import codecs

from datetime import timedelta
from decimal import Decimal

#https://stackoverflow.com/questions/1260792/import-a-file-from-a-subdirectory#%E2%80%A6
sys.path.extend([f'./{name}' for name in os.listdir(".") if os.path.isdir(name)])

from dbutils import *
from flutils import *
from dtutils import *

logs_dir = "/home/admin/dockers/waterdata_backend/data/bulk_upload/logs/"

logfile = logs_dir + str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')) + ".log"
logger = logging
logger.basicConfig(filename=logfile,level=logging.INFO)
logger.info('-' * 80)
logger.info(inspect.stack()[0][3] + ' Logging started at ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
logger.info('-' * 80)



def strip_nonascii(b):
    return b.decode('ascii', errors='ignore')


def process_csv(meter_no, download_dir): 
    
    logger.info(inspect.stack()[0][3] + ' Downloading CSV for meter ' + meter_no + ' at ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
    
    
    df = pd.DataFrame(columns=['StationName','ObsDate','EvapoTranspiration','Rain','PanEvap', 'MaxTemp','MinTemp','MaxHumid', 'MinHumid', '10mWind Speed','SolarRadiation'])  #(columns=['v','t','q'])
    df1 = pd.DataFrame(columns=['StationName','ObsDate','EvapoTranspiration','Rain','PanEvap', 'MaxTemp','MinTemp','Max Humid', 'MinHumid', '10mWind Speed','SolarRadiation']) #(columns=['v','t','q'])
    
    for i in range(2009,2022):
        
        for j in range(1,12):
            
            fname = download_dir + '/narrabri_airport-YYYYMM.csv'
            fname1 = fname.replace('YYYY',str(i))
            fname2 = fname1.replace('MM', str(j).zfill(2))
            fname3 = fname2.replace('narrabri', "upd_narrabri")
            
            
            # Massage the binary data
            fp = open(fname2,'rb')
            lines = fp.readlines()
            fp.close
 
            lns = []
            line_count = 0
            for line in lines:
                line_count = line_count + 1
                if line_count > 13:
                    ln = (line.decode('utf-8').replace('\n','')).split(',')
                    lns.append(ln)
            
            lns = lns[:-1]   # remove the Totals line
            
            df = pd.DataFrame(lns, columns=['StationName','ObsDate','EvapoTranspiration','Rain','PanEvap', 'MaxTemp','MinTemp','MaxHumid', 'MinHumid', '10mWindSpeed','SolarRadiation']) #, date_parser=mydateparser
                    
            if df.empty == True:
                logger.info(inspect.stack()[0][3] + ' ERROR: No CSV data for meter ' + meter_no + ' at ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
            else:
                logger.info(inspect.stack()[0][3] + ' Returning CSV data for meter ' + meter_no + ' at ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
                 
        df1 = df1.append(df, ignore_index=True)
                  
    
    return df1



def main():

    download_dir = "/home/admin/dockers/waterdata_backend/data/api/"
    

    meter_no = "054038"
    
    #TODO: implement this URL --> ftp.bom.gov.au/anon/gen/clim_data/IDCKWCDEA0/tables/nsw/narrabri_airport/narrabri_airport-202207.csv

    #url = 'ftp.bom.gov.au/anon/gen/clim_data/IDCKWCDEA0/tables/nsw/narrabri_airport/narrabri_airport-202207.csv'
    

    setupLogging(meter_no, logs_dir)
    
    result = process_csv(meter_no,download_dir) 
    
    #TODO: Return download CSV file
    #if result == True:
    #    download_hist = download_dir + 'bulk_upload_hist'
    #    download_file = download_dir + csvfile
    #    move_download = moveFile(download_file, download_hist)

    return True


if __name__ == "__main__":
    main()
    
    


