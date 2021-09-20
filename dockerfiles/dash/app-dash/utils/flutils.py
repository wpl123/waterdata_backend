#-*- coding: UTF-8 -*- 
import pymysql
import logging
import datetime
import shutil
import os, glob

from utils.dbutils import *

def setupLogging(meter_no, logs_dir):
    
    logfile = logs_dir + str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')) + ".log"
    logging.basicConfig(filename=logfile,level=logging.INFO)
    logging.info('-' * 80)
    logging.info(' Logging started for ' + meter_no + ' at ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))




def moveFile(fnm, dnm):
    logging.info(' Inside moveFile: filename ' + fnm + ' directory name ' + dnm + ' at ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
    dir_writeable = check_dir_writable(dnm)

    if dir_writeable == True:
        for file in glob.glob(fnm):
            shutil.move(file, dnm)
            logging.info(' File ' + file + ' moved to directory ' + dnm + ' at ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
        return True
    else:
        return False
        logging.error(' File ' + file + ' couldn\'t be moved to directory ' + dnm + ' ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))    


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
    