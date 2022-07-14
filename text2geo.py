import requests   
import pdb
from shapely.geometry import Point


def text2geo(locations): 
    if len(locations):
        q_value = ' '.join(locations)
        loc_dict = {'q': q_value,'limit':1,'format':'json','adressdetails':1}
        result = requests.get('https://nominatim.openstreetmap.org/search', params= loc_dict).json()
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
        q_value = ' '.join(locations)
        loc_dict = {'q': q_value,'limit':5,'format':'json','adressdetails':1}
        return requests.get('https://nominatim.openstreetmap.org/search', params= loc_dict).json()

