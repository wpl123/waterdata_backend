
import pandas as pd
import sys, inspect
import csv, time 
import datetime
import logging
import fnmatch

from ftplib import FTP
from datetime import timedelta

from dbutils import *
from dtutils import *
from flutils import *



# Mt Kaputar http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=136&p_display_type=dailyDataFile&p_startYear=&p_c=&p_stn_num=054151
# Mt Lindsay http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=136&p_display_type=dailyDataFile&p_startYear=&p_c=&p_stn_num=054021
#----------------------------------------------------------------------------------------------



def rainfallFormat(mysql, meter_no, df1,download_dir):
    
    write_log('Data format started')
    localdate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #ldate = (datetime.datetime.today() - timedelta(days=1)).strftime('%Y%m%d')
    
    # initialise variables
    
    mid = 0
    j = 0
    rf_read1 = 0.0
    DY_READ1 = 1
    QL_READ1 = "N"
    comments = 'Automated Load'
    creation_date = localdate
    fields = []
    rows = []

#    ftp data

#IndexNo,SensorType,SensorDataType,SiteIdType,SiteId,ObservationTimestamp,RealValue,Unit,SensorParam1,SensorParam2,Quality,Comment
#199,RN,7,SSR,054021-1,2021-08-14T23:00:00Z,0,mm,,86400,3,
#200,RN,7,SSR,054021-1,2021-08-15T23:00:00Z,0,mm,,86400,3,

    for i in range(len(df1)):
       
        read_date = normalizeDate2(df1.iloc[i, 5])
        rf_read1 = df1.iloc[i, 6]
        dy_read1 = DY_READ1
        ql_read1 = QL_READ1
        mn = df1.iloc[i, 4]
        
        fields = [mid,mn[:12],read_date,rf_read1,dy_read1,ql_read1,comments,creation_date]

        rows.append(fields)

    df2 = pd.DataFrame(rows,columns=['id','meter_no','read_date','rf_read1','dy_read1','ql_read1','comments','creation_date'])
    # write_csv_data(df2, meter_no, download_dir)     # Unhash for testing
    write_log('Data format ended')
    return(df2)



def loadFormatted(mysql, meter_no, df):

    write_log('Data load started')
    
    for i in range(len(df)):
        
        sql2 = ('''SELECT `id` FROM `rainfall` WHERE `meter_no` = '{0}' AND `read_date` = '{1}' ''').format(df.iloc[i,1], df.iloc[i,2])
        dup_id = checkDuplicates(mysql, sql2)      # check for duplicates  
        
        if dup_id == None:
            df.iloc[i,0] = lastID(mysql, 'rainfall') + 1

#            print(df2.iloc[i,0], df2.iloc[i,1], df2.iloc[i,2], df2.iloc[i,3],df2.iloc[i,4],df2.iloc[i,5],df2.iloc[i,6],df2.iloc[i,7])
            sql3 = (''' INSERT 
                        INTO `rainfall` (`id`, `meter_no`, `read_date`, 
                                `rf_read1`, `dy_read1`, `ql_read1`, 
                                `comments`, `creation_date`)VALUES ({0}, '{1}', '{2}', {3}, {4}, '{5}', '{6}', '{7}')
                        ''' ).format(df.iloc[i,0], df.iloc[i,1], df.iloc[i,2], df.iloc[i,3],df.iloc[i,4],df.iloc[i,5],df.iloc[i,6],df.iloc[i,7])
            
            result2 = mysql.execSQL(sql3)          # insert row
            if result2 == False:
                write_log('Insert failed meter_no: {0} date: {1}'.format(df.iloc[i,1],df.iloc[i,2]))
        else:
            write_log('Skipping duplicate id ' + str(dup_id) + ' for meter_no: ' + df.iloc[i,1] + ' date: ' + str(df.iloc[i,2]))
            result2 = False    
    return result2




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
        write_log('FTP of ' + filename + ' failed ' + str(e))
    
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
        write_log('Data from file ' + downloads_dir + fname + ' extracted') 
        downloaded_fname = downloads_dir + fname
        df_loaded = load_data(data, meter_no)

    return downloaded_fname, df_loaded 



def rainfall_ftp_write(meter_no, download_url, params, download_dir, logs_dir):

    #logfile = setupLogging(logs_dir)
    
    to_day = datetime.datetime.today()
    #ldate = (to_day).strftime('%Y%m%d')    # ldate = logfile date   

    ftp = FTP(download_url)        # connect to host, default port
    write_log('FTP session opened for meter ' + meter_no + ' url ' + download_url) 
    downloaded_file, df_loaded = ftp_extract(ftp,meter_no,params,download_dir)
    ftp.quit()
    write_log('Removing ' + downloaded_file) 
    os.remove(downloaded_file)
    #FTP complete, process data
   
    mysql = MySQLUtil()
    mysql.dbConnect()
   
    df_formatted = rainfallFormat(mysql, meter_no, df_loaded,download_dir)    
    if df_formatted.empty == False: #not empty
        
        rf_load = loadFormatted(mysql, meter_no, df_formatted)
        if rf_load == True:
            upd_meter = updateMeter(mysql, meter_no)
    
    else:
        write_log('No rainfall data for ' + meter_no)

    mysql.dbClose()
    write_log('FTP download ended for meter ' + meter_no)
    
    

        