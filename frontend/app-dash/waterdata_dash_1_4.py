# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import pymysql

# import plotly.graph_objs as go
# import plotly.express as px
# 
from plotly.subplots import make_subplots
import plotly.graph_objects as go

import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash_extensions.javascript import arrow_function

from dash.dependencies import Input, Output
from datetime import datetime as dt, date

from utils.dbutils import *
from utils.flutils import *
from utils.dash_dbutils import *


#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css']
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash(__name__, external_stylesheets=dbc.themes.BOOTSTRAP)
#app = dash.Dash(__name__)

mysql = MySQLUtil()
mysql.dbConnect(host ='192.168.11.6', user = 'root', psw = 'water', db_name = 'waterdata', port=30000)

app = dash.Dash()

# All Meter Data
meters = pd.DataFrame(get_meters(mysql), columns=['meter_no','meter_name','meter_type','lat','lon'])
df = pd.concat([get_meter_data(mysql, meters.iloc[i,0], meters.iloc[i,2]) for i in range(len(meters))])
df.columns = ['meter_no','read_date_idx','read_date','level']
df['read_date_idx'] = pd.to_datetime(df['read_date_idx'])
df.set_index('read_date_idx',inplace=True,drop=True)
sdate = df.iloc[0,1]
edate = df.iloc[-1,1]

#print("df: ", df)
# Elfin Surfacewater Data
dfe = pd.DataFrame(get_surfacewater(mysql,'CF419051',sdate,edate))
dfe.columns = ['meter_no','read_date_idx','read_date','level']
dfe['read_date_idx'] = pd.to_datetime(dfe['read_date_idx'])
dfe.set_index('read_date_idx',inplace=True,drop=True)
#print("dfe: ", dfe)

# Kaputar Rainfall Data
dfk = pd.DataFrame(get_rainfall(mysql,'54151',sdate,edate))
dfk.columns = ['meter_no','read_date_idx','read_date','level']
dfk['read_date_idx'] = pd.to_datetime(dfk['read_date_idx'])
dfk.set_index('read_date_idx',inplace=True,drop=True)
#print("dfk: ", dfk)


#df_melt = pd.melt(df, id_vars =['read_date'])


# Generate some in-memory data.
maulesck = dlx.dicts_to_geojson([dict(lat=-30.4995666700, lon=150.1557222200)])
brisbane = dlx.geojson_to_geobuf(dlx.dicts_to_geojson([dict(lat=-27.470125, lon=-153.021072)]))
    
#----------------------------------------------------------------------------------------------------------------------------------

def generate_table(dataframe, max_rows=10):
   return html.Table(
      # Header
      [html.Tr([html.Th(col) for col in dataframe.columns])] +
      # Body
      [html.Tr([
         html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
      ]) for i in range(min(len(dataframe), max_rows))]
   )
	




study = ['Scatter','Bar','Line','Heatmap']

markdown_text = '''
##### Using this dashboard

Select two groundwater monitoring bores that you wish to graph, then select the start and finish dates that are of interest.

Hover over the pins below to determine the bore numbers to select
'''
#--------------------------------------------------------------------------------------------------

card_graph = dbc.Card(

#        dbc.Spinner(
#            children=[
                dcc.Graph(id='gw-graph', figure={})
#                , body=True, color="secondary",
#           ],
#       ),        
#        dbc.Spinner(children=[dcc.Graph(id="loading-output")], size="lg", color="primary", type="border", fullscreen=True,),
        
)

card_map = dbc.Card(
    
    dl.Map(center=[-30, 150], zoom=10, children=[
        dl.TileLayer(),
        dl.GeoJSON(data=maulesck),  # in-memory geojson (slowest option)
        dl.GeoJSON(data=brisbane, format="geobuf"),  # in-memory geobuf (smaller payload than geojson)
        dl.GeoJSON(url="/assets/us-state-capitals.json", id="capitals"),  # geojson resource (faster than in-memory)
        dl.GeoJSON(url="/assets/us-states.pbf", format="geobuf", id="states",
        hoverStyle=arrow_function(dict(weight=5, color='#666', dashArray=''))),  # geobuf resource (fastest option)
    ], style={'width': '100%', 'height': '20vh', 'margin': "auto", }, id="map"), #"display": "block"
)

card_date_picker = dbc.Card(

    dbc.CardBody(
        [        
            html.Div(
                [
                    dcc.DatePickerRange(
                        id='my-date-picker-range',  # ID to be used for callback
                        calendar_orientation='horizontal',  # vertical or horizontal
                        day_size=39,  # size of calendar image. Default is 39
                        end_date_placeholder_text="End Date",  # text that appears when no end date chosen
                        with_portal=False,  # if True calendar will open in a full screen overlay portal
                        first_day_of_week=0,  # Display of calendar when open (0 = Sunday)
                        reopen_calendar_on_clear=True,
                        is_RTL=False,  # True or False for direction of calendar
                        clearable=True,  # whether or not the user can clear the dropdown
                        number_of_months_shown=1,  # number of months shown when calendar is open
                        min_date_allowed=sdate,  # minimum date allowed on the DatePickerRange component  e.g. dt(2007, 1, 1)
                        max_date_allowed=edate,  # maximum date allowed on the DatePickerRange component e.g. dt(2007, 1, 1)
                        initial_visible_month=dt(2017, 11, 1),  # the month initially presented when the user opens the calendar
                        start_date=dt(2017, 11, 1).date(),
                        end_date=edate,
                        display_format='YYYY-MM-DD',  # how selected dates are displayed in the DatePickerRange component.
                        month_format='MMMM, YYYY',  # how calendar headers are displayed when the calendar is opened.
                        minimum_nights=1,  # minimum number of days between start and end date

                        persistence=True,
                        persisted_props=['start_date','end_date'],
                        persistence_type='session',  # session, local, or memory. Default is 'local'

                        updatemode='bothdates'  # singledate or bothdates. Determines when callback is triggered
                    ),
                ],
                style={'width': '100%'} #,'align': 'stretch'
                ),
            ],
       ),
)

card_selector = dbc.Card(

    dbc.CardBody(
        [        
            
            dcc.Markdown(children=markdown_text),
            
            html.Div([

                dcc.Dropdown(
                    id='xaxis-column',
                    options=[{'label': i, 'value': i} for i in meters['meter_no']],
                    value='Meter_Number1'
                ),
            ],
            style={'width': '50%', 'height': '100%', 'display': 'inline-block'}
            ),
        
        
            html.Div([
                dcc.Dropdown(
                    id='yaxis-column',
                    options=[{'label': i, 'value': i} for i in meters['meter_no']],
                    value='Meter_Number2'
                ),
            ],
            style={'width': '50%', 'height': '100%','display': 'inline-block'}
            ),  
        ],
    ),
)


card_header = dbc.Card(
    [
        html.H3(children='Maules Ck Groundwater Monitoring Network'),
    ],        
)    
    
container_map = dbc.Container(
    [
        dbc.Col(card_map, 

        ),
    ]
)

    
container_picker = dbc.Container(
    [
        dbc.Col(card_selector, 

        ),
        
        dbc.Col(card_date_picker, 

        ),

        dbc.Col(card_map, 

        ),

    ],


)


#--------------------------------------------------------------------------------------------------
# TypeError: The `dash_bootstrap_components.Col` component (version 0.11.1) received an unexpected keyword argument: `justify`
# Allowed arguments: align, children, className, id, key, lg, loading_state, md, sm, style, width, xl, xs

app.layout = dbc.Container(children=[

        dbc.Row(dbc.Col(card_header, width=12),
            no_gutters=True
        ),

        dbc.Row(
            children=[
                dbc.Col(
                    [

                        dbc.Container(container_picker),

#                        dbc.Col(dbc.Button(id="Submit", n_clicks=0, children=["Submit"]),
#                                width={'size': 1, 'offset': 4}),

                    ],
                    width=5
                ),

                dbc.Col(
                    [
                        dbc.Col(card_graph),  # justify="start", "center", "end", "between", "around"
                        

                    ],
                    width=7,
                ),
            ],
            no_gutters=True,
        
        ),

#        dbc.Row(
#            [    
#                dbc.Col(
#                    [
#
#                        dbc.Container(container_map),
#                    ],
#                     width=5
#                )        
#            ],no_gutters=True
#        ),    
    ],
)


#--------------------------------------------------------------------------------------------------


@app.callback(
    Output(component_id='gw-graph', component_property='figure'),
   [Input(component_id='xaxis-column', component_property='value'),
    Input(component_id='yaxis-column', component_property='value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')],
    prevent_initial_call=False
   )

def update_graph(meter_no1, meter_no2, start_date, end_date): 
        

    dff = pd.DataFrame(columns=['meter_no','read_date_idx','read_date','level'])
    dff1 = pd.DataFrame(columns=['meter_no','read_date_idx','read_date','level'])
    dff2 = pd.DataFrame(columns=['meter_no','read_date_idx','read_date','level'])
    m1 = '00000'
    m2 = '00000'
    
    if len(meter_no1) > 0:
        dff1 = df[(df['meter_no'] == meter_no1)]
        dff1 = dff1.loc[start_date:end_date]
        m1 = dff1.iloc[0,0]
        
    #     raise dash.exceptions.PreventUpdate    
    
    if len(meter_no2) > 0:
        dff2 = df[(df['meter_no'] == meter_no2)]
        dff2 = dff2.loc[start_date:end_date]
        m2 = dff2.iloc[0,0]
        

        dff = pd.merge(dff1,dff2,left_index=True, right_index=True)

        dfe1 = dfe.loc[start_date:end_date]
        dfk1 = dfk.loc[start_date:end_date]
        

# subplots https://plotly.com/python/subplots/



    fig = make_subplots(
                rows=3, cols=1,
                subplot_titles=("Bore Comparison", "Elfin Surfacewater", "Kaputar Rainfall"))
    
    
    fig.append_trace(go.Scatter(x=dff['read_date_x'], y=dff['level_x'],name=m1), row=1, col=1)
    fig.append_trace(go.Scatter(x=dff['read_date_x'], y=dff['level_y'],name=m2), row=1, col=1)
    fig.append_trace(go.Scatter(x=dfe1['read_date'], y=dfe1['level'],name='CF41905'), row=2, col=1)
    fig.append_trace(go.Scatter(x=dfk1['read_date'], y=dfk1['level'],name='54151'), row=3, col=1)

    fig.update_yaxes(title_text="(AHD)", row=1, col=1)
    fig.update_yaxes(title_text="(m)", row=2, col=1)
    fig.update_yaxes(title_text="(mm)", row=3, col=1)
    fig.update_layout(height=800, width=600, title_text="Groundwater, Surfacewater Comparison")

    #trace1 = go.Scatter(x=dff['read_date_x'], 
    #                    y=dff['level_x'],
    #                    xaxis="x1",
    #                    yaxis="y1"
    #)
#
    #trace2 = go.Scatter(x=dff['read_date_x'], 
    #                    y=dff['level_y'],
    #                    xaxis="x1",
    #                    yaxis="y1"
    #)      
    #
    #trace3 = go.Scatter(x=dfe1['read_date'], 
    #                    y=dfe1['level'],
    #                    xaxis="x3",
    #                    yaxis="y3"
    #)
#
    #trace4 = go.Scatter(x=dfk1['read_date'], 
    #                    y=dfk1['level'],
    #                    xaxis="x4",
    #                    yaxis="y4"
    #)
#
    #data = [trace1, trace2, trace3, trace4]
#
    #layout = go.Layout(
#
    #    xaxis=dict(
    #        domain=[0, 0.45]
    #    ),
    #    yaxis=dict(
    #        domain=[0, 0.45]
    #    ),
    #    xaxis2=dict(
    #        domain=[0.55, 1]
    #    ),
    #    xaxis4=dict(
    #        domain=[0.55, 1],
    #        anchor="y4"
    #    ),
    #    yaxis3=dict(
    #        domain=[0.55, 1]
    #    ),
#
    #)
    #
    #fig = go.Figure(data=data, layout=layout)
        
    return fig 
    



def main():

    logs_dir = "/home/admin/dockers/waterdata_frontend/dash/logs/"
    check_file_writable(logs_dir)
    
    setupLogging(' DASH ', logs_dir)
    
    

    


if __name__ == '__main__':
   app.run_server(debug=True)
   