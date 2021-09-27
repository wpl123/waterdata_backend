
import pymysql
import pandas as pd
import os, glob, datetime, csv
import logging

from datetime import date, timedelta

import dbconfig


def setup_logging(meter_no, logs_dir):

    logfile = logs_dir + "load_" + meter_no + ".log"
    logging.basicConfig(filename=logfile,level=logging.INFO)
    logging.info('Logging started ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))


def normalize_sw_Date(d):
    return '-'.join(((d[15:19]), d[12:14], d[9:11]))


def run_sql_select_1_row(sql1):
    
    connection = pymysql.connect(
        host=dbconfig.host,
        user=dbconfig.user, 
        password=dbconfig.psw,
        database=dbconfig.db_name,
        port=dbconfig.port)

    last_id = 0
       
    with connection.cursor() as cursor:
        logging.info('SQL Select ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
        cursor.execute(sql1)
        result = cursor.fetchall()
        if result[0] == None:
            return(0) # no duplicate   #TODO Try Block
        else:
            return(1) # duplicate
    
    connection.close()

    return(last_id)



def run_sql_insert(sql1):

    connection = pymysql.connect(
        host='192.168.11.6',
        user='root', 
        password='water',
        database='waterdata',
        port=30000)

    last_id = 0
    
    with connection.cursor() as cursor:

        logging.info('SQL Insert ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
        
        cursor.execute(sql1)

        #     df = pd.read_sql_query(sql1, connection, coerce_float=True)  # parse_dates=['read_date','%Y-%m-%d'], 
        
    connection.commit() #TODO - remove all the open and closing
    connection.close()

    return(last_id)


    # df = None
        # if sql_type == "select":
        #     res = cursor.execute(sql1)
        #     # df = pd.read_sql_query(sql1, connection, parse_dates=['read_date','%Y-%m-%d'], coerce_float=True)
        #     print(df)
        #     if df == None:
        #         last_id = 0
        #     else:    
        #         last_id = df.iloc[0,0]
            
        # elif sql_type == "insert":

def surfacewater_format(meter_no, downloads_dir, uploads_dir):
    
    logging.info('Data format started ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
    # print(downloads_dir + meter_no + '*')

    localdate = datetime.datetime.now()
    newdate = ''
    ldate = (datetime.datetime.today() - timedelta(days=1)).strftime('%Y%m%d')

    files = glob.glob(downloads_dir + meter_no + '*') #e.g.  /home/admin/dockers/waterdata_frontend/data/downloads/GQ967137.1.1.*


    formatted_csvfile = uploads_dir + 'fmt_' + meter_no + '_' + ldate + '.csv'

    df1 = pd.concat([pd.read_csv(fp, index_col=False, header=None, skiprows=[0], usecols=[0,1,2,3,4,5], \
        engine='python').assign(meter_no=os.path.basename(fp)) for fp in files])

     
    df1.fillna(value=0,inplace=True)


    df1.round({'3' : 2, '5' : 2, '7' : 2})

    #print(df1.dtypes)
    df1[0] = df1[0].astype(str)  #dt.strftime('%Y-%m-%d')
    
    # initialise variables
    mid = run_sql_select_1_row('''SELECT * FROM surfacewater ORDER BY ID DESC LIMIT 1''') + 1
    mn = ''
    # read_date = ''
    sl_read1 = 0.0
    ql_read1 = 0
    sl_read2 = 0.0
    ql_read2 = 0
    sl_read3 = 0.0
    ql_read3 = 0
    comments='Update'
    creation_date = localdate.strftime('%Y-%m-%d')

    fields = []
    with open(formatted_csvfile, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile,dialect='excel')

        for i in range(len(df1)):
            
            if df1.iloc[i,2] == " ":    # remove blank lines
                continue

            read_date = normalize_sw_Date(df1.iloc[i, 0])
            #read_date = df1.iloc[i, 0]
            sl_read1 = df1.iloc[i, 1]
            ql_read1 = df1.iloc[i, 2]
            sl_read2 = df1.iloc[i, 3]
            ql_read2 = df1.iloc[i, 4]
            mn = df1.iloc[i, 6]
            mid = mid + i

            fields = [mid,mn[:-13],read_date,sl_read1,ql_read1,sl_read2,ql_read2,sl_read3,ql_read3,comments,creation_date]

            writer.writerow(map(lambda x: x, fields))

    #formatted_csvfile.close()
    return(formatted_csvfile)


def load_formatted_sw_data(meter_no, downloads_dir, uploads_dir, formatted_csvfile):

    logging.info('Data load started ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
    
    #         sql = ('''  LOAD DATA LOCAL INFILE '{0} '
    #                     INTO TABLE `surfacewater`
    #                     FIELDS TERMINATED BY ','
    #                     ENCLOSED BY '"'
    #                     LINES TERMINATED BY '\n'
    #                     
    #               ''').format(formatted_csvfile)

    

    df2 = pd.read_csv(formatted_csvfile, index_col=False, header=None, engine='python')

    
    i = 0
    sql2 = ('''SELECT * FROM `surfacewater` WHERE `meter_no` = '{0}' AND `read_date` = {1}''').format(df2.iloc[i,1], df2.iloc[i,2])
    
    sql3 = (''' INSERT 
                INTO `surfacewater` (`id`, `meter_no`, `read_date`, 
                        `sl_read1`, `ql_read1`, `sl_read2`, `ql_read2`, 
                        `sl_read3`, `ql_read3`, `comments`, `creation_date`)
                VALUES ({0}, '{1}', {2}, {3}, {4}, {5}, {6}, {7}, {8}, '{9}', {10})
    ''' ).format(df2.iloc[i,0], df2.iloc[i,1], df2.iloc[i,2], df2.iloc[i,3],df2.iloc[i,4],
        df2.iloc[i,5],df2.iloc[i,6],df2.iloc[i,7],df2.iloc[i,8],df2.iloc[i,9],df2.iloc[i,10])
        
    with open(formatted_csvfile, 'r', newline='') as csvfile:
        
        for i in range(len(df2)):
            
            res = run_sql_select_1_row(sql2)     # check for duplicates
            if result == 0:
                res2 = run_sql_insert(sql3)
                if res2 != 0:
                    logging.error('Insert failed' + " meter_no:" + df2.iloc[i,1] + " date:" + df2.iloc[i,2] + " " + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
            else:
                logging.info('Skipping duplicate id:' + result + " meter_no:" + df2.iloc[i,1] + " date:" + df2.iloc[i,2] + " " + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
                
    return


def surfacewater_load(meter_no, downloads_dir, uploads_dir, logs_dir):

    setup_logging(meter_no, logs_dir)
    formatted_csvfile = surfacewater_format(meter_no, downloads_dir, uploads_dir)
    sw_load = load_formatted_sw_data(meter_no, downloads_dir, uploads_dir, formatted_csvfile)
    # update meter record with the read date

