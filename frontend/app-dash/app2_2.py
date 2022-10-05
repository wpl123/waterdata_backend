# -*- coding: utf-8 -*-
import json
import geojson

import os, sys, locale
import dash
from dash import html, dcc, callback, Input, Output
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
#print("here1")
from index2_2 import create_page_home
from summary2_2 import create_page_summary
from groundwater2_2 import create_page_groundwater
from surfacewater2_2 import create_page_surfacewater
from rainfall2_2 import create_page_rainfall
#print("here2")
#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#external_stylesheets = ['https://codepen.io/anon/pen/mardKv.css']
external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css']

server = Flask(__name__)


#app = dash.Dash(server=__name__)
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash(server=server, use_pages=True, external_stylesheets=external_stylesheets)
#print("here3")

# mysql = MySQLUtil()
# mysql.dbConnect()
# # All Meter Data
# meters = pd.DataFrame(get_meters(mysql), columns=['meter_no','meter_name','meter_type','lat','lng', 'url'])
# df = pd.concat([get_meter_data(mysql, meters.iloc[i,0], meters.iloc[i,2]) for i in range(len(meters))])
# df.columns = ['meter_no','read_date_idx','read_date','level']
# df['read_date_idx'] = pd.to_datetime(df['read_date_idx'])
# df.set_index('read_date_idx',inplace=True,drop=True)
# sdate = df.iloc[0,1]
# edate = df.iloc[-1,1]





app.layout = html.Div([
	html.H1('Multi-page app with Dash Pages'),

    html.Div(
        [
            html.Div(
                dcc.Link(
                    f"{page['name']} - {page['path']}", href=page["relative_path"]
                )
            )
            for page in dash.page_registry.values()
        ]
    ),

	dash.page_container
])

if __name__ == '__main__':
   app.run_server(debug=True,host='192.168.11.6',port=8050)
#   app.run_server(debug=False,host='192.168.11.6',port=8050)   
#    app.run_server()