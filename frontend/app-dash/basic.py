# -*- coding: utf-8 -*-

#import dash
#import dash_core_components as dcc
#import dash_html_components as html
#import dash_bootstrap_components as dbc
#
#from dash.dependencies import Input, Output
#
#import pandas as pd
#import plotly.express as px

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import pymysql

# import plotly.graph_objs as go
import plotly.express as px
# 
from plotly.subplots import make_subplots
import plotly.graph_objects as go


from dash.dependencies import Input, Output
from datetime import datetime as dt, date

df = pd.DataFrame({'GW967137.1.1':[1.000000,0.868643,0.741188,0.018659,0.301556],
                    'GW967137.1.1':[1.000000,0.868643,0.741188,0.018659,0.301556],
                    'GW967137.2.2':[0.868643,1.000000,0.506081,0.014930,0.121363],
                    'Elfin Crossing':[0.741188,0.506081,1.000000,0.063414,0.505518],
                    'Kaputar Rainfall':[0.018659,0.014930,0.063414,1.000000,0.120831],
                    'Rainfall MA90':[0.301556,0.121363,0.505518,0.120831,1.000000]},
                    columns=['GW967137.1.1','GW967137.2.2','Elfin Crossing','Kaputar Rainfall','Rainfall MA90'])

#external_stylesheets = ['https://codepen.io/anon/pen/mardKv.css']
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash(__name__)
#
#
#
card_heatmap = dbc.Card(
    [
        dcc.Graph(id='gw-heatmap', figure={})
    ]  
)

app.layout = dbc.Container([
    dbc.Card(card_heatmap),
])
#
#
#@app.callback ([Output(component_id='gw-heatmap', component_property='figure')],
#        Input('data', 'value'))

def show_cor():    
    

    fig = px.imshow(df,title='Correlation Heatmap')
    return fig


def main():

    logs_dir = "/home/admin/dockers/waterdata_frontend/dash/logs/"
    df = pd.DataFrame({'GW967137.1.1':[1.000000,0.868643,0.741188,0.018659,0.301556],
                    'GW967137.1.1':[1.000000,0.868643,0.741188,0.018659,0.301556],
                    'GW967137.2.2':[0.868643,1.000000,0.506081,0.014930,0.121363],
                    'Elfin Crossing':[0.741188,0.506081,1.000000,0.063414,0.505518],
                    'Kaputar Rainfall':[0.018659,0.014930,0.063414,1.000000,0.120831],
                    'Rainfall MA90':[0.301556,0.121363,0.505518,0.120831,1.000000]},
                    columns=['GW967137.1.1','GW967137.2.2','Elfin Crossing','Kaputar Rainfall','Rainfall MA90'])

    fig = show_cor(df)
    fig.show()
    
    
if __name__ == '__main__':
    app.run_server(debug=True,host='192.168.11.6',port=8050)