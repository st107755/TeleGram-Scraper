#%% 
import pandas as pd
from datetime import date, time, datetime
import re
import pdb

data = pd.read_csv('chat.csv',delimiter=';')



format_string_dt = "%Y-%m-%d %H:%M:%S+00:00"
format_string_time = "%H:%M Uhr"

date_string = "2022-04-14 12:43:22+00:00"




#extract important parts
td = data [["text","date"]]
td.dropna(inplace=True)
td.drop(td.tail(1).index,inplace=True)
split_text=td['text'].str.split('-',expand=True)
df= split_text.join(td["date"])

#print(df)

for index, row in df.iterrows():
    df_date = df.loc[index,'date']
    #
    #df_time = df.loc[index,0]
    df_time = re.search('\d\d:\d\d',df.loc[index,0]).group()
    df_list = df_time.split(':')
    #pdb.set_trace()

    dt_date = datetime.strptime(df_date, format_string_dt)
    dt_datetime = dt_date.replace(hour=int(df_list[0]),minute=int(df_list[1]),second=0)
    print("date")
    print(dt_date)
    print("new")
    print(dt_datetime)


def detect_time (date,clock):
    pass

##Methode detect_date fertig machen
#Ausnahmen beheben

## dataframe erstellen: Spalten: date, type(Blitzer,...), location






#Method for detecting street names



#Sorting comments into new files depending on the presence of a street name
# %%
