# download_wrapper.py

# import pandas as pd
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
#from flutils import *

from surfacewater_all_download import *






def scrape_webdata():

    meter_no = "203056"
    url = "https://realtimedata.waternsw.com.au?ppbm=203056|203_RICHMOND|SURFACE_WATER&rs&1&rscf_org"
    download_dir = "./app/gibbo_code/downloads/"
    logs_dir = "./app/gibbo_code/downloads/logs/"
    
#    check_file_writable(download_dir)
#    check_file_writable(logs_dir)

    date_1 = datetime.datetime.strptime("2013-09-14", "%Y-%m-%d")   #date("2010-10-27", "%Y-%m-%d")
    
    for i in range(104):
        print("date_1 " + str(date_1))
        surfacewater_scrape_and_write(meter_no, url, date_1, download_dir, logs_dir)
        date_1 = date_1 + datetime.timedelta(days=18)
    
def main():

    scrape_webdata()


if __name__ == "__main__":
    main()