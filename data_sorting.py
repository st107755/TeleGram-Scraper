#%% 
import pandas as pd
import numpy as np
from datetime import date, time, datetime
import re
import pdb

data_raw = pd.read_csv('chat.csv',delimiter=';')

#extract important parts Chat1
td = data_raw [["text","date"]].copy()
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
        dt_datetime = ""
        df_date = df1.loc[index,'date']
        tmp_time = re.search('\d\d:\d\d',df1.loc[index,0])
        
        if tmp_time is None:
            dt_datetime = float("NaN")
        else:
            df_time = tmp_time.group().split(':')
            dt_date = datetime.strptime(df_date, format_string_dt)
            dt_datetime = dt_date.replace(hour=int(df_time[0]),minute=int(df_time[1]),second=0)
            
        dt_column.append (dt_datetime)

    df1 ["datetime"] = dt_column
    df1.dropna(subset = ["datetime"], inplace=True)
    return df1


##method to detect infotype
##in progress
itype_tmp = []
str_type1 = "r'(polizeikontrolle|verkehrsbeobachtung)'"
str_type2 = "r'(blitzer|laser)"
str_type3 = "r'(baustelle|sperrung|verkehrsbehinderung|unfall|panne|defektes fahrzeug|stau|stockender verkehr|gefahr|fahrbahn|auf straße|einsatz)"

#print(type(df1[1][1]))
#pl=re.match(str_type1, df1[2][1],re.IGNORECASE)
pl=re.match(str_type1, "verkehrsbeobachtung",re.IGNORECASE)
pl1 = pl.group()
print(pl1)
breakpoint()
df1.loc[df1[1][1].match(str_type1, re.IGNORECASE)]
breakpoint()

for index, row in df1.iterrows():
    if df1.loc[df1[index,1].str.match(str_type1, re.IGNORECASE)] is True:
        breakpoint()
        itype_int = 1
    elif df1.loc[df1[index,1].str.match(str_type2, re.IGNORECASE)] is True:
        itype_int = 2
    elif df1.loc[df1[index,1].str.match(str_type3, re.IGNORECASE)] is True:
        itype_int = 3
    else:
        itype_int = float("NaN")
    itype_tmp.append (itype_int)

print (itype_tmp)

def detect_infotype ():
    pass




#df = detect_time_chat1 (df1,format_string_dt)
#print(df)




#breakpoint()

##Methode detect_date fertig machen
#Ausnahmen beheben

## dataframe erstellen: Spalten: date, type(Blitzer,...), location
#neuer dataframe?


#Method for detecting street names


#Sorting comments into new files depending on the presence of a street name
# %%
