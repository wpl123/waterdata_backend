import pandas as pd
import numpy as np
import datetime
import inspect

from datetime import timedelta
from dateutil.parser import parse

#from wrapper_api_download import logger
from dbutils import *
from flutils import *


def checkDate(y,m,d):
    # print (y, m, d)
    dte = '-'.join((y, m, d))

    if dte:
        try:
            parse(dte)
            return True
        except:
            return False
    return False


def convert_string_date(date1):
    
    date2 = datetime.datetime.strptime(date1,"%Y%m%d%H%M%S")
#    print("Date: ", date2)
    return date2


def convert_string_date2(date1):
    
    date2 = datetime.datetime.strptime((date1),"%Y-%m-%d")
#    print("Date: ", date2)
    return date2


def convert_date_string(date1):
    
    date2 = date1.strftime("%Y%m%d%H%M%S")
#    print("String: ", date2)
    return date2




def get_range(sdate_str,edate_str,interval): #year, month, day, hour, minute, second, period, default
    
    sdate_dte = convert_string_date(sdate_str)
    edate_dte = convert_string_date(edate_str)
    ndays = edate_dte - sdate_dte
#    print("ndays: ", ndays)
    if interval == "minute":
        no_iterations = int(((ndays.days * 96) / 960) + 1)
    else:    
        no_iterations = int((ndays.days / 1000) + 1)

#    print("Iterations: ", no_iterations)
    return no_iterations



def get_sdate(edate_str,interval): #year, month, day, hour, minute, second, period, default
    
    edate_dte = convert_string_date(edate_str)

    if interval == "minute":
        sdate_dte = edate_dte + timedelta(minutes=15)    
    else:
        sdate_dte = edate_dte + timedelta(days=1)

    return convert_date_string(sdate_dte)



def get_edate(sdate_str,ndate_str,interval): #year, month, day, hour, minute, second, period, default

    sdate_dte = convert_string_date(sdate_str)
    ndate_dte = convert_string_date(ndate_str)
# if no of records requested > 1000 then calculate edate; else use edate
    
    if interval == "minute":
        if (ndate_dte - sdate_dte).days > 10:    # i.e. 10 days with (24 hours x 4 fifteen min intervals) = 960 records
            edate_dte = sdate_dte + timedelta(days=10) - timedelta(minutes=15)
        else:
            edate_dte = ndate_dte #+ timedelta(minutes=1425)   
    else:
        if (ndate_dte - sdate_dte).days > 1000: 
            edate_dte = sdate_dte + timedelta(days=1000)
        else:
            edate_dte = ndate_dte
    return convert_date_string(edate_dte)


def normalize_sw_Date(d):
    return '-'.join(((d[0:4]), d[4:6], d[6:8]))


# 01/06/2022
def normalize_date1(d):
    return '-'.join(((d[6:10]), d[3:5], d[0:2]))

# 2021-08-14T23:00:00Z
def normalizeDate2(d):
    return d[0:10]
