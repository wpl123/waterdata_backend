# -*- coding: utf-8 -*-
import json
import geojson

import os, sys, locale
import dash
from dash import html, dcc, callback, Input, Output, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import pymysql

from flask import Flask

from pathlib import Path

# import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

import dash_leaflet as dl
import dash_leaflet.express as dlx

from dash_extensions.javascript import arrow_function
from dash.dependencies import Input, Output

from datetime import datetime as dt, date

root_folder = r'{}'.format(Path(Path(__file__).parent.absolute().parent))
#print(root_folder)
sys.path.append(root_folder + '/app-dash/pages')

#https://stackoverflow.com/questions/1260792/import-a-file-from-a-subdirectory#%E2%80%A6
sys.path.extend([f'./{name}' for name in os.listdir(".") if os.path.isdir(name)])
locale.setlocale(locale.LC_ALL, '')

#Debug
#https://stackoverflow.com/questions/60593604/importerror-attempted-relative-import-with-no-known-parent-package
#print(__name__)
#print(sys.path)
#__package__ = ".frontend.app-dash"
#print("In module products sys.path[0], __package__ ==", sys.path[0], __package__)

from dbutils import *
from flutils import *
from dash_dbutils import *
from utils.read_database import *

from index import create_page_home
from summary import create_page_summary
from correlations import create_page_correlations
from groundwater import create_page_groundwater
from surfacewater import create_page_surfacewater
from rainfall import create_page_rainfall
from sat_map import get_info


server = Flask(__name__)

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
#app.config.suppress_callback_exceptions=True

df_meters, df = read_db()
meter_list = list(df_meters['meter_no'])
# add Elfin Surfacewater Data
dfe = df[df['meter_no'] == '419051']

# add Kaputar Rainfall Data
dfk = df[df['meter_no'] == '054151-2']

dfek = pd.merge(dfe,dfk,left_index=True, right_index=True)

sdate = df.iloc[0,1]
edate = df.iloc[-1,1]

#

 
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Loading(
                    children=[
                        html.Div(id='page-content'),
                    ],    
                    #color="119DFF",
                    type="dot",
                    fullscreen=False
                   
                ),
    #html.Div(id='page-content'),
    dcc.Store(id='store-data',data=[],storage_type='memory')   
])


#TODO: Setup spinner
#TODO: Use callback to populate dropdown
#@app.callback(Output("monitors", "children"), 
#              [Input("monitor", "hover_feature")])
#def info_hover(feature):
#    if feature is not None:
# #       print(feature)
#        return get_info(feature)


@app.callback(
   Output('store-data', 'data'),
   [Input(component_id='xaxis-column', component_property='value'),
    Input(component_id='yaxis-column', component_property='value'),
   ],
    prevent_initial_call=True
   )


def store_data(meter_no1, meter_no2):
    
    dff1 = df[(df['meter_no'] == meter_no1)]      
    dff2 = df[(df['meter_no'] == meter_no2)]
    
    dff3 = pd.merge(dff1,dff2,left_index=True, right_index=True)
    df2 = pd.merge(dff3,dfek,left_index=True, right_index=True)
    
    return df2.to_dict('records')



@app.callback(Output('page-content', 'children'),
            [Input('url', 'pathname'),
            Input('store-data', 'data')
            ])
def display_page(pathname,data):
    
    if pathname == '/':
        return create_page_home(data)
    if pathname == '/summary':
        return create_page_summary(data)
    if pathname == '/correlations':
        return create_page_correlations(data)
    if pathname == '/groundwater':
        return create_page_groundwater(data)
    if pathname == '/surfacewater':
        return create_page_surfacewater(data)
    if pathname == '/rainfall':
        return create_page_rainfall(data)
    else:
        return create_page_home(data)





if __name__ == '__main__':
   app.run_server(debug=True,host='192.168.11.6',port=8050)
#   app.run_server(debug=False,host='192.168.11.6',port=8050)   
#    app.run_server()