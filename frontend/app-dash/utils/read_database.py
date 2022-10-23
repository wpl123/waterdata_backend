
from dbutils import *
from flutils import *
from dash_dbutils import *


def read_meters():
    mysql = MySQLUtil()
    mysql.dbConnect()
    meters = pd.DataFrame(get_meters(mysql), columns=['meter_no','meter_name','meter_type','lat','lon', 'url', 'get_data'])
    mysql.dbClose
    return meters   


    
def read_db():
    mysql = MySQLUtil()
    mysql.dbConnect()
    # All Meter Data
    meters = pd.DataFrame(get_meters(mysql), columns=['meter_no','meter_name','meter_type','lat','lng', 'url', 'get_data'])
    df = pd.concat([get_meter_data(mysql, meters.iloc[i,0], meters.iloc[i,2]) for i in range(len(meters))])
    mysql.dbClose
    
    df.columns = ['meter_no','read_date_idx','read_date','level']
    df['read_date_idx'] = pd.to_datetime(df['read_date_idx'])
    df.set_index('read_date_idx',inplace=True,drop=True)
        
    return meters, df