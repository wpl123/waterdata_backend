import pandas as pd
import numpy as np
import sys, webbrowser
import csv, time 
import datetime
import logging, inspect
import requests
import json

from datetime import timedelta
from flutils_all import *

def convert_string_date(date1):
    
    date2 = datetime.datetime.strptime(date1,"%Y%m%d%H%M%S")
#    print("Date: ", date2)
    return date2


def convert_date_string(date1):
    
    date2 = datetime.datetime.strftime(date1,"%Y%m%d%H%M%S")
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



def getResponse(url):
    try:  
        response = requests.get(url)
    except requests.exceptions.HTTPError as errh:
        logging.error(inspect.stack()[0][3] + ' Http error: ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S') + str(errh))
        return None
    except requests.exceptions.ConnectionError as errc:
        logging.error(inspect.stack()[0][3] + ' Error Connecting: ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S') + str(errc))
        return None
    except requests.exceptions.Timeout as errt:
        logging.error(inspect.stack()[0][3] + ' Timeout Error: ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S') + str(errt))
        return None
    except requests.exceptions.RequestException as err:
        logging.error(inspect.stack()[0][3] + ' OOps: Something Else: ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S') + str(err))
        return None

    jsonData = response.json() 
    if response and response.status_code == 200:
        return jsonData
    else:
        logging.error(inspect.stack()[0][3] + " Error receiving data: " + response.status_code + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
        return None


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
#    print(df)           
    return(df)


def splitData(df):      # 0. Sort data by variable and extract into separate df

    df0 = pd.DataFrame(columns=["Time","Variable","Value","Quality""Time","Variable","Value","Quality"],index=["Time"])
    df1 = pd.DataFrame(columns=["Time","Variable","Value","Quality"],index=["Time"])
    df2 = pd.DataFrame(columns=["Time","Variable","Value","Quality"],index=["Time"])
    df3 = pd.DataFrame(columns=["Time","Variable","Value","Quality"],index=["Time"])   # NB Limit of 4 variables
    
    
   
    # 
    df = df.sort_values(by=['Variable'])
    no_var = df.value_counts(subset=['Variable'])
    lastvar = df.iloc[0,1] 
    j = 0
    df_length = len(df)
    for i in range(df_length):

       
        if (df.iloc[i,1] != lastvar) or (i == (df_length - 1)):     # trigger df write at change in Variable or End of the Dataframe
                                                                    # in the next row after last Variable
            if j == 0:
                if i == (df_length - 1): # end of the dataframe
                    df0 = df[0:i + 1]
                else:    
                    df0 = df[0:i]
                i0 = i 
#                print(f"j: {j} i: {i} Variable {df.iloc[i,0]}, lastvar {lastvar}")
                j = j + 1
            elif j == 1:
                if i == (df_length - 1): # end of the dataframe
                    df1 = df[i0:i + 1]
                else:    
                    df1 = df[i0:i]
                i1 = i 
#                print(f"j: {j} i: {i} Variable {df.iloc[i,0]}, lastvar {lastvar}")
                j = j + 1
            elif j == 2:
                if i == (df_length - 1): # end of the dataframe
                    df2 = df[i1:i + 1]
                else:    
                    df2 = df[i1:i]
                i2 = i 
#                print(f"j: {j} i: {i} Variable {df.iloc[i,0]}, lastvar {lastvar}")
                j = j + 1
            elif j == 3:
                if i == (df_length - 1): # end of the dataframe
                    df3 = df[i1:i + 1]
                else:    
                    df3 = df[i2:i]
                i3 = i 
#                print(f"j: {j} i: {i} Variable {df.iloc[i,0]}, lastvar {lastvar}")
                j = j + 1    
            else:  
                logging.error(inspect.stack()[0][3] + " Skipping 5th variable. Can only handle 4 variables. Can be changed!" + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
        
        lastvar = df.iloc[i,1] 
    
    df_merged = mergeData(df0,df1,df2,df3)
           
    return(df_merged)


def loadData(_data):
    tracelist = []
    varfromlist = []
   
    try:
        waterdata = _data['return']['traces']     #TODO: Trap errors
    except LookupError as e:
        logging.error(inspect.stack()[0][3] + " Lookup Error " + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S') + str(e))
        df = pd.DataFrame(columns=["Time","Variable","Value","Quality"],index=["Time"]) # taken from mergeData()
        return df
    else:     
#    print(waterdata)
        for tracesdict in waterdata:    #traces

            variabledata = tracesdict['varfrom_details']['variable']
#            print("variabledata: ", variabledata)

            tracedata = tracesdict['trace']
            if tracedata != []:
#                print("tracedata ", tracedata)
                for tracedict in tracedata:
                
#                    print("tracedict: ", tracedict)
                    fields = [str(tracedict.get('t')),variabledata,str(tracedict.get('v')),str(tracedict.get('q'))] #
                    tracelist.append(fields)
#                print("tracelist: ", tracelist)

#        for x in tracelist:
#            print(x)

        df = pd.DataFrame(tracelist,columns=["Time","Variable","Value","Quality"]) #

        df = splitData(df)

#    print("tracelist",df)

    return df     


        #      tracedict.get('v')


def download_data(download_url):
#    print(download_url)
    data = getResponse(download_url)
    if data == None:
        return False
    else:
         return data    



def write_data(df, meter_no, download_dir):
    
    run_date = datetime.datetime.today()
    ldate = (run_date).strftime('%Y%m%d')    # ldate = logfile date
    
    fname = download_dir + str(meter_no) + "_" + str(ldate) + ".csv"
    df.to_csv(fname)
    return True


   
    