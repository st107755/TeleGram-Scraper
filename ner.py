from flair.data import Sentence
from flair.models import SequenceTagger
import pandas as pd
from regex import R
import text2geo #file with geofunction
import geopandas as gpd
from shapely.geometry import Point
import pdb

def extract_loc_ner(sentence):
    loc_list = []
    # search for location in classification
    for entitys in sentence.get_spans('ner'):
          if entitys.tag == 'LOC':
            loc_list.append(entitys.text)
    return loc_list

def singular_location_query(loc_list, location_result):
    #pdb.set_trace()
    loc_summary = []
    for loc in loc_list: #loc kann beliebig benannt werden
        loc_summary.append(text2geo.request(loc + " stuttgart"))
        
        loc_summary.sort(key=len)
        loc_summary = [loc for loc in loc_summary if len(loc) != 0]
    try:
        result_loc = loc_summary[0]
        latitude = float(result_loc[0]['lat'])
        longitude = float(result_loc[0]['lon'])
        location_result = Point(latitude,longitude)
    except:
        location_result = Point(0,0)
    return location_result

"""delete areanames from dataset: stuttgart, stuggi, ludwigsburg, lubu """
def cleanup(df):
    df.dropna(subset=["text"],inplace=True) # will empty with string
    df['text'] = df['text'].apply(lambda x: x.lower())
    df['text'] = df['text'].apply(lambda x: x.replace("stuttgart",""))
    df['text'] = df['text'].apply(lambda x: x.replace("stuggi",""))
    df['text'] = df['text'].apply(lambda x: x.replace("ludwigsburg",""))
    df['text'] = df['text'].apply(lambda x: x.replace("lubu",""))
    return df


# init named entity recordnition
tagger = SequenceTagger.load("flair/ner-german-large")
df = pd.read_csv('chat.csv',delimiter=';')
df = cleanup(df)
empty_loc_list = 0
full_loc_list = 0
for index, row in df.iterrows():
    # classify sentence
    sentence = Sentence(row['text'])
    tagger.predict(sentence)
    loc_list = extract_loc_ner(sentence)

    location_result = text2geo.text2geo(loc_list)
    if location_result.x == 0 and location_result.y == 0 and len(loc_list)>1:
        location_result = singular_location_query(loc_list, location_result)

    if location_result == Point(0,0):
        if len(loc_list) > 0:
            full_loc_list += 1
        else:
            empty_loc_list +=1
    
    df.loc[index,'geometry'] = location_result.wkt

print("empty loc list: " + str(empty_loc_list))
print("full loc list: " + str(full_loc_list))
df['geometry'] = gpd.GeoSeries.from_wkt(df['geometry'])
gdf = gpd.GeoDataFrame(df, geometry='geometry')
gdf.to_csv('chat_geo.csv', sep=';', encoding='utf-8-sig', index=False) 


