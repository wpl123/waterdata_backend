import pandas as pd

def df_split(df):

# meter_no_x_x read_date_x_x  level_x_x  meter_no_y_x read_date_y_x  level_y_x meter_no_x_y read_date_x_y  level_x_y meter_no_y_y read_date_y_y  level_y_y    
    fields1 = []
    fields2 = []
    fields3 = []
    
    for i in range(len(df)):
        
        row1 = [df.iloc[i,0],df.iloc[i,1],df.iloc[i,2],df.iloc[i,3],df.iloc[i,4],df.iloc[i,5]]
        row2 = [df.iloc[i,6],df.iloc[i,7],df.iloc[i,8]]
        row3 = [df.iloc[i,9],df.iloc[i,10],df.iloc[i,11]]
        
        fields1.append(row1)
        fields2.append(row2)
        fields3.append(row3)
    

    df1 = pd.DataFrame(fields1,columns=['meter_no_x', 'read_date_x', 'level_x', 'meter_no_y', 'read_date_y', 'level_y'])
    df2 = pd.DataFrame(fields2,columns=['meter_no', 'read_date', 'level'])
    df3 = pd.DataFrame(fields3,columns=['meter_no', 'read_date', 'level'])
    
    return df1, df2, df3
    #return fields1, fields2, fields3  