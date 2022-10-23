#-*- coding: UTF-8 -*- 
import pymysql
import logging
import datetime
import shutil
import os, glob
import pandas as pd

from dbutils import *
from dtutils import *
from flutils import *

def get_meters(mysql):

    sql1 = ('''  SELECT `meter_no`, `meter_name`, `meter_type`, `meter_lat` AS `lat`, `meter_long` AS `lon`, `download_url` AS `url`, `get_data` FROM `meters` ''')
    result = mysql.execQuery(sql1)
    return(result)

def get_meter_name(mysql):

    sql1 = ('''  SELECT `meter_no`, `meter_name`, `meter_type`, `meter_lat` AS `lat`, `meter_long` AS `lon`, `get_data` FROM `meters` ''')
    result = mysql.execQuery(sql1)
    return(result)


def get_meter_data(mysql, meter, mtype):

    sdate = '2008-01-01'    #TODO
    today = datetime.datetime.today()       # - timedelta(days=1)
    edate = (today).strftime('%Y-%m-%d')  # edate == today
      
    mdf = []

    if mtype == 11:
        mdf = pd.DataFrame(get_surfacewater(mysql, meter, sdate, edate))
    elif mtype == 12:
        mdf = pd.DataFrame(get_groundwater(mysql, meter, sdate, edate))
    elif mtype == 13:
        mdf = pd.DataFrame(get_groundwater(mysql, meter, sdate, edate))
    elif mtype == 4:
        mdf = pd.DataFrame(get_rainfall(mysql, meter, sdate, edate))
    else:
        mdf = None
        pass

    return (mdf)



def get_groundwater(mysql,meter,s_date,e_date):

    sql2 = ('''  SELECT 
                    `A`.`meter_no` AS `meter_no`, `A`.`read_date` AS `read_date_idx`, 
                    `B`.`read_date` AS `read_date`,`A`.`bl_ahd` AS `level`                    
                FROM   
                    `groundwater` AS `A`  
                INNER JOIN
                    `groundwater` `B` ON (`B`.`meter_no` = '{0}' AND `B`.`read_date` = `A`.`read_date` )
                WHERE  
                    `A`.`meter_no` = '{0}' AND `A`.`read_date` >= '{1}' AND `A`.`read_date` <= '{2}'
                '''.format(meter,s_date,e_date))


    sql2_1 = (''' SELECT `meter_no`, `read_date1, `bl_ahd` AS `level` 
                FROM `groundwater`         
                WHERE `meter_no` = '{0}' AND `read_date` >= '{1}' AND `read_date` <= '{2}'
                '''.format(meter,s_date,e_date))
                
    result = mysql.execQuery(sql2)
    return(result)



def get_surfacewater(mysql,meter,s_date,e_date):
    
    sql3 = ('''  SELECT 
                    `A`.`meter_no` AS `meter_no`, `A`.`read_date` AS `read_date_idx`, 
                    `B`.`read_date` AS `read_date`,`A`.`sl_read1` AS `level`                    
                FROM   
                    `surfacewater` AS `A`  
                INNER JOIN
                    `surfacewater` `B` ON (`B`.`meter_no` = '{0}' AND `B`.`read_date` = `A`.`read_date` )
                WHERE  
                    `A`.`meter_no` = '{0}' AND `A`.`read_date` >= '{1}' AND `A`.`read_date` <= '{2}'
                '''.format(meter,s_date,e_date))
    
    result = mysql.execQuery(sql3)
    return(result)




def get_simple_surfacewater(mysql,meter,s_date,e_date):
    
    
    sql3_1 = (''' SELECT `meter_no`, `read_date`,  `sl_read1` AS `level` 
                FROM `surfacewater`         
                WHERE `meter_no` = '{0}' AND `read_date` >= '{1}' AND `read_date` <= '{2}'
                '''.format(meter,s_date,e_date))
    
    result = mysql.execQuery(sql3_1)
    return(result)



def get_rainfall(mysql,meter,s_date,e_date):

    sql4 = ('''  SELECT 
                    `A`.`meter_no` AS `meter_no`, `A`.`read_date` AS `read_date_idx`,
                    `A`.`read_date` AS `read_date`, 
                    `A`.`rf_read1` AS `level`                    
                FROM   
                    `rainfall` AS `A`  
                WHERE  
                    `A`.`meter_no` = '{0}' AND `A`.`read_date` >= '{1}' AND `A`.`read_date` <= '{2}'
                '''.format(meter,s_date,e_date))
    
    result = mysql.execQuery(sql4)
    return(result)
    



def get_simple_rainfall(mysql,meter,s_date,e_date):

    sql4_1 = (''' SELECT `meter_no`, `read_date`, `rf_read1` AS `level` 
                FROM `rainfall`         
                WHERE `meter_no` = '{0}' AND `read_date` >= '{1}' AND `read_date` <= '{2}'
                '''.format(meter,s_date,e_date))
    
    result = mysql.execQuery(sql4_1)
    return(result)




# create the function
def df_to_geojson(dfj, properties, lat='latitude', lng='longitude'): #

    # print(dfj)
    # print(properties)
    # print(lat, lng)
    """
    Turn a dataframe containing point data into a geojson formatted python dictionary

    dfj : the dataframe to convert to geojson
    properties : a list of columns in the dataframe to turn into geojson feature properties
    lat : the name of the column in the dataframe that contains latitude data
    lng : the name of the column in the dataframe that contains longitude data
    """

    # create a new python dict to contain our geojson data, using geojson format
    geojson = {'type':'FeatureCollection', 'features':[]}

    # loop through each row in the dataframe and convert each row to geojson format
    # x is the equivalent of the row, df.iterrows converts the dataframe in to a pd.series object
    # the x is a counter and has no influence
    for x, row in dfj.iterrows():

        feature = {'type':'Feature',
                   'properties':{},
                   'geometry':{'type':'Point',
                               'coordinates':[]}}

        # fill in the coordinates
        feature['geometry']['coordinates'] = [float(row.lng),float(row.lat)]

        # be aware that the dataframe is a pd.series
        #print('rowitem converts to ndarray(numpy) :\n ', row)
        # convert the array to a pandas.serie
        geo_props = pd.Series(row)

        # for each column, get the value and add it as a new feature property
        # prop determines the list from the properties
        for prop in properties:

            #loop over the items to convert to string elements

            #convert to string
            if type(geo_props[prop]) == float:
                #print('ok')
                geo_props[prop] = str(int(geo_props[prop]))

            # now create a json format, here we have to make the dict properties
            feature['properties'][prop] = geo_props[prop]

        # add this feature (aka, converted dataframe row) to the list of features inside our dict
        geojson['features'].append(feature)
    return geojson


