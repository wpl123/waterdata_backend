import geojson
import geopandas as gpd
import shapely
from shapely.geometry import Point,Polygon

import json
import requests
import numpy as np
import geopip
import dash_leaflet as dl
import dash_leaflet.express as dlx

def swapCoords(x):
    out = []
    for iter in x:
        if isinstance(iter, list):
            out.append(swapCoords(iter))
        else:
            return [x[1], x[0]]
    return out


url = "/home/admin/dockers/waterdata_backend/frontend/app-dash/assets/Zone11.geojson"

i = 0
gj_dict =[]
with open(url) as f:
    gj = geojson.load(f)
#gj_dict = gj.to_dict()
#print(gj_dict)
#gj1 = dlx.dicts_to_geojson([{**p, **dict(tooltip="Zone: " + p['Name'] + "<br>" 
#                                    + "Area:    " + str(p['T_Area_ha']))} for p in gj])
geobuf = dlx.geojson_to_geobuf(gj)
dl.Overlay(dl.GeoJSON(data=geobuf, id="zones", format="geobuf",                    
                                     hoverStyle=arrow_function(dict(weight=5, color='#666', dashArray=''))),name="Groundwater Aquifer", checked=True),

#gj1 = geopip.GeoPIP(gj_dict)
#print(gj1)

quit
    #print(len(gj['features']))
    
#for i in range(len(gj['features'])):
#    features = gj['features'][i]
#    for feature in features:
        
##     name = (features['properties']['ELEMENTID'])
#        coords = (features['geometry']['coordinates'])
#        gj2 = gpd.GeoSeries(['geometry']['coordinates']).map(lambda polygon: shapely.ops.transform(lambda x, y: (y, x), polygon))
#        print(coords)
# #     area = (features['properties']['T_Area_ha'])
# #     print(area)
#     for coord in coords:
#         for x in coord:
#             for y in x:
#                 print(y[0],y[1])
# #     

#gdf = gpd.read_file(url)          #read geojson into a df
#
##    print(polygons['Name'],polygons['T_Area_ha'])
#gpd.GeoSeries(gdf['coordinates']).map(lambda polygon: shapely.ops.transform(lambda x, y: (y, x), polygon))
#
#polygons_dict = gdf.to_dict('records')  #convert the df to a dict    
#print(polygons_dict)
