import pandas as pd

import dash
from dash import html,dcc
import dash_bootstrap_components as dbc
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash_extensions.javascript import arrow_function
from dash.dependencies import Input, Output
from navbar import create_navbar
from sidebar import create_meter_selector, create_sidebar
from sat_map import create_map

from dbutils import *
from flutils import *
from dash_dbutils import *


#nav = create_navbar()
markdown_text = '''


        \n\nSelect two groundwater monitoring bores that you wish to compare from the dropdowns below.\n\n
        
        
        '''
side = create_sidebar(markdown_text)
sat_map = create_map()
m_sel = create_meter_selector()
nav = create_navbar()

#Bootstrap cheatsheet --> https://hackerthemes.com/bootstrap-cheatsheet/

def create_page_home(data):
    layout = dbc.Container([
        dbc.Row([
            nav
        ]),
        html.Hr(),
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        
                        dbc.Row(side),
                        dbc.Row(m_sel),
                    ],width=2
                ),
                dbc.Col(sat_map)
            ]
        )
        
    ])
    return layout
    
def create_page_home2(data):
    layout = dbc.Container([
        dbc.Row([
            nav
        ]),
        html.Hr(),
        dbc.Row(
            children=[
                dbc.Col(
                    [
                        side
                    ],xs=4, sm=4, md=2,lg=2, xxl=2
                ),
                #dbc.Col(
                #    children=[
                #        dbc.Row(sat_map)
                #    ],xs=8, sm=8, md=10,lg=10, xxl=10
                #)
                dbc.Col(
                [
                    dash.page_container
                ],xs=8, sm=8, md=10,lg=10, xxl=10)
                    
            ]
        )
        
    ])
    return layout

#,xs=8, sm=8, md=10,lg=10, xxl=10
#xs=4, sm=4, md=2,lg=2, xxl=2