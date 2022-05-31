#%%
## Project Textmining
## Social Media - Telegram groups

#install cmd 
#python3 -m pip install matplotlib

# import packages
import pandas as pd
import re
import string
import matplotlib.pyplot as plt

data = pd.read_csv ("chat.csv", delimiter=';', encoding='utf-8')

#%% data cleaning
textseries = data['text']
textseries = textseries.dropna()
textseries = textseries.astype(str)


#%%
def splitter (textseries):
    wordcount = dict()
    for index,value in textseries.items():
        words = re.split(r'\W+', value)
        for word in words:
           if word in wordcount: 
               wordcount[word]+=1
           else: 
               wordcount[word]=1
    
    return wordcount
        

final = splitter(textseries)

# %% stopwords vorinstallieren
import nltk
nltk.download('stopwords')

# %% stopwords,...
from nltk.corpus import stopwords
german_stop_words = stopwords.words('german')

# stopwords removal & lower case
textseries2 = textseries.str.lower().apply(lambda x: ' '.join([word for word in x.split() if word not in (german_stop_words)]))

#%% function without stopwords
def splitter (textseries2):
    wordcount = dict()
    for index,value in textseries2.items():
        words = re.split(r'\W+', value)
        for word in words:
           if word in wordcount: 
               wordcount[word]+=1
           else: 
               wordcount[word]=1
    
    return wordcount
        

final_removed_stopwords = splitter(textseries2)

# %% select keys from dict
selected_data = {key: final_removed_stopwords[key] for key in ["bullen", "blitzer", "polizeikontrolle"]}
