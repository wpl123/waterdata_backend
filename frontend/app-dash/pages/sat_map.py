import pandas as pd
import geojson
import geopandas

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

attribution = '© Google'
keys = ["Satellite","Topo"]
url = "/home/admin/dockers/waterdata_backend/frontend/app-dash/assets/Zone11.geojson"

# Get Zones
with open(url) as f:
    gj = geojson.load(f)
    gb = dlx.geojson_to_geobuf(gj)



def get_info(feature=None):
    header = [html.H4("Namoi Aquifer, Monitoring Stations")]
    return header

info = html.Div(children=get_info(), id="info", className="info",
                style={"position": "absolute", "top": "10px", "right": "170px", "z-index": "1000"})


def get_meter_site_data():
    
    meters = read_meters()
    df_meters = meters[['lat', 'lon', 'meter_no', 'meter_name']]
    meters_dict = df_meters.to_dict('records')
    geojson = dlx.dicts_to_geojson([{**m, **dict(tooltip="Meter: " + m['meter_no'] + "<br>" 
                                    + "Name:    " + m['meter_name'] + "<br>" 
                                    + "Lat :    " + str(m['lat']) + "<br>" 
                                    + "Lon :    " + str(m['lon']))} for m in meters_dict])
    geobuf = dlx.geojson_to_geobuf(geojson)
    
    return geobuf


def get_polygon_coords1():
    
    polygon_list =[]
    #Get the polygon coords for each zone
    with open(url) as f:
        gj = geojson.load(f)
    
    for i in range(len(gj['features'])):
        features = gj['features'][i]
        name   = (features['properties']['ELEMENTID'])
        coords = (features['geometry']['coordinates'])
        area   = (features['properties']['T_Area_ha']) 
        rows   = [name,coords,area]
        polygon_list.append(rows)
    # create tooltip --> https://stackoverflow.com/questions/39770744/how-to-add-a-html-title-tooltip-to-a-leaflet-js-polygon
    # L.polygon(coords).bindTooltip("my tooltip").addTo(map);
    #    dl.Polygon(coords).bindTooltip("Zone: " + name + "<br>" + "(Ha): " + str(area)).addTo(map)
    return polygon_list
    

def get_polygon_coords2():
    
    df_polygon = geopandas.read_file(url)                          #read geojson into a df
    #df_polygon.rename(columns = {'lon':'lng'}, inplace = True)     # rename for geobugf compatability
    polygons_dict = df_polygon.to_dict('records')                  #convert the df to a dict
    
    geojson = dlx.dicts_to_geojson([{**p, **dict(tooltip="Zone: " + p['Name'] + "<br>" 
                                    + "Area:    " + str(p['T_Area_ha']))} for p in polygons_dict])  # add the tooltip
    geobuf = dlx.geojson_to_geobuf(geojson)                         #convert the geojson to a geobuf
    return geobuf  


def get_info1(feature=None):  #TODO: Remove
    
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
                    dl.GeoJSON(url=url, id="Zone11"),
                ], style={'width': '100%', 'height': '80vh','margin': "auto", }, id="map"), #"display": "block"  
            ],
        ),
        html.Div(id="monitors"),
    ]        
)
# 	https://maps.six.nsw.gov.au/arcgis/rest/services/public/NSW_Base_Map/MapServer/WMTS/1.0.0/WMTSCapabilities.xml
card_map = dbc.Card(
    [        
        html.Div(
            [
    
                dl.Map(center=[-30.50, 150.10], zoom=10, 
                    children=[
                        dl.TileLayer(url="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}", attribution=attribution),
                        dl.LayersControl(
                            #[dl.BaseLayer(
                            #    dl.TileLayer(url="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}", attribution=attribution),
                            #    
                            #)]  +
                   
                            [#dl.Overlay(dl.GeoJSON(url="/assets/Zone11.geojson", 
                            ##                       #options=dict(style=style_handle),  # how to style each polygon
                            ##                       zoomToBounds=True,  # when true, zooms to bounds when data changes (e.g. on load)
                            ##                       zoomToBoundsOnClick=True,  # when true, zooms to bounds of feature (e.g. polygon) on click
                            ##                       hoverStyle=arrow_function(dict(weight=5, color='#666', dashArray='')),  # style applied on hover
                             #                      id="geojson"),name="Groundwater Aquifer", checked=True),
                             dl.Overlay(dl.GeoJSON(data=gb, id="zones", format="geobuf",                    
                                     hoverStyle=arrow_function(dict(weight=2, color='#FF0000', dashArray=''))),name="Groundwater Aquifer", checked=True),
                            
                             dl.Overlay(dl.GeoJSON(data=get_meter_site_data(), id="monitor", format="geobuf",                    
                                     hoverStyle=arrow_function(dict(weight=5, color='#666', dashArray=''))),name="Meter Markers", checked=True)]
                           
                        ),
                                     
                    ], style={'width': '100%', 'height': '80vh','margin': "auto", }, id="map"
                ),
            ]     
        ),
        html.Div(id="monitors"),
    ]        
)



card_map1 = dbc.Card(
    [        
        html.Div(
            [
    
                dl.Map(center=[-30.50, 150.10], zoom=10, 
                    children=[

                            dl.TileLayer(url="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}"),
#                            dl.GeoJSON(data=get_meter_site_data(),options=dict(filter=geojson_filter), id="geojson"),
#                            dl.GeoTIFFOverlay(id=GEOTIFF_ID, interactive=True, style={'width': '1000px', 'height': '500px'}),
                            dl.GeoJSON(url="/assets/Zone11.geojson", id="Zone11"),
                            dl.GeoJSON(data=get_meter_site_data(), id="monitor", format="geobuf",                    
                            hoverStyle=arrow_function(dict(weight=5, color='#666', dashArray=''))),
                    ], style={'width': '100%', 'height': '80vh','margin': "auto", }, id="map"
                ),
            ]     
        ),
        html.Div(id="monitors"),
    ]        
)

def create_map():
    
    #polygon_coords = get_polygon_coords()
    
    layout = html.Div([
        info,
        card_map,
        
    ])
    #for p in polygon_coords:
    #        dl.polygon(p[1]).bindTooltip("Zone: " + p[0] + "<br>" + "(Ha): " + str(p[2])).addTo(map)
            
    return layout