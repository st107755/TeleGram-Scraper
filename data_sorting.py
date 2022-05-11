#%% 
import pandas as pd
data = pd.read_csv('chat.csv',delimiter=';')

#extract important parts
td = data [["text","date"]]
td.dropna(inplace=True)
td.drop(td.tail(1).index,inplace=True)
split_text=td['text'].str.split('-',expand=True)

df= split_text.join(td["date"])

print(df)

#add date column

#Method for detecting street names



#Sorting comments into new files depending on the presence of a street name
# %%
