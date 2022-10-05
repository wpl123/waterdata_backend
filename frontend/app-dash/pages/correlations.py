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


def make_correlations_graph(data):
    
    df = pd.DataFrame(data)
    
    dff,dfe,dfk = df_split(df)
    m1 = str(dff.iloc[0,0])
    m2 = str(dff.iloc[0,3])
    
#   Create concatenated df for the heatmap
#    df_join = pd.merge(dff,dfe1,left_index=True, right_index=True)
    df_join = pd.merge(dff,dfe,left_index=True, right_index=True)
    df_join1 = df_join.drop(columns=['meter_no_x', 'read_date_x', 'meter_no_y', 'read_date_y'],axis=1)

#    df_join2 = pd.merge(df_join1,dfk1,left_index=True, right_index=True)
    df_join2 = pd.merge(df_join1,dfk,left_index=True, right_index=True)
    df_join3 = df_join2.drop(columns=['meter_no_x', 'read_date_x', 'meter_no_y', 'read_date_y'],axis=1)
   
    df_join3.columns = [m1,m2,'Elfin Crossing','Kaputar Rainfall'] #
    
    df_join3 = df_join3.dropna() #(axis=0, how='any', thresh=None, subset=None, inplace=False)
    
    df_join3 = df_join3.apply(pd.to_numeric)
    df_corr = df_join3.corr(method='spearman')
        
    fig = px.scatter(dff, x='level_x', y='level_y')
    fig.update_layout(hovermode='closest',xaxis_title=m1,yaxis_title=m2,title='Scatter Plot',title_font_size=30) # ,height=400, width=465 / height=250, width=250 400
    #
    fig2 = px.imshow(df_corr)
    fig2.update_layout(hovermode='closest',title='Correlation Heatmap',title_font_size=30) #,height=500, width=500
    
    
    return fig





def create_page_correlations(data):
    #print("data: ",data)
    correlations_graph = make_correlations_graph(data)
    
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
                    dcc.Graph(id='correlations-graph', figure=correlations_graph)
                ),    
            ]
        )
        
    ])
    return layout