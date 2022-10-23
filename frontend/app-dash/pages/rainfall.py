import dash
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

import pandas as pd

from utils.df_split import df_split
from navbar import create_navbar
from sidebar import create_sidebar


markdown_text = '''
        Hover over the graph, use the tools in the top right corner.
        '''

nav = create_navbar()
side = create_sidebar(markdown_text)


def make_rainfall_graph(data):
    
    df = pd.DataFrame(data)
    
    dff,dfe,dfk = df_split(df)
    m1 = str(dff.iloc[0,0])
    m2 = str(dff.iloc[0,3])
   
    
    fig = px.line(dfk, x='read_date', y='level') # ,color='#0508fb' ,color='blue'
    fig.update_layout(hovermode='closest',xaxis_title='054151-2 (mm)',yaxis_title='Date',title='Rainfall Bar Plot',title_font_size=30) # ,height=400, width=465 / height=250, width=250 400
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightPink')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightPink')
    
    return fig





def create_page_rainfall(data):
    #print("data: ",data)
    rainfall_graph = make_rainfall_graph(data)
    
    layout = dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Maules Creek Water",
                            className='text-centre text-primary mb-4'),width=12)
        ]),
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        dbc.Row(side),
                    ]),
                dbc.Col( 
                    dcc.Graph(id='rainfall-graph', figure=rainfall_graph)
                ),    
            ]
        )
        
    ])
    return layout