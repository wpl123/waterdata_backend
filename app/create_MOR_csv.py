#connect to database

import pymysql
import pandas as pd
import numpy as np
import csv



#def mysqlconnect(): 
    # To connect MySQL database 

  
connection = pymysql.connect(
    # host='192.168.208.1',
    host='192.168.11.6',
    user='root', 
    password='water',
    database='waterdata',
    port=30000)


try:
    with connection.cursor() as cursor:
               
        
        
        sql = ('''  SELECT 
                        `A`.`read_date`, 
                        `A`.`meter_no` AS `bl_meter1`, `A`.`bl_ahd` AS `bl_ahd1`, `A`.`mean_temp` AS `mean_temp1`,
                        `B`.`meter_no` AS `bl_meter2`, `B`.`bl_ahd` AS `bl_ahd2`, `B`.`mean_temp` AS `mean_temp2`,
                        `E`.`meter_no` AS `bl_meter3`, `E`.`bl_ahd` AS `bl_ahd3`, `E`.`mean_temp` AS `mean_temp3`,
                        `F`.`meter_no` AS `bl_meter4`, `F`.`bl_ahd` AS `bl_ahd4`, `F`.`mean_temp` AS `mean_temp4`,
                        `C`.`meter_no` AS `meter_no3`, `C`.`sl_read1` AS `sl_read1`,
                        `D`.`meter_no` AS `meter_no4`, `D`.`rf_read1` AS `rf_read1`
                    FROM   
                        `groundwater` AS `A`  
                    INNER JOIN
                        `groundwater` `B` ON (`B`.`meter_no` = "GW967137.2.2" AND `B`.`read_date` = `A`.`read_date` )
                    INNER JOIN
                        `groundwater` `E` ON (`E`.`meter_no` = "GW967138.1.1" AND `E`.`read_date` = `A`.`read_date` )
                    INNER JOIN
                        `groundwater` `F` ON (`F`.`meter_no` = "GW967138.2.2" AND `F`.`read_date` = `A`.`read_date` )
                    INNER JOIN
                        `surfacewater` `C` ON (`C`.`meter_no` = "CF419051" AND `C`.`read_date` = `A`.`read_date` )
                    INNER JOIN
                        `rainfall` `D` ON (`D`.`meter_no` = "54151" AND `D`.`read_date` = `A`.`read_date` )
                    WHERE  
                        `A`.`meter_no` = "GW967137.1.1" AND `A`.`read_date` NOT BETWEEN '2008-01-31' AND '2008-09-01'
                            AND `A`.`read_date` NOT BETWEEN '2020-12-13' AND '2021-01-01'
                    ''')
        
        
    
    df1 = pd.read_sql_query(sql, connection, parse_dates=['read_date','%Y-%m-%d'], coerce_float=True)   # parse_dates=['read_date','%Y-%m-%d'],
    
   
except:
    print("Error: unable to convert the data")
    
connection.close()   
    


df1['bl_ahd1'] = pd.to_numeric(df1['bl_ahd1'])
df1['bl_ahd2'] = pd.to_numeric(df1['bl_ahd2'])

df1['mean_temp1'] = pd.to_numeric(df1['mean_temp1'])
df1['mean_temp2'] = pd.to_numeric(df1['mean_temp2'])

df1['bl_ahd3'] = pd.to_numeric(df1['bl_ahd3'])
df1['bl_ahd4'] = pd.to_numeric(df1['bl_ahd4'])

df1['mean_temp3'] = pd.to_numeric(df1['mean_temp3'])
df1['mean_temp4'] = pd.to_numeric(df1['mean_temp4'])

df1['sl_read1'] = pd.to_numeric(df1['sl_read1'])
df1['rf_read1'] = pd.to_numeric(df1['rf_read1'])


all_training_data = 'data/waterdata/sw_training_data.csv'

with open(all_training_data, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile,dialect='excel')
        
        fields = ['read_date','sl_read1','bl_ahd1','bl_ahd2','rf_read1','mean_temp1','mean_temp2','bl_meter3','bl_ahd3','mean_temp3','bl_meter4','bl_ahd4','mean_temp4','sl_meter','rf_meter'] 
        
        writer.writerow(fields)

        for i in range(len(df1)):
            

            row = [df1.iloc[i,0],df1.iloc[i,14],df1.iloc[i,1], df1.iloc[i,2],df1.iloc[i,3],df1.iloc[i,4],df1.iloc[i,5],
            df1.iloc[i,6],df1.iloc[i,7],df1.iloc[i,8],df1.iloc[i,9],df1.iloc[i,10],
            df1.iloc[i,11],df1.iloc[i,12],df1.iloc[i,13],df1.iloc[i,15],df1.iloc[i,16]]
            


            writer.writerow(map(lambda x: x, row))