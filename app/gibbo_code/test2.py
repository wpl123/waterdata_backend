import pandas as pd

#df = pd.read_csv("./app/gibbo_code/downloads/203056.csv")
#df[].replace('', np.nan, inplace=True)
#pd.set_option('display.max_rows', 200)
#print(df)

#df1 = pd.DataFrame(cat1,columns=['Textfile','Sub_Header','Cond_Category','Sub_Section'])
#df.to_csv('./app/gibbo_code/downloads/203056_edit.csv',encoding='utf-8',index=False,mode='w') 

df = pd.read_csv("./app/gibbo_code/downloads/203056_edit.csv")
df.drop_duplicates(inplace=True)
df.to_csv('./app/gibbo_code/downloads/203056_edit2.csv',encoding='utf-8',index=False,mode='w')