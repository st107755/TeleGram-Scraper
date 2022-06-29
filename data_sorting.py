#%% 
import pandas as pd
#import numpy as np
from datetime import datetime
import re
import pdb

data_raw = pd.read_csv('chat.csv',delimiter=';')

#extract important parts Chat1
td = data_raw [["id","text","date"]].copy()
td.dropna(inplace=True)
td.drop(td.tail(1).index,inplace=True)
st1 = td['text'].str.split(' - ', 2,expand=True).copy()
st2=st1[2].str.rsplit(' - ', 1,expand=True).copy()

st1n=st1.drop([2], axis=1)
st2.rename(columns={0: "text"},inplace=True)
st2n=st1n.join(st2["text"])
df1= st2n.join(td[["date","id"]])

ndf1=df1.loc[:,['id']].copy()


#Method to extract the dates and times from chat1
def detect_time_chat1 (df,df_out):
    format_string_dt = "%Y-%m-%d %H:%M:%S+00:00"
    dt_column = []
    for index, row in df.iterrows():
        tmp_time = []
        dt_datetime = ""
        df_date = df.loc[index,'date']
        tmp_time = re.search('\d\d:\d\d',df.loc[index,0])
        
        if tmp_time is None:
            dt_datetime = float("NaN")
        else:
            df_time = tmp_time.group().split(':')
            dt_date = datetime.strptime(df_date, format_string_dt)
            dt_datetime = dt_date.replace(hour=int(df_time[0]),minute=int(df_time[1]),second=0)
            
        dt_column.append (dt_datetime)

    df_out ["datetime"] = dt_column
    return df_out



#Method to detect type of information from chat1
def detect_infotype_chat1 (df,df_out):
    itype_tmp = []
    str_type1 = r"(polizeikontrolle*|verkehrsbeobachtung)"
    str_type2 = r"(blitzer|laser|radar)"
    str_type3 = r"(baustelle|sperrung|verkehrsbehinderung|unfall|panne|defektes fahrzeug|defekter lkw|stau|stockender verkehr|gefahr|fahrbahn|auf straße|einsatz)"
    str_type4 = r"(info|vorab)"

    for index, row in df.iterrows():
        itype_int = ""
        if re.search(str_type4,str(df.loc[index,[0,1]]), re.IGNORECASE):
            itype_int = 4
        elif re.search(str_type1,str(df.loc[index,[0,1]]), re.IGNORECASE):
            itype_int = 1
        elif re.search(str_type2,str(df.loc[index,[0,1]]), re.IGNORECASE):
            itype_int = 2
        elif re.search(str_type3,str(df.loc[index,[0,1]]), re.IGNORECASE):
            itype_int = 3
        else:
            itype_int = 4
        itype_tmp.append(itype_int)
    
    df_out ["infotype"] = itype_tmp
    return df_out

#Method to detect entries with street names from chat1
def detect_streetname_chat1 (df,df_out):
    streetname_tmp = []
    str_streets = r"(straße\b|weg\b|str|platz\b|ring|strasse\b|\Stunnel\b|steige|allee)"

    for index, row in df.iterrows():
        streetname = ""
        #if  re.search(str_streets,str(df.iloc[index,[2,-2]]), re.IGNORECASE):
        if  re.search(str_streets,str(df.iloc[index,2]), re.IGNORECASE):
                streetname = "yes"
        else:
                streetname = "no"
        streetname_tmp.append(streetname)

    df_out ["streetname"] = streetname_tmp
    return df_out


df1.reset_index(drop=True, inplace=True)
ndf2 = detect_time_chat1 (df1,ndf1)
ndf3 = detect_infotype_chat1 (df1,ndf2)
ndf3.reset_index(drop=True, inplace=True)

ndf4 = detect_streetname_chat1 (df1,ndf3)
ndf4.dropna(subset = ["datetime"], inplace=True)
ndf4=ndf4.fillna('')

print(ndf4)
#print(df1) for text with id as shared key
#breakpoint()

###############################################
##Next goals
#make dataframe handling a bit prittier
#method to extract address where streetname=="yes"
#
## final dataframe: 
# columns: id, datetime, infotype(Blitzer,...), streetname(if found),text(?)
###############################################


# %%
