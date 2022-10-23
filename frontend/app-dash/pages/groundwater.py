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


def make_groundwater_graph(data):
    
    df = pd.DataFrame(data)
    
    dff,dfe,dfk = df_split(df)
    m1 = str(dff.iloc[0,0])
    m2 = str(dff.iloc[0,3])
    
    #Todo: 2 Separate Graphs
    fig = make_subplots(
                rows=1, cols=1,row_heights=[25]) # ,subplot_titles=("Groundwater")
    
    fig.append_trace(go.Scatter(x=dff['read_date_x'], y=dff['level_x'],name=m1), row=1, col=1) #TODO: Row Heights
    fig.append_trace(go.Scatter(x=dff['read_date_x'], y=dff['level_y'],name=m2), row=1, col=1)
    
    fig.update_yaxes(title_text="(AHD)", row=1, col=1)
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightPink')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightPink')
    
    
    fig.update_layout(title_text="Groundwater Bore Comparison",title_font_size=30)  #TODO: validate groundwater # ,height=875,width=930
    
    
    
    return fig





def create_page_groundwater(data):
    #print("data: ",data)
    groundwater_graph = make_groundwater_graph(data)
    
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
                    dcc.Graph(id='groundwater-graph', figure=groundwater_graph)
                ),    
            ]
        )
        
    ])
    return layout