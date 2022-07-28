#Analysing missing data - no match
#%%
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#%% import resultdata
df = pd.read_csv('chat_geo.csv',delimiter=';')

# %% subset data without geodata
df_na = df[df['geometry']=='POINT (0 0)']

# %% count missing geomatch + text
df_na['geometry'].count()
#2029

# %% count missing text
df_na['text'].isna().sum()
#270

# %% case missing text & missing geomatch un all data
# 1 - no location recognized
# 2 - no mapping with geodata
df['na_type_key'] = np.where(
     df['text'].isnull(), '1', 
     np.where(
        df['geometry']=='POINT (0 0)', '2', '0'
     )
)

df['na_type'] = np.where(
     df['text'].isnull(), 'no text', 
     np.where(
        df['geometry']=='POINT (0 0)', 'no map', 'matching'
     )
)

#%%
df['na_type'].groupby(df['na_type']).count()

# %% counting & plotting - barchart
#df['na_type'].value_counts().plot.bar(title='missing location barplot')
#sns.set_theme(style="darkgrid")
#ax = sns.countplot(x="na_type", data=df)
#ax.bar_label(ax.containers[0])

# %% counting & plotting - pie chart
df['na_type'].value_counts().plot(kind='pie', title='missing location pieplot',autopct='%1.1f%%')
plt.show()
# %% analysing data with no location -> no text
df_na_loc = df[df['na_type_key']=='1']

# %% analysing data with no geo -> 
df_na_geo = df[df['na_type_key']=='2']

# %%
df.to_csv('chat_geo_na_type.csv', sep=';', encoding='utf-8-sig', index=False) 