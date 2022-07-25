#-*- coding: UTF-8 -*- 

import logging
import pandas as pd
import datetime
import shutil
import os, glob, inspect
#import pandas as pd




def check_dir_writable(dnm):
    return os.access(dnm, os.W_OK)



def check_file_writable(fnm):  
    
    if os.path.exists(fnm):
        # path exists
        if os.path.isfile(fnm): # is it a file or a dir?
            # also works when file is a link and the target is writable
            return os.access(fnm, os.W_OK)
        else:
            return False # path is a dir, so cannot write as a file
    # target does not exist, check perms on parent dir
    pdir = os.path.dirname(fnm)
    if not pdir: pdir = '.'
    # target is creatable if parent dir is writable
    return os.access(pdir, os.W_OK)
    


def check_loaded(_meter_no, _download_dir, _last_download):
    _result = False
    _today = datetime.datetime.today()
    _ldate = (_today).strftime('%Y%m%d')
    _ddate = (_last_download).strftime('%Y%m%d')
    _csvfile = _download_dir + _meter_no + '_' + _ldate + '.csv'
    
    if _ddate == _ldate:                        # check if download failed
        _result = True
    elif os.path.exists(_csvfile) == True:     # check if upload failed
        _result = True
    else:
        _result = False
        
    return _result    
 


def check_logfile(_logfile):

    file1 = open(_logfile, "r")
    readfile = file1.read()
    if 'error' in readfile or 'ERROR' in readfile or 'Error' in readfile: 
        _error_flag = True
    else: 
        _error_flag = False 
    file1.close()
    return _error_flag



def del_files(_directory, _fname):
    result = False
    if os.path.exists(_directory):
        for file in glob.glob(_directory + _fname):
            os.remove(file)

        result = True    
    return result




def get_fname(downloads_dir, meter_no,ldate):
        
    fname = downloads_dir + meter_no + '_' + ldate + '.csv'
    return fname




def make_logfile(_logfile):
    
    if check_dir_writable(_logfile):
        with os.fdopen(_logfile, 'w') as log:
            log.write('Logfile created' + str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
        return True    
    else:
        return False
    



def mergeData(df0,df1,df2,df3):
    df = pd.DataFrame(columns=["Time","Variable","Value","Quality"],index=["Time"])
    # 1. Set Time as the index
    # 2. Merge records based on Time
    
    if pd.notnull(df0.iloc[0,0]) == True:  
        df = df0
    if pd.notnull(df1.iloc[0,0]) == True:    
        df = df.merge(df1,on=["Time"])    
    if pd.notnull(df2.iloc[0,0]) == True:
        df = df.merge(df2,on=["Time"])
    if pd.notnull(df3.iloc[0,0]) == True:
        df = df.merge(df3,on=["Time"]) 

    df = df.sort_values(by=['Time']) 
      
    return(df)    



def moveFile(fnm, dnm):  
    logging.info(inspect.stack()[0][3] + ' About to move {0} to directory name {1} at {2}'.format(fnm,dnm,datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')))
    dir_writeable = check_dir_writable(dnm)
    result = False

    if dir_writeable == True:
        for file in glob.glob(fnm):
            try:
                chk_file = dnm + '/' + os.path.basename(file)
                logging.info(inspect.stack()[0][3] + ' Check if {0} exists at {1}'.format(chk_file,datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')))
                if os.path.exists(chk_file):                     # check if that filename already exists in the destination directory   
                    logging.info(inspect.stack()[0][3] + ' File {0} exists. Moving to {0}.new at {1}'.format(chk_file,datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')))
                    chk_file = chk_file + ".new"                 # move to a different name
                shutil.move(file, chk_file)
                logging.info(inspect.stack()[0][3] + ' File {0} moved to directory {1} at {2}'.format(file,dnm,datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')))
                result = True
            except Exception as e:
                logging.error(inspect.stack()[0][3] + ' File could not be moved to directory. Error was ' + str(e))
                result = False    
        return result
    else:
        return False
#        logging.error(inspect.stack()[0][3] + ' File {0} could not be moved to directory {1} at {2} '.format(file,dnm,datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')))    



def setupLogging(meter_no, logs_dir):
    
    logfile = logs_dir + str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')) + ".log"
    logging.basicConfig(filename=logfile,level=logging.INFO)
    logging.info('-' * 80)
    logging.info(inspect.stack()[0][3] + ' Logging started for ' + meter_no + ' at ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))


#def setupLogging_new(logs_dir):
#    
#    logfile = logs_dir + str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')) + ".log"
#    logger = logging
#    logger.basicConfig(filename=logfile,level=logging.INFO)
#    logger.info('-' * 80)
#    logger.info(inspect.stack()[0][3] + ' Logging started at ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))




def write_csv_data(df, meter_no, download_dir):
    
    run_date = datetime.datetime.today()
    ldate = (run_date).strftime('%Y%m%d')    # ldate = logfile date
    
    fname = download_dir + str(meter_no) + "_" + str(ldate) + ".csv"
    df.to_csv(fname)
    return True



#def write_csv(fname,df_to_csv):
#
#    df_to_csv.to_csv(fname,encoding='utf-8',index=False,mode='w')
#    logging.info(inspect.stack()[0][3] + ' Finished writing records to CSV file ' + fname )
#    return fname
#