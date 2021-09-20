import pandas as pd
import numpy as np
import requests
import regex,re
import logging
import glob, os, sys, inspect
from datetime import datetime, date
from contextlib import suppress



workingdir = "/home/admin/dockers/masters/app/"
csv_dir = "/home/admin/dockers/masters/data/csv/"
logs_dir = "/home/admin/dockers/masters/data/code_consents/logs/"
cond_dir = "/home/admin/dockers/masters/data/cond_cat/"
consents_dir = "/home/admin/dockers/masters/data/code_consents/"

df = pd.read_csv(consents_dir +'coded_sub_section.csv',header=0)

df = df.drop(['Textfile','Sub_Header','Cond_Category'],axis=1)
df['Stars]'] = 0

print(df)

for i in range(len(df)):
    if df.iloc[i,1] < .2:
        df.iloc[i,2] = 1
    elif df.iloc[i,1] < .4:
        df.iloc[i,2] = 2
    elif df.iloc[i,1] < .6:
        df.iloc[i,2] = 3
    elif df.iloc[i,1] < .8:
        df.iloc[i,2] = 4
    elif df.iloc[i,1] > .8:
        df.iloc[i,2] = 5            

print(f'{df.loc[1]} {df.loc[2]}')        