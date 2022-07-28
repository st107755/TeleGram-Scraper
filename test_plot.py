from ctypes.wintypes import POINT
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as cx
from shapely.geometry import Point
import geoplot
import geoplot.crs as gcrs
import pdb


def drop_invalid_points(gdf):
    for index, row in gdf.iterrows(): # Looping over all points
        x_round = round(row.geometry.x,2)
        y_round = round(row.geometry.y,2)
        if 9.13 > x_round or x_round > 9.3 or  48.73 > y_round or y_round > 48.83:
            gdf.loc[[index],"geometry"] = None
            #pdb.set_trace()
    return gdf
    
df = pd.read_csv('chat_geo.csv',delimiter=';')
df['geometry'] = gpd.GeoSeries.from_wkt(df['geometry'])
gdf = gpd.GeoDataFrame(df, geometry='geometry',crs=4326)
gdf = gpd.GeoDataFrame(df,geometry = df.geometry)
gdf = drop_invalid_points(gdf)
#gdf = gdf.dropna()

#### Normal map
'''
df_wm = gdf.to_crs("EPSG:4326")
ax = df_wm.plot()
cx.add_basemap(ax, crs="EPSG:4326")
'''
#### KDE Map

#ax = geoplot.kdeplot(gdf, thresh=0.5)
#cx.add_basemap(ax, crs="EPSG:4326")

#### Colorpleth
ax = geoplot.quadtree(gdf, nmax=5)
cx.add_basemap(ax, crs="EPSG:4326")
#### Show 
plt.show()