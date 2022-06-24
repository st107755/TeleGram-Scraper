#%% 
import pandas as pd
from datetime import date, time, datetime
import re
import pdb

data_raw = pd.read_csv('chat.csv',delimiter=';')

#extract important parts Chat1
td = data_raw [["text","date"]]
td.dropna(inplace=True)
td.drop(td.tail(1).index,inplace=True)
split_text=td['text'].str.split('-',expand=True)
df1= split_text.join(td["date"])


format_string_dt = "%Y-%m-%d %H:%M:%S+00:00"

#Method to extract the dates and times from chat1 and extend dataframe
def detect_time_chat1 (df1,format_string_dt):
    dt_column = []
    for index, row in df1.iterrows():
        tmp_time = []
        df_date = df1.loc[index,'date']
        tmp_time = re.search('\d\d:\d\d',df1.loc[index,0])
        
        if tmp_time is None:
            dt_datetime = ""
        else:
            df_time = tmp_time.group()
            df_list = df_time.split(':')
            dt_date = datetime.strptime(df_date, format_string_dt)
            dt_datetime = dt_date.replace(hour=int(df_list[0]),minute=int(df_list[1]),second=0)
            
        dt_column.append (dt_datetime)

    df1 ["datetime"] = dt_column
    return df1

df = detect_time_chat1 (df1,format_string_dt)
print (df)


##Methode detect_date fertig machen
#Ausnahmen beheben

## dataframe erstellen: Spalten: date, type(Blitzer,...), location
#neuer dataframe?




#Method for detecting street names


#Sorting comments into new files depending on the presence of a street name
# %%
