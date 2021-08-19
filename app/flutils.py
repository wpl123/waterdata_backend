#-*- coding: UTF-8 -*- 

import logging
import datetime
import shutil
import os, glob, inspect
#import pandas as pd



def setupLogging(meter_no, logs_dir):
    
    logfile = logs_dir + str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')) + ".log"
    logging.basicConfig(filename=logfile,level=logging.INFO)
    logging.info('-' * 80)
    logging.info(inspect.stack()[0][3] + ' Logging started for ' + meter_no + ' at ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))




def moveFile(fnm, dnm):
    logging.info(inspect.stack()[0][3] + ' Inside moveFile: filename {0} directory name {1} at {2}'.format(fnm,dnm,datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')))
    dir_writeable = check_dir_writable(dnm)

    if dir_writeable == True:
        for file in glob.glob(fnm):
            try:
                shutil.move(file, dnm)
                logging.info(inspect.stack()[0][3] + ' File {0} moved to directory {1} at {2}'.format(file,dnm,datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')))
                result = True
            except Exception as e:
                logging.info(inspect.stack()[0][3] + ' File couldn\'t be moved to directory. Error was ' + str(e))
                result = False    
            return result
    else:
        return False
        logging.error(inspect.stack()[0][3] + ' File {0} couldn\'t be moved to directory {1} at {2} '.format(file,dnm,datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')))    


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
    


