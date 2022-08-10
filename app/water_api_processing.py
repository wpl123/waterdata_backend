import pymysql
import pandas as pd
import numpy as np
import sys, webbrowser
import csv, time 
import datetime
import inspect
import requests
import json

from datetime import timedelta
from decimal import Decimal

#from wrapper_api_load import logger
from dbutils import *
from flutils import *
from dtutils import *



def make_sql1(tablename,meter_no,read_date):
    
    sql1 = ('''SELECT * FROM `{0}` WHERE `meter_no` = '{1}' AND `read_date` = '{2}' ''').format(tablename, meter_no, read_date)

    return sql1



def make_sql2(tablename,operation,meter_no,read_date,calc_id,variable,level,quality):
    
    sql2 = ""
    comments  = "Automated Load No 1"
    comments2 = "Automated Load No 2"
    creation_date = datetime.datetime.today().strftime("%Y-%m-%d")
    
    if tablename == "surfacewater":
        
        if operation == "INSERT":
            if variable == "100.00":    
                sql2 = (''' INSERT 
                    INTO `surfacewater` (`id`, `meter_no`, `read_date`, 
                            `sl_read1`, `ql_read1`, `sl_read2`, `ql_read2`, 
                            `sl_read3`, `ql_read3`, `comments`, `creation_date`)
                    VALUES ({0}, '{1}', '{2}', {3}, '{4}', {5}, '{6}', {7}, '{8}', '{9}', '{10}')
                    ''' ).format(calc_id, meter_no, read_date, level[0], quality[0],level[1], quality[1],level[2], quality[2],comments, creation_date)
            else:
                write_log('ERROR: Surface water Variable ' + variable + ' was not able to be handled on INSERT')
        else: #operation = "UPDATE"
            if variable == "100.00":        
                sql2 = (''' UPDATE `surfacewater` 
                        SET  
                            `sl_read1` = {0}, `ql_read1` = '{1}', `sl_read2` = {2}, `ql_read2` = '{3}', 
                            `sl_read3` = {4}, `ql_read3` = '{5}', `comments` ='{6}', `creation_date` = '{7}'
                        WHERE `meter_no` = '{8}' AND `read_date` = '{9}'    
                    ''' ).format(level[0], quality[0],level[1], quality[1],level[2], quality[2],comments2, creation_date, meter_no,read_date)
            else:
                write_log('ERROR: Surface water Variable ' + variable + ' was not able to be handled on UPDATE')    
        
            
    elif tablename == "groundwater":  
        if operation == "INSERT":
            
            if variable == "110.00":
                
                sql2 = (''' INSERT 
                    INTO `groundwater` (`id`, `meter_no`, `read_date`, 
                            `bl_bmp`, `ql_bmp`, `bl_ahd`, `ql_ahd`, 
                            `comments`, `creation_date`)
                    VALUES ({0}, '{1}', '{2}', {3}, '{4}', {5}, '{6}', '{7}', '{8}')
                    ''' ).format(calc_id, meter_no, read_date, level[0], quality[0],level[1], quality[1],comments, creation_date)
        
            elif variable == "2080.00":    
                sql2 = (''' INSERT 
                    INTO `groundwater` (`id`, `meter_no`, `read_date`, 
                            `mean_temp`, `ql_temp`, `comments`, `creation_date`)
                    VALUES ({0}, '{1}', '{2}', {3}, '{4}', '{5}', '{6}')
                    ''' ).format(calc_id, meter_no, read_date, level[2], quality[2],comments, creation_date)
            else:
                write_log('ERROR: Groundwater Variable ' + variable + ' was not able to be handled on INSERT')
                
        else: #operation = "UPDATE"
                
            if variable == "110.00":
                
                sql2 = (''' UPDATE `groundwater` 
                        SET  
                            `bl_bmp` = {0}, `ql_bmp` = '{1}', `bl_ahd` = {2}, `ql_ahd` = '{3}', 
                            `comments` = '{4}', `creation_date` = '{5}'
                        WHERE `meter_no` = '{6}' AND `read_date` = '{7}'
                    ''' ).format(level[0], quality[0],level[1], quality[1],comments2, creation_date,meter_no,read_date)
            elif variable == "2080.00":
                sql2 = (''' UPDATE `groundwater` 
                        SET  
                            `mean_temp` = {0}, `ql_temp` = '{1}', `comments` = '{2}', `creation_date` = '{3}'
                        WHERE `meter_no` = '{4}' AND `read_date` = '{5}'    
                    ''' ).format(level[2], quality[2],comments2, creation_date, meter_no,read_date)
            else:
                write_log('ERROR: Groundwater Variable ' + variable + ' was not able to be handled on UPDATE')    
          
    
    return sql2



def make_sql3(meter_no):
   
    download_date = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    
    sql3 = ''' UPDATE `{0}` SET `last_download` =  '{2}' WHERE `meter_no` = '{1}' ORDER BY `last_download` DESC LIMIT 1 '''.format("meters", meter_no,download_date)

    return sql3



def load_surfacewater_data(mysql,meter_no,df2):

    write_log('Database load for ' + meter_no + 'started')
    
    for i in range(len(df2)):
        
        _read_date = normalize_sw_Date(str(df2.iloc[i,0]))
        _calc_id   = 0
        _variable  = str(df2.iloc[i,1])
        _level     = []
        _quality   = []
        _sl_read   = df2.iloc[i,2]
        _ql_read   = df2.iloc[i,3]
        
        if _variable == "100.00":    # Update different parts of the record based on the JSON variable returned
            _level     = [df2.iloc[i,2],0,0]
            _quality   = [df2.iloc[i,3],0,0]   
        else:
            write_log('ERROR: Surfacewater Variable ' + _variable + ' was not able to be handled')    
          
        
        sql1   = make_sql1("surfacewater",meter_no,_read_date)
        dup = getDuplicate(mysql, sql1)      # check for duplicates
        
        if dup == None:
            _calc_id = lastID(mysql, "surfacewater") + 1
            sql2     = make_sql2("surfacewater","INSERT",meter_no,_read_date,_calc_id, _variable, _level, _quality) 

            result2 = mysql.execSQL(sql2)          # insert row
            if result2 == False:
                write_log('Insert failed for meter_no:' + meter_no + " date: " + str(df2.iloc[i,0]))
        else:   
            
            #Check if contents of duplicate_record are the same as the latest readings (can change due to NSW Water sanity checks)
            # if they are then skip the UPDATE
            
            if _variable == "100.00" and str(dup[3]) == _sl_read and str(dup[4]) == _ql_read: 
                continue
            
            sql2     = make_sql2("surfacewater","UPDATE",meter_no,_read_date,_calc_id, _variable, _level, _quality) 

            result2 = mysql.execSQL(sql2)          # insert row
            if result2 == False:
                write_log('Insert failed for meter_no:' + meter_no + " date: " + str(df2.iloc[i,0]))
        
        sql3 = make_sql3(meter_no)
        result3 = mysql.execSQL(sql3)
        
        write_log('Database load for ' + meter_no + ' completed ') 
                
    return


    
def load_groundwater_data(mysql,meter_no,df2):
    
    write_log('Database load started for ' + meter_no)
    
    _elevation = 0.0
    _bl_bmp    = 0.0
    
    sql = ('''SELECT `meter_elev` FROM `meters` WHERE `meter_no` = '{0}' ''').format(meter_no)
    result = mysql.execOne(sql)
    _elevation = result[0]  #get the elevation from the tuple

    for i in range(len(df2)):
        
        _read_date = normalize_sw_Date(str(df2.iloc[i,0]))
        _calc_id   = 0
        _level     = []
        _quality   = []
        _variable  = str(df2.iloc[i,1])
        _bl_bmp    = Decimal(df2.iloc[i,2])                  # convert the df groundwater level to a decimal
        _bl_ahd    = _elevation - _bl_bmp
        _ql_ahd    = df2.iloc[i,3]
                
        if _variable == "110.00":                    # Update different parts of the record based on the JSON variable returned
            _level     = [df2.iloc[i,2],_bl_ahd,0]
            _quality   = [df2.iloc[i,3],_ql_ahd,0]
        elif _variable == "2080.00":
            _level     = [0,0,df2.iloc[i,2]]
            _quality   = [0,0,df2.iloc[i,3]]
        else:
            write_log('ERROR: Groundwater Variable ' + _variable + ' was not able to be handled')

        sql1   = make_sql1("groundwater",meter_no,_read_date)
        dup    = getDuplicate(mysql, sql1)      # check for duplicates
            
        if dup == None:
            _calc_id = lastID(mysql, "groundwater") + 1
            sql2     = make_sql2("groundwater", "INSERT", meter_no,_read_date,_calc_id, _variable, _level, _quality) 
        
            result2 = mysql.execSQL(sql2)          # insert row
            if result2 == False:
                write_log('Insert failed for meter_no: ' + meter_no + " date: " + str(df2.iloc[i,0]))
        else:           
            
            #Check if contents of duplicate_record are the same as the latest readings (can change due to NSW Water sanity checks)
            # if they are then skip the UPDATE
            
            if _variable == "110.00" and str(dup[3]) == _bl_ahd and str(dup[4]) == _ql_ahd: 
                continue
            #TODO: Get this working for temp
            
            sql2     = make_sql2("groundwater","UPDATE",meter_no,_read_date,_calc_id, _variable, _level, _quality) 

            result2 = mysql.execSQL(sql2)          # insert row
            if result2 == False:
                write_log('Insert failed for meter_no: ' + meter_no + " date: " + str(df2.iloc[i,0]))
        
        
        sql3 = make_sql3(meter_no)
        result3 = mysql.execSQL(sql3) 
                
    return




def load_JSON(_data,_meter_no,_tablename):
    tracelist = []
    
    mysql = MySQLUtil()
    mysql.dbConnect()
    
    try:
        waterdata = _data['return']['traces']     #TODO: Trap errors
    except LookupError as e:
        write_log("Lookup Error " + str(e))
        # df = pd.DataFrame(columns=["Time","Variable","Value","Quality"],index=["Time"]) # taken from mergeData()
        # return df
        quit()
    except TypeError as e:
        write_log("Type Error " + str(e))
        #df = pd.DataFrame(columns=["Time","Variable","Value","Quality"],index=["Time"]) # taken from mergeData()
        #return df
        quit()
    else:     
#    print(waterdata)
        # logger.info(inspect.stack()[0][3] + " Data Returned " + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S') + "\n\n" + str(waterdata))
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
        
        if _tablename == "groundwater":  
            result = load_groundwater_data(mysql,_meter_no,df)
        elif _tablename == "surfacewater":   
            result = load_surfacewater_data(mysql,_meter_no,df) 
    
    mysql.dbClose()
    return df     


      
def getResponse(url):
    try:  
        response = requests.get(url)
    except requests.exceptions.HTTPError as errh:
        write_log('Http error: ' + str(errh))
        return None
    except requests.exceptions.ConnectionError as errc:
        write_log('Error Connecting: ' + str(errc))
        return None
    except requests.exceptions.Timeout as errt:
        write_log('Timeout Error: ' + str(errt))
        return None
    except requests.exceptions.RequestException as err:
        write_log('OOps: Something Else: ' + str(err))
        return None

    jsonData = response.json() 
    if response and response.status_code == 200:
        return jsonData
    else:
        write_log("Error receiving data: " + response.status_code)
        return None


def download_apidata(download_url):
#    print(download_url)
    data = getResponse(download_url)
#    if data == None:
#        return data
#    else:
    return data    


def execute_api(url, meter_no, download_dir, tablename): 
    
    write_log('Launching API for meter ' + meter_no)
    result = False
    
    df = pd.DataFrame()  #(columns=['v','t','q'])
    df1 = pd.DataFrame() #(columns=['v','t','q'])
    
    data = download_apidata(url)
    if data == None:
        write_log('ERROR: No JSON data for meter ' + meter_no)
        result = False   # Do somethng else
    else:
        write_log('Returning JSON data for meter ' + meter_no)
        df = load_JSON(data,meter_no,tablename) 
        df1 = df1.append(df, ignore_index=True)
        #result = write_csv_data(df1, meter_no, download_dir)   # Unhash for testing
    
    write_log('Completed API processing for meter ' + meter_no)    
    
    return df1

