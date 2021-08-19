# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import glob, os
import time
import datetime
import csv


localdate = datetime.datetime.now()
meter_no = ''
newdate = ''

def normalizeDate(d):
    return '-'.join((d[15:19], d[12:14], d[9:11]))


files = glob.glob("unformatted_data/GW_2col/GW*")

df1 = pd.concat([pd.read_csv(fp, index_col=False, header=None, skiprows=[0,1,2,3,4], usecols=[0,1,2,3,4]     ).assign(meter_no=os.path.basename(fp)) for fp in files])

df1.fillna(value=0,inplace=True)


#initialise variables
mid = None
mn = ''
read_date = ''
bl_bmp = 0.0
ql_bmp = 0
bl_ahd = 0.0
ql_ahd = 0
mean_temp = 0.0
ql_temp = 0
comments='Initial load'
creation_date = localdate.strftime('%Y-%m-%d')

fields = []
with open('formatted_data/fmt_2col_bore_data.csv', 'a', newline='') as csvfile:
    writer = csv.writer(csvfile,dialect='excel')

    for i in range(len(df1)):

        read_date = normalizeDate(df1.iloc[i, 0])
        bl_bmp = df1.iloc[i, 1]
        ql_bmp = df1.iloc[i, 2]
        bl_ahd = df1.iloc[i, 3]
        ql_ahd = df1.iloc[i, 4]
        mn = df1.iloc[i, 5]
        mid = i

        fields = [mid,mn[:12],read_date,bl_bmp.round(4),ql_bmp.round(),bl_ahd.round(4),ql_ahd.round(),mean_temp,ql_temp,comments,creation_date]

        writer.writerow(map(lambda x: x, fields))


# %%



# %%



# %%



# %%



# %%



# %%



