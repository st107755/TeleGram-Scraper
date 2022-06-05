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
    df.loc[index,'geometry'] = text2geo.text2geo(entity_list).wkt
    # pdb.set_trace()

df['geometry'] = gpd.GeoSeries.from_wkt(df['geometry'])
gdf = gpd.GeoDataFrame(df, geometry='geometry')
gdf.to_csv('chat_geo.csv', sep=';', encoding='utf-8-sig', index=False) 

