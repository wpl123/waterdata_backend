import pandas as pd

import dash
from dash import html
import dash_bootstrap_components as dbc
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash_extensions.javascript import arrow_function
from dash.dependencies import Input, Output
from navbar2_2 import create_navbar
from sidebar2_2 import create_sidebar

from dbutils import *
from flutils import *
from dash_dbutils import *


dash.register_page(__name__, path='/')

nav = create_navbar()
side = create_sidebar()


#def get_data():
#    
#    df_meters = meters[['lat', 'lng', 'meter_no', 'meter_name', 'url', 'meter_type']]
#    
#    data = df_to_geojson(df_meters, ['meter_no','meter_name','url','meter_type'],"lat","lng")
#    
#    geobuf = dlx.geojson_to_geobuf(data)  # convert to geobuf
#    return geobuf
#
#
#card_map = dbc.Card(
#    [        
#        html.Div(
#            [
#    
#                dl.Map(center=[-30.50, 150.10], zoom=10, children=[
##                    dl.TileLayer(),
#                    dl.TileLayer(url="http://www.google.cn/maps/vt?lyrs=s@189&gl=cn&x={x}&y={y}&z={z}"),
##                    dl.GeoTIFFOverlay(id=GEOTIFF_ID, interactive=True, style={'width': '1000px', 'height': '500px'}),
#                    dl.GeoJSON(data=get_data(), id="monitor", format="geobuf",
#                    hoverStyle=arrow_function(dict(weight=5, color='#666', dashArray=''))),
#                ], style={'width': '100%', 'height': '54vh','margin': "auto", }, id="map"), #"display": "block"  
#            ],
#        ),
#        html.Div(id="monitors"),
#    ]        
#)



def create_page_home():
    layout = html.Div([
        nav,
        side,
        
    ])
    return layout