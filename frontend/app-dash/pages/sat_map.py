import pandas as pd

import dash
from dash import html
import dash_bootstrap_components as dbc
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash_extensions.javascript import arrow_function
from dash.dependencies import Input, Output
from torch import HOIST_CONV_PACKED_PARAMS
from navbar2_2 import create_navbar
from sidebar2_2 import create_sidebar

from dbutils import *
from flutils import *
from dash_dbutils import *
from utils.read_database import *


def get_meter_site_data():
    
    meters = read_meters()
    df_meters = meters[['lat', 'lon', 'meter_no', 'meter_name']]
    #df_meters.rename(columns={'lng':'lon'}, inplace=True)
    
    meters_dict = df_meters.to_dict('records')
    
    geojson = dlx.dicts_to_geojson([{**m, **dict(tooltip="Meter: " + m['meter_no'] + "<br>" 
                                                 + "Name:    " + m['meter_name'] + "<br>" 
                                                 + "Lat :    " + str(m['lat']) + "<br>" 
                                                 + "Lon :    " + str(m['lon']))} for m in meters_dict])
    geobuf = dlx.geojson_to_geobuf(geojson)
    
    return geobuf


def get_meter_site_data2():
    
    meters = read_meters()
    df_meters = meters[['lat', 'lng', 'meter_no', 'meter_name', 'url', 'meter_type']]
    data = df_to_geojson(df_meters, ['meter_no','meter_name','url','meter_type'],"lat","lng")
    geobuf = dlx.geojson_to_geobuf(data)  # convert to geobuf
        
    return geobuf
    
    
    

def get_info(feature=None):  #TODO: Remove
    
    header = [html.H4("Monitoring Station Data")]
    if not feature:
        return header + ["Hover over a marker"]
    return header + [html.B(feature["properties"]["meter_no"]), 
                     (": "),
                     (feature["properties"]["meter_name"]),
                     #(", Coords: "), 
                     #(feature["geometry"]["lat"]),                             
                     html.Br()]  






card_map2 = dbc.Card(
    [        
        html.Div(
            [
    
                dl.Map(center=[-30.50, 150.10], zoom=10, children=[
#                    dl.TileLayer(),
#                    dl.TileLayer(url="http://www.google.cn/maps/vt?lyrs=s@189&gl=cn&x={x}&y={y}&z={z}"),
                    dl.TileLayer(url="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}"),
#                    dl.GeoJSON(data=get_meter_site_data(),options=dict(filter=geojson_filter), id="geojson"),
#                    dl.GeoTIFFOverlay(id=GEOTIFF_ID, interactive=True, style={'width': '1000px', 'height': '500px'}),
#                    dl.GeoJSON(data=get_meter_site_data(), id="monitor", format="geobuf",                    
#                    hoverStyle=arrow_function(dict(weight=5, color='#666', dashArray=''))),
                    dl.GeoJSON(url="/assets/Zone11.geojson", id="Zone11"),
                ], style={'width': '100%', 'height': '80vh','margin': "auto", }, id="map"), #"display": "block"  
            ],
        ),
        html.Div(id="monitors"),
    ]        
)

card_map = dbc.Card(
    [        
        html.Div(
            [
    
                dl.Map(center=[-30.50, 150.10], zoom=10, children=[
#                    dl.TileLayer(),
#                    dl.TileLayer(url="http://www.google.cn/maps/vt?lyrs=s@189&gl=cn&x={x}&y={y}&z={z}"),
                    dl.TileLayer(url="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}"),
#                    dl.GeoJSON(data=get_meter_site_data(),options=dict(filter=geojson_filter), id="geojson"),
#                    dl.GeoTIFFOverlay(id=GEOTIFF_ID, interactive=True, style={'width': '1000px', 'height': '500px'}),
                    dl.GeoJSON(data=get_meter_site_data(), id="monitor", format="geobuf",                    
                    hoverStyle=arrow_function(dict(weight=5, color='#666', dashArray=''))),
                ], style={'width': '100%', 'height': '80vh','margin': "auto", }, id="map"),
            ]     
        ),
        html.Div(id="monitors"),
    ]        
)

def create_map():
    layout = html.Div([
        card_map
        
    ])
    return layout