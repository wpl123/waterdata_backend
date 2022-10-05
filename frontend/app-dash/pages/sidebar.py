import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

import pandas as pd

from dbutils import *
from flutils import *
from dash_dbutils import *
from utils.read_database import *

  


def create_meter_selector():
    
    meters = read_meters()
    meter_list = list(meters['meter_no'])
    markdown_text = """
    Select two groundwater monitoring bores that you wish to compare from the dropdowns below.
    
    """
    
    
        
    layout = dbc.Container([
        dcc.Markdown(children=markdown_text),
        dbc.Row(
            html.Div([
                dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in meter_list],
                value='GW967137.1.1'
                ),
            ], className="dash-bootstrap", style={'width':'100%'}),    
        ),
        dbc.Row(
            html.Div([
                dcc.Dropdown(
                    id='yaxis-column',
                    options=[{'label': i, 'value': i} for i in meter_list],
                    value='GW967137.2.2'
                ),
            ], className="dash-bootstrap", style={'width':'100%'}),    
        ),
        
    ])
    
    return layout



def create_sidebar(markdown_text):
    
    meters = read_meters()
    meter_list = list(meters['meter_no'])
    
    markdown_text = """
    Select two groundwater monitoring bores to compare from the dropdowns below.
    
    """
    
    
    sidebar = dbc.NavbarSimple(
        
        children=[
            
            dbc.Col(
                
                children=[
                                        
#                    dcc.Markdown(children=markdown_text),
                                    
                    dbc.DropdownMenu(
                        nav=True,
                        in_navbar=True,
                        label="Graph Menu", # Label given to the dropdown menu
                        children=[
                            # In this part of the code we create the items that will appear in the dropdown menu on the right
                            # side of the Navbar.  The first parameter is the text that appears and the second parameter 
                            # is the URL extension.
                            dbc.DropdownMenuItem("Home", href='/'), # Hyperlink item that appears in the dropdown menu
                            dbc.DropdownMenuItem(divider=True), # Divider item that appears in the dropdown menu  
                            dbc.DropdownMenuItem("Summary", href='/summary'), # Hyperlink item that appears in the dropdown menu
                            dbc.DropdownMenuItem("Correlations", href='/correlations'), # Hyperlink item that appears in the dropdown menu
                            #dbc.DropdownMenuItem(divider=True), 
                            dbc.DropdownMenuItem("Surfacewater", href='/surfacewater'), # Hyperlink item that appears in the dropdown menu
                            #dbc.DropdownMenuItem(divider=True), 
                            dbc.DropdownMenuItem("Groundwater", href='/groundwater'), # Hyperlink item that appears in the dropdown menu
                            #dbc.DropdownMenuItem(divider=True), 
                            dbc.DropdownMenuItem("Rainfall", href='/rainfall'), # Hyperlink item that appears in the dropdown menu
                            dbc.DropdownMenuItem(divider=True), 
                        ],
                    ),  
                ]
                
            )
            
        ],
        #brand="Home",  # Set the text on the left side of the Navbar
        brand_href="/",  # Set the URL where the user will be sent when they click the brand we just created "Home"
        sticky="top",  # Stick it to the top... like Spider Man crawling on the ceiling?
        color="dark",  # Change this to change color of the navbar e.g. "primary", "secondary" etc.
        dark=True,  # Change this to change color of text within the navbar (False for light text)
    )

    return sidebar

   
   
   