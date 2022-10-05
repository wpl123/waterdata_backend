import dash
from dash import html, dcc
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


def make_surfacewater_graph(data):
    
    df = pd.DataFrame(data)
    
    dff,dfe,dfk = df_split(df)
    m1 = str(dff.iloc[0,0])
    m2 = str(dff.iloc[0,3])
    
        
    fig = px.scatter(dff, x='level_x', y='level_y')
    fig.update_layout(hovermode='closest',xaxis_title=m1,yaxis_title=m2,title='Scatter Plot',title_font_size=30) # ,height=400, width=465 / height=250, width=250 400
    #
    #fig2 = px.imshow(df_corr)
    #fig2.update_layout(hovermode='closest',title='Correlation Heatmap',title_font_size=30) #,height=500, width=500
    
    
    return fig





def create_page_surfacewater(data):
    #print("data: ",data)
    surfacewater_graph = make_surfacewater_graph(data)
    
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
                    dcc.Graph(id='surfacewater-graph', figure=surfacewater_graph)
                ),    
            ]
        )
        
    ])
    return layout