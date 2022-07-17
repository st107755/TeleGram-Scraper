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

# delete areanames from dataset: stuttgart, stuggi, ludwigsburg, lubu
df['text'] = df['text'].apply(lambda x: x.lower())
df['text'] = df['text'].apply(lambda x: x.replace("stuttgart",""))
df['text'] = df['text'].apply(lambda x: x.replace("stuggi",""))
df['text'] = df['text'].apply(lambda x: x.replace("ludwigsburg",""))
df['text'] = df['text'].apply(lambda x: x.replace("lubu",""))

for index, row in df.iterrows():
    # classify sentence
    sentence = Sentence(row['text'])
    loc_list = []
    tagger.predict(sentence)
    loc_summary = []
    # search for location in classification
    for entitys in sentence.get_spans('ner'):
          if entitys.tag == 'LOC':
            loc_list.append(entitys.text)

    location_result = text2geo.text2geo(loc_list)
    if location_result.x == 0 and location_result.y == 0 and len(loc_list)>1:
      #pdb.set_trace()
      for loc in loc_list: #loc kann beliebig benannt werden
        loc_summary.append(text2geo.text2geo_res(loc))
      
      loc_summary.sort(key=len)
      loc_summary = [loc for loc in loc_summary if len(loc) != 0]
      #pdb.set_trace()
      try:
        result_loc = loc_summary[0]
        latitude = float(result_loc[0]['lat'])
        longitude = float(result_loc[0]['lon'])
        location_result = Point(latitude,longitude)
      except:
        location_result = Point(0,0)
      
       


    # pdb.set_trace()
    df.loc[index,'geometry'] = location_result.wkt
    # pdb.set_trace()

df['geometry'] = gpd.GeoSeries.from_wkt(df['geometry'])
gdf = gpd.GeoDataFrame(df, geometry='geometry')
gdf.to_csv('chat_geo.csv', sep=';', encoding='utf-8-sig', index=False) 


