
import pandas as pd
import sys, os
import csv, time 
import datetime
import inspect
import fnmatch
import codecs

from ftplib import FTP
from datetime import timedelta,date
#from wrapper_api_load import logger

from dbutils import *
from dtutils import *
from flutils import *



# Mt Kaputar http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=136&p_display_type=dailyDataFile&p_startYear=&p_c=&p_stn_num=054151
# Mt Lindsay http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=136&p_display_type=dailyDataFile&p_startYear=&p_c=&p_stn_num=054021
#----------------------------------------------------------------------------------------------



def ws_data_format(meter_no,df1,download_dir):
    
# df1            

#   StationName     ObsDate EvapoTranspiration  Rain PanEvap MaxTemp MinTemp MaxHumid MinHumid 10mWindSpeed SolarRadiation
#   NARRABRI AIRPORT  01/06/2022                2.1   0.0            14.8     6.1       88       36         3.14          12.40
#   NARRABRI AIRPORT  02/06/2022                1.3   0.0            13.4    -0.7       91       49         1.58          10.26
#   NARRABRI AIRPORT  03/06/2022                0.9   0.0            12.5     1.2       94       75         2.13           4.55        

    
    write_log('Data format started')
    localdate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
    # initialise variables
    
    mid = 0
    comments = 'Automated Load'
    creation_date = localdate
    fields = []
    rows = []

    #print(df1)
    for i in range(len(df1)):
        
        read_date  = normalize_date1(df1.iloc[i, 1]) 
        
#       Set unknown values in extra ws_bom fields to -99.00 instead of zero or NULL  
#       TODO: Set them to NULL
        air_temp   = -99.00
        rel_humid  = -99.00
        wind_speed = -99.00
        wind_dir   = -99.00

        fields = [mid,meter_no,read_date,df1.iloc[i, 2],df1.iloc[i, 3],df1.iloc[i, 4],df1.iloc[i, 5],df1.iloc[i, 6],air_temp,df1.iloc[i, 7],df1.iloc[i, 8],rel_humid,df1.iloc[i, 9],wind_speed,wind_dir,df1.iloc[i, 10],comments,creation_date]

        rows.append(fields)

    df2 = pd.DataFrame(rows,columns=['id','meter_no','read_date','evaptranspiration','rf_read','pan_evaporation','max_air_temp','min_air_temp','air_temp','max_rel_humid','min_rel_humid','rel_humid','ave_10m_wind_speed','wind_speed','wind_direction','solar_radiation','comments','creation_date'])
    df2 = df2.replace(' ', -99.00) #        Set unknown to -99.00 instead of zero and nans while at it
    df2 = df2.fillna(-99.00)              
    #write_csv_data(df2, meter_no, download_dir)    #Unhash for testing
    write_log('Data format ended')
    return(df2)



def update_database(mysql, meter_no, df):

    write_log('Database load started')
    
    for i in range(len(df)):
        
        sql2 = ('''SELECT `id` FROM `ws_bom` WHERE `meter_no` = '{0}' AND `read_date` = '{1}' ''').format(df.iloc[i,1], df.iloc[i,2])
        dup_id = checkDuplicates(mysql, sql2)      # check for duplicates  
        
        if dup_id == None:                              #TODO: Check if update needed for modified data
            df.iloc[i,0] = lastID(mysql, 'ws_bom') + 1

            sql3 = (''' INSERT 
                        INTO `ws_bom` (`id`, `meter_no`, `read_date`,
                                `evaptranspiration`,`rf_read`,`pan_evaporation`,`max_air_temp`,`min_air_temp`,`air_temp`,
                                `max_rel_humid`,`min_rel_humid`,`rel_humid`,`ave_10m_wind_speed`,`wind_speed`,`wind_direction`,`solar_radiation`,
                                `comments`,`creation_date`)VALUES ({0}, '{1}', '{2}', {3}, {4}, {5}, {6}, {7},{8}, {9}, {10}, {11}, {12}, {13}, {14}, {15},'{16}','{17}')
                        ''' ).format(df.iloc[i,0], df.iloc[i,1], df.iloc[i,2], df.iloc[i,3],df.iloc[i,4],df.iloc[i,5],df.iloc[i,6],df.iloc[i,7], df.iloc[i,8], df.iloc[i,9], df.iloc[i,10],df.iloc[i,11],df.iloc[i,12],df.iloc[i,13],df.iloc[i,14],df.iloc[i,15],df.iloc[i,16],df.iloc[i,17])
            
            result2 = mysql.execSQL(sql3)          # insert row
            if result2 == False:
                write_log('Insert failed meter_no: {0} date: {1}'.format(df.iloc[i,1],df.iloc[i,2]))
        else:
# Debug         write_log('Skipping duplicate id ' + str(dup_id) + ' for meter_no: ' + df.iloc[i,1] + ' date: ' + str(df.iloc[i,2]))
            result2 = False
    write_log('Database load for ' + meter_no + ' completed ')            
    return result2



def getFile(ftp, filename):
    
    df = pd.DataFrame(columns=['StationName','ObsDate','EvapoTranspiration','Rain','PanEvap', 'MaxTemp','MinTemp','MaxHumid', 'MinHumid', '10mWind Speed','SolarRadiation'])  #(columns=['v','t','q'])
        
    try:
        ftp.retrbinary("RETR " + filename ,open(filename, 'wb').write)
                
        # Massage the binary data
        fp = open(filename,'rb')
        lines = fp.readlines()
        fp.close
        
        lns = []
        line_count = 0
        for line in lines:
            line_count = line_count + 1
            if line_count > 13:             # skip header lines
                ln = (line.decode('utf-8').replace('\n','')).split(',')
                lns.append(ln)
        
        lns = lns[:-1]                      # remove the Totals line from the bottom of the list
        
        df = pd.DataFrame(lns, columns=['StationName','ObsDate','EvapoTranspiration','Rain','PanEvap', 'MaxTemp','MinTemp','MaxHumid', 'MinHumid', '10mWindSpeed','SolarRadiation']) #, date_parser=mydateparser
                        
    except Exception as e:
        write_log('FTP of ' + filename + ' failed ' + str(e))
        
    return df




# read through the downloaded file_list1, determine the start and end dates of the files to be downloaded and add these to file_list2

def match_files_to_load(s_month, s_year, file_list1):
    
    write_log('Calculated starting month ' + str(s_month)  + ', year ' + str(s_year)) 
    today = datetime.date.today()
    edate   = today.strftime('%Y%m%d%H%M%S')
    e_year  = edate[:4]
    e_month = edate[4:6]
    
    file_list2  = []
   
    for _file in file_list1:                                    # look at all the files on the ftp server
        
        for _year in range(int(s_year),(int(e_year) + 1)):      # restrict search to the range of files to be uploaded
            
            if _year == (int(e_year)):                          # i.e. this year
                month_start = int(s_month)
                month_end   = int(e_month)
            else:                                               # i.e. previous years
                month_start = 1
                month_end = 12
                    
            for _month in range(month_start, (month_end + 1)):   
                
                fname  =  '-YYYYMM.csv'
                fname1 = fname.replace('YYYY',str(_year))
                fname2 = fname1.replace('MM', str(_month).zfill(2))
                
                if _file.find(fname2) > 0:                      # if calculated filename exists on the ftp server, add it to file_list2
                    file_list2.append(_file)
                   
    return file_list2



def get_first_file(_meter_no,_params):
    
    day_offset = 7                 
    edt   = date.today()
    sdate = edt
    sdate = check_start_end_dates("ws_bom", _meter_no, day_offset)
    sdate = sdate.strftime('%Y%m%d%H%M%S')
    _year = sdate[:4]
    _month = sdate[4:6]

    return _month, _year


def ftp_extract(ftp,meter_no,params,downloads_dir):

#    welcome_text = ftp.getwelcome()
#    print(welcome_text)
    
    df1 = pd.DataFrame() 
    
    ftp.cwd(params)
    os.chdir(downloads_dir)                             #changing to /pub/unix            
    
    files = []
    ftp.retrlines('NLST', files.append)                 # list directory contents 
    
    s_month, s_year = get_first_file(meter_no,params)
    files = match_files_to_load(s_month, s_year, files) # match files to download based on date
    
    for fname in fnmatch.filter(files, '*.csv'):
        
        df = getFile(ftp,fname)
        
        write_log('Data from file ' + downloads_dir + fname + ' extracted at ') 
        downloaded_fname = downloads_dir + fname
        
        df1 = df1.append(df, ignore_index=True)
    return downloaded_fname, df1




def ws_ftp_write(meter_no, download_url, params, download_dir, logs_dir):

    to_day = datetime.datetime.today()
    
    ftp = FTP(download_url,'anonymous', 'wplaird@bigpond.com')      # connect to host, default port, user anonymous, passwd anonymous@
    ftp.encoding='utf-8'                                            # force encoding for file name in utf-8 rather than default that is iso-8889-1
         
    write_log('FTP session opened for meter ' + meter_no + ' url ' + download_url + ' at ') 
    downloaded_file, df_loaded = ftp_extract(ftp,meter_no,params,download_dir)
    ftp.quit()
    #FTP complete, process data
    
    os.remove(downloaded_file)
        
   
    mysql = MySQLUtil()
    mysql.dbConnect()
   
    df_formatted = ws_data_format(meter_no, df_loaded,download_dir)    # format the downloaded data
    if df_formatted.empty == False: #not empty
        
        rf_load = update_database(mysql, meter_no, df_formatted)
        if rf_load == True:
            upd_meter = updateMeter(mysql, meter_no)
    
    else:
        write_log('No weather station data for ' + meter_no)

    mysql.dbClose()
    write_log('Completed FTP processing for meter ' + meter_no)
    
    

        