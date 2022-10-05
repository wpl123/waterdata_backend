
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


def make_summary_graph(data):
    
    df = pd.DataFrame(data)
    
    dff,dfe,dfk = df_split(df)
    
    m1 = str(dff.iloc[0,0])
    m2 = str(dff.iloc[0,3])
    
    fig = make_subplots(
                rows=3, cols=1,row_heights=[25,25,25],shared_xaxes=True,
                subplot_titles=("Groundwater", "Elfin Surfacewater", "Kaputar Rainfall")) # , "Kaputar Rainfall MA (90)"
    
    fig.append_trace(go.Scatter(x=dff['read_date_x'], y=dff['level_x'],name=m1), row=1, col=1) #TODO: Row Heights
    fig.append_trace(go.Scatter(x=dff['read_date_x'], y=dff['level_y'],name=m2), row=1, col=1)
    fig.append_trace(go.Scatter(x=dfe['read_date'], y=dfe['level'],name='41905'), row=2, col=1)
    fig.append_trace(go.Scatter(x=dfk['read_date'], y=dfk['level'],name='054151-2',opacity=1), row=3, col=1)
    #fig.append_trace(go.Scatter(x=dfk['read_date'], y=dfk['MA90'],name='054151-2 (MA90)',mode='lines',opacity=1), row=4, col=1)

    fig.update_traces(marker_color='#0508fb',selector=dict(type='bar'), row=3, col=1)

    fig.update_yaxes(title_text="(AHD)", row=1, col=1)
    fig.update_yaxes(title_text="(m)", row=2, col=1)
    fig.update_yaxes(title_text="(mm)", row=3, col=1)
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightPink')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightPink')
    #fig.update_yaxes(title_text="(mm)", row=4, col=1)
    
    fig.update_layout(title_text="Groundwater, Surfacewater Comparison",title_font_size=30,height=875,width=930) #height=875,width=930, textfont_color=
    
    #fig1 = px.scatter(dff, x='level_x', y='level_y')
    #fig1.update_layout(hovermode='closest',xaxis_title=m1,yaxis_title=m2,title='Scatter Plot',title_font_size=30) # ,height=400, width=465 / height=250, width=250 400
    #
    #fig2 = px.imshow(df_corr)
    #fig2.update_layout(hovermode='closest',title='Correlation Heatmap',title_font_size=30) #,height=500, width=500
    
    
    return fig

header = html.H3('Summary Data')



def create_page_summary(data):
    #print("data: ",data)
    summary_graph = make_summary_graph(data)
    
    layout = dbc.Container([
        dbc.Row([
            nav
        ]),
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        
                        dbc.Row(side),
#                        dbc.Row(m_sel),
                    ],width=2
                ),
                dcc.Graph(id='summary-graph', figure=summary_graph),
            ],
        )
        
    ])
    
    #layout = dbc.Container([
    #    dbc.Row([
    #        dbc.Col(html.H1("Maules Creek Water",
    #                        className='text-centre text-primary mb-4'),width=12)
    #    ]),
    #    dbc.Row(
    #        children=[
    #            dbc.Col(
    #                children=[
    #                    dbc.Row(side),
    #                ]),
    #            dbc.Col( 
    #                dcc.Graph(id='summary-graph', figure=summary_graph)
    #            ),    
    #        ]
    #    )
    #    
    #])
    return layout