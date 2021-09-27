# http://www.bom.gov.au/jsp/ncc/cdio/wData/wdata?p_nccObsCode=136&p_display_type=dailyDataFile&p_stn_num=054151&p_startYear=
# http://www.bom.gov.au/jsp/ncc/cdio/wData/wdata?p_nccObsCode=136&p_display_type=dailyDataFile&p_stn_num=054021&p_startYear=


import pymysql
import pandas as pd
import numpy as np
from datetime import date
import time
import datetime
import csv


def mysqlconnect(): 
    # To connect MySQL database 

  
    connection = pymysql.connect()
    
    
    try:
        with connection.cursor() as cursor:
                   
                       
            sql1 = ('''  
                    SELECT *
                    FROM `groundwater` AS `A`
                    WHERE `A`.`meter_no` = 'GW967137.1.1' AND `A`.`read_date` < '2020-01-01' AND NOT EXISTS 
                        (SELECT * FROM `rainfall` AS `B` 
                        WHERE `B`.`meter_no` = '54151' AND `B`.`read_date` = `A`.`read_date` AND `B`.`rf_read1` > 0)
                    ''')
            
            
            
        
            df1 = pd.read_sql_query(sql1, connection, coerce_float=True)  # parse_dates=['read_date','%Y-%m-%d'],
            
            # print(df1)
                                    
            fields = []
            mid = 0
            mn = ''
            read_date = ''
            
            rf_read = 0.0
            per_read = 0
            ql_read = 0
            comments='Batch Update'
            localdate = datetime.datetime.now()
            creation_date = localdate.strftime('%Y-%m-%d')
            #df3 = ['id','meter_no','read_date','rf_read1','dy_read1','ql_read1','comments','creation_date']
            
            mid = 56671
            
            with open('formatted_data/correct_54151_rainfall_data.csv', 'w', newline='') as csvfile:
                    
                writer = csv.writer(csvfile,dialect='excel')
               
            
                for i in range(len(df1)):
        
                    sql2 = "SELECT * FROM `rainfall` AS `A` WHERE `A`.`meter_no` = '54021' AND `A`.`read_date` = '{0}' AND `A`.`rf_read1` > 0".format(df1.iloc[i,2])
                                      
                    df2 = pd.read_sql_query(sql2, connection, parse_dates=['read_date','%Y-%m-%d'], coerce_float=True) # 

                    for j in range(len(df2)):
                        
                        
                        mn = '54021'
                        
                        read_date = df2.iloc[j,2].strftime('%Y-%m-%d')
                        
                        rf_read = df2.iloc[j, 3]
                        per_read = df2.iloc[j, 4]
                        ql_read = '401'
                        
                        fields = [mid,mn,read_date,rf_read.round(4),per_read,ql_read,comments,creation_date]
                        
                        writer.writerow(map(lambda x: x, fields))
                        
                        mid = mid + 1 
                        
                        
                        sql3 = "UPDATE `rainfall` WHERE `meter_no` = '54021' AND `A`.`read_date` = '{0}' AND `A`.`rf_read1` > 0".format(df1.iloc[i,2])

         
    except:
        print("Error: unable to convert the data")

    connection.close()
  
# Driver Code 
if __name__ == "__main__" : 
    mysqlconnect()
