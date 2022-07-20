import json
import requests  
import urllib 
import logging
import pdb
from shapely.geometry import Point

def request(search):
    encoded = search.replace(' ', '+') 
    header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36',
                'Host': 'nominatim.openstreetmap.org'}
    return requests.get('https://nominatim.openstreetmap.org/search.php?q={}&format=jsonv2'.format(encoded),headers=header).json()

def text2geo(locations): 
    if len(locations):
        q_value = ' '.join(locations)
        result = request(q_value)
        try:
            latitude = float(result[0]['lat'])
            longitude = float(result[0]['lon'])
            return Point(latitude,longitude)
        except:
            return Point(0,0)
    else:   
        return Point(0,0)

def text2geo_res(locations):
    if len(locations):
        return request(locations)

