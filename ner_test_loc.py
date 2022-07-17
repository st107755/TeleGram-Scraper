#%%
from flair.data import Sentence
from flair.models import SequenceTagger
import pandas as pd
import text2geo #file with geofunction
import geopandas as gpd
from shapely.geometry import Point
import pdb

# load tagger
tagger = SequenceTagger.load("flair/ner-german-large")
# read data
df = pd.read_csv('chat.csv',delimiter=';')
# will empty with string
df = df.fillna('')
# gdf = gpd.GeoDataFrame(df)

#%%
# make example sentence
sentence = Sentence("Auf'm weg zur Arbeit durch lubu verstärkt Polizei Kontrollen. Gefühlt standen sie an jeder 10ten Ecke Rum und haben den Verkehr beobachtet.   Raum Ludwigsburg/Neckarwahingen / oßweil")

# predict NER tags
tagger.predict(sentence)

# print sentence
print(sentence)

# print predicted NER spans
print('The following NER tags are found:')
# iterate over entities and print
for entity in sentence.get_spans('ner'):
    print(entity)

######################################################################################

# %%

# load tagger
#tagger = SequenceTagger.load("flair/ner-german-large")
# read data
df_test = pd.read_csv('chat.csv',delimiter=';')
df_test_loc ={}
# will empty with string
df_test = df.fillna('')
# gdf = gpd.GeoDataFrame(df)

for index, row in df.iterrows():
    # classify sentence
    sentence = Sentence(row['text'])
    entity_list = []
    tagger.predict(sentence)
    # search for location in classification
    for entitys in sentence.get_spans('ner'):
          if entitys.tag == 'LOC':
            entity_list.append(entitys.text)

    # pdb.set_trace()
    df_test.loc[index,'geometry'] = text2geo.text2geo(entity_list).wkt
    ##df_test.loc[index, 'locations'] = entity_list #-versuch, alle Locations pro Sentence auszugeben, die erkannt worden sind
    df_test_loc[index,'locations'] = entity_list
    # pdb.set_trace() 

df_test['geometry'] = gpd.GeoSeries.from_wkt(df['geometry'])
gdf = gpd.GeoDataFrame(df_test, geometry='geometry')
gdf.to_csv('chat_geo2.csv', sep=';', encoding='utf-8-sig', index=False) 


# %%
