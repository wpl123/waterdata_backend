import pymysql
import os, sys, glob, datetime, csv
import logging

import numpy as np
import pandas as pd
import sklearn
import tensorflow as tf

from tensorflow import keras
from pylab import rcParams
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler
from pandas.plotting import register_matplotlib_converters

from datetime import date, timedelta

#https://stackoverflow.com/questions/1260792/import-a-file-from-a-subdirectory#%E2%80%A6
sys.path.extend([f'./{name}' for name in os.listdir(".") if os.path.isdir(name)])

from args_utils import *
from ml_dbutils import *
from dbutils import *
from flutils import *

RANDOM_SEED = 42

np.random.seed(RANDOM_SEED)
tf.random.set_seed(RANDOM_SEED)


def get_data(mysql):
    
    # df = df.drop(['bl_meter1','bl_ahd1','bl_meter2','bl_ahd2','bl_meter3','bl_ahd3','mean_temp3','bl_meter4','bl_ahd4','mean_temp4','sl_meter','rf_meter'],axis=1)
    meters = pd.DataFrame(get_meters(mysql), columns=['meter_no','meter_name','meter_type','lat','lng', 'url'])
    #df = pd.concat([get_meter_data(mysql, meters.iloc[i,0], meters.iloc[i,2]) for i in range(len(meters))])
    df = pd.concat([get_meter_data(mysql, meters.iloc[i,0], meters.iloc[i,2]) for i in range(len(meters))])
    df.columns = ['meter_no','read_date_idx','read_date','level']
    df['read_date_idx'] = pd.to_datetime(df['read_date_idx'])
    df.set_index('read_date_idx',inplace=True,drop=True)
    
    return df


def get_meter_list(meters_to_model):
    
    for _meters in meters_to_model:
        _meter = _meters.split(',')
    return _meter


def surfacewaterFormat(mysql, _meter_args, _logs_args):
    #meter_no, model_name, meters_to_model
    _meter_no            = split_args(_meter_args,1,2)        # get meter_no from the 
    _meters_to_model     = _meter_args[11:12]      # i.e the params field with meters to model
    
    _meter = get_meter_list(_meters_to_model)
        
    for m in _meter:
        df = get_data(mysql,m)
        df1 = df1.append(df)
        
    
    return(df1)


def create_dataset(X, y, time_steps=1):
        Xs, ys = [], []
        for i in range(len(X) - time_steps):
            v = X.iloc[i:(i + time_steps)].values
            Xs.append(v)        
            ys.append(y.iloc[i + time_steps])
        return np.array(Xs), np.array(ys)


def model_run(df):

    #df = pd.read_csv(formatted_csvfile,parse_dates=['read_date'],index_col="read_date")

    df = df.drop(['bl_meter1','bl_ahd1','bl_meter2','bl_ahd2','bl_meter3','bl_ahd3','mean_temp3','bl_meter4','bl_ahd4','mean_temp4','sl_meter','rf_meter'],axis=1)

    train_size = int(len(df) * 0.75)
    test_size = len(df) - train_size
    train, test = df.iloc[0:train_size], df.iloc[train_size:len(df)]

    f_columns = ['rf_read1']

    f_transformer = RobustScaler()
    sl_transformer = RobustScaler()

    f_transformer = f_transformer.fit(train[f_columns].to_numpy())
    sl_transformer = sl_transformer.fit(train[['sl_read1']])

    train.loc[:, f_columns] = f_transformer.transform(train[f_columns].to_numpy())
    train['sl_read1'] = sl_transformer.transform(train[['sl_read1']])

    test.loc[:, f_columns] = f_transformer.transform(test[f_columns].to_numpy())
    test['sl_read1'] = sl_transformer.transform(test[['sl_read1']])

    time_steps = 10

    # reshape to [samples, time_steps, n_features]

    X_train, y_train = create_dataset(train, train.sl_read1, time_steps)
    X_test, y_test = create_dataset(test, test.sl_read1, time_steps)

    model = keras.Sequential()
    model.add(
      keras.layers.Bidirectional(
        keras.layers.LSTM(
          units=128, 
          input_shape=(X_train.shape[1], X_train.shape[2])
        )
      )
    )
    model.add(keras.layers.Dropout(rate=0.2))
    model.add(keras.layers.Dense(units=1))
    model.compile(loss='mean_squared_error', optimizer='adam')


    history = model.fit(
        X_train, y_train, 
        epochs=40, 
        batch_size=32, 
        validation_split=0.1,
        shuffle=False
    )


    y_pred = model.predict(X_test)

    y_train_inv = sl_transformer.inverse_transform(y_train.reshape(1, -1))
    y_test_inv = sl_transformer.inverse_transform(y_test.reshape(1, -1))
    y_pred_inv = sl_transformer.inverse_transform(y_pred)

    fname = '/home/jovyan/work/training_data/sw_modelled_training_data.csv'
    np.savetxt(fname, y_pred_inv, fmt='%f', delimiter=' ', newline='\n', header='sf_read1', footer='', comments='', encoding=None)

    sw_load = None
    return(sw_load)




def sw_load_model_data(mysql, meter_no, downloads_dir, uploads_dir, formatted_csvfile):
    return None


def surfacewaterModel(meter_args, logs_args):
        
    
    meter_no            = split_args(meter_args,1,2)        # get meter_no from the 
    downloads_dir       = split_args(logs_args,0,1)
    uploads_dir         = split_args(logs_args,1,2)
    
    #meter = meters.split(',')
    
    #setupLogging(meter_no, logs_dir)
    
    mysql = MySQLUtil()
    mysql.dbConnect()
    #mysql.dbConnect(host ='192.168.11.6', user = 'root', psw = 'water', db_name = 'waterdata', port=30000)
    
    
    df = surfacewaterFormat(mysql, meter_args, logs_args)
    print(df)
   
    
    if df.empty != True:
        
        sw_model = model_run(df)
        sw_load = loadSWFormatted(mysql, meter_no, downloads_dir, uploads_dir, formatted_csvfile)
        upd_meter = updateMeter(mysql, meter_no)     # update meter record with the read date
        
        download_hist = downloads_dir + 'download_hist'  #TODO:
        upload_hist   = uploads_dir + 'upload_hist'
        download_file = downloads_dir + meter_no + '*'
        upload_file   = formatted_csvfile
    
        move_download = moveFile(download_file, download_hist) # move formatted file and uploaded file to a new directory download_hist and upload_hist subdirectory
        move_upload   = moveFile(upload_file, upload_hist) # move formatted file and uploaded file to a new directory download_hist and upload_hist subdirectory
    else:
        logging.error(' No download file for ' + meter_no + ' ' + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))

    mysql.dbClose()