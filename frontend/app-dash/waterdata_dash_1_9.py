# -*- coding: utf-8 -*-
import json
import geojson

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

import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash_extensions.javascript import arrow_function

from dash.dependencies import Input, Output
from datetime import datetime as dt, date

from utils.dbutils import *
from utils.flutils import *
from utils.dash_dbutils import *


#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = ['https://codepen.io/anon/pen/mardKv.css']
#external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#app = dash.Dash(__name__, external_stylesheets=dbc.themes.BOOTSTRAP)
#app = dash.Dash(__name__)

#theme =  {
#    'dark': True,
#    'detail': '#007439',
#    'primary': '#00EA64',
#    'secondary': '#6E6E6E',
#}

mysql = MySQLUtil()
mysql.dbConnect(host ='192.168.11.6', user = 'root', psw = 'water', db_name = 'waterdata', port=30000)

#app = dash.Dash()

# All Meter Data
meters = pd.DataFrame(get_meters(mysql), columns=['meter_no','meter_name','meter_type','lat','lng', 'url'])
df = pd.concat([get_meter_data(mysql, meters.iloc[i,0], meters.iloc[i,2]) for i in range(len(meters))])
df.columns = ['meter_no','read_date_idx','read_date','level']
df['read_date_idx'] = pd.to_datetime(df['read_date_idx'])
df.set_index('read_date_idx',inplace=True,drop=True)

sdate = df.iloc[0,1]
edate = df.iloc[-1,1]
syear = int(sdate.strftime('%Y'))
eyear = int(edate.strftime('%Y'))

color_prop = 'meter_type'

# Elfin Surfacewater Data
dfe = pd.DataFrame(get_surfacewater(mysql,'419051',sdate,edate))
dfe.columns = ['meter_no','read_date_idx','read_date','level']
dfe['read_date_idx'] = pd.to_datetime(dfe['read_date_idx'])
dfe.set_index('read_date_idx',inplace=True,drop=True)

# Kaputar Rainfall Data
dfk = pd.DataFrame(get_rainfall(mysql,'054151-2',sdate,edate))
dfk.columns = ['meter_no','read_date_idx','read_date','level']
dfk['read_date_idx'] = pd.to_datetime(dfk['read_date_idx'])
dfk.set_index('read_date_idx',inplace=True,drop=True)

# Get 10 day moving average of rainfall
dfk['MA90'] = (dfk['level'].rolling(window=90).mean())

#df_ma90 = (dfk['level'].rolling(window=90).mean())

#dfk = pd.merge(dfk,df_ma90,left_index=True, right_index=True)
#dfk = dfk.replace('NaN', 0) # ,inplace=True
 
# Add rainfall bins for the moving average TODO: don't appear to work.

# dfk['rf_bin'] = pd.cut(
#     dfk['MA90'],
#     bins=[-1,40,80,120,160],                             
#     labels=[1,2,3,4],
#     include_lowest=True
#     )

# Remove nan's
#dfk.dropna(inplace=True)

# Wait for the user input to terminate the program
#input("Loaded dfk. Press any key to continue")

    #print("-1.",dfk)
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
	

def get_data():
    
    df_meters = meters[['lat', 'lng', 'meter_no', 'meter_name', 'url', 'meter_type']]
    
    data = df_to_geojson(df_meters, ['meter_no','meter_name','url','meter_type'],"lat","lng")
    
    geobuf = dlx.geojson_to_geobuf(data)  # convert to geobuf
    return geobuf


def get_info(feature=None):
    header = [html.H4("Monitoring Station Data")]
    if not feature:
        return header + ["Hoover over a marker"]
    return header + [html.B(feature["properties"]["meter_no"]), 
                     (": "),
                     (feature["properties"]["meter_name"]), 
                                                   #TODO:  ("Coords: "),(feature["geometry"]["type"]["Point"]),
                     html.Br()]  



markdown_text = '''##### Using this dashboard

Select two groundwater monitoring bores that you wish to compare, then select the start and finish dates that are of interest.

Hover over the pins to the left to determine the bore numbers to select
'''


#--------------------------------------------------------------------------------------------------


card_dials = dbc.Card(

    dbc.Col(
        [
            dbc.Row(
                children=[
                    dbc.Col(dcc.Graph(id='gw-dial', figure={})),
                    dbc.Col(dcc.Graph(id='sw-dial', figure={})), #, width=6
#                    dcc.Graph(id='gw-dial', figure={}),
#                    dcc.Graph(id='sw-dial', figure={}),
                ],no_gutters=True
            ),
        ],                      #width=12 
    ),
       
)

card_heatmap = dbc.Card(
    [
        dcc.Graph(id='gw-heatmap', figure={})
    ]  
)

card_scatter = dbc.Card(
    [
        dcc.Graph(id='gw-scatter', figure={})
    ]  
)

card_big_graph = dbc.Card(

        dcc.Graph(id='gw-graph', figure={})
        
)

card_table = dbc.Card(

        dcc.Input(id='gw-table', value={})
        
)

# https://community.plotly.com/t/google-map-integration-with-dash-web-framework/38211/4
# zoom and center to marker --> https://jeffreymorgan.io/articles/how-to-center-a-leaflet-map-on-a-marker/

card_map = dbc.Card(
    [        
        html.Div(
            [
    
                dl.Map(center=[-30.50, 150.10], zoom=10, children=[
#                    dl.TileLayer(),
                    dl.TileLayer(url="http://www.google.cn/maps/vt?lyrs=s@189&gl=cn&x={x}&y={y}&z={z}"),
#                    dl.GeoTIFFOverlay(id=GEOTIFF_ID, interactive=True, style={'width': '1000px', 'height': '500px'}),
                    dl.GeoJSON(data=get_data(), id="monitor", format="geobuf",
                    hoverStyle=arrow_function(dict(weight=5, color='#666', dashArray=''))),
                ], style={'width': '100%', 'height': '54vh','margin': "auto", }, id="map"), #"display": "block"  
            ],
        ),
        html.Div(id="monitors"),
    ]        
)

card_picker = dbc.Card(

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
                        start_date=dt(2007, 11, 1).date(),
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
                style={'width': '110%'} #,'align': 'stretch'
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
    dbc.CardBody(
        [
            html.H3(children='Maules Creek Water Monitoring Network'),
        ],
    ),            
)


#--------------------------------------------------------------------------------------------------
# TypeError: The `dash_bootstrap_components.Col` component (version 0.11.1) received an unexpected keyword argument: `justify`
# Allowed arguments: align, children, className, id, key, lg, loading_state, md, sm, style, width, xl, xs

app.layout = dbc.Container(children=[


        dbc.Row(
            children=[
                
                dbc.Col(
                    children=[

#                        dbc.Card(card_dials),
                        dbc.Card(card_map),
                        dbc.Card(card_scatter),
                    ],
                    width=3
                ), 
                
                dbc.Col(
                    children=[
                            
                        dbc.Card(card_header),
                        dbc.Card(card_selector),    
                        dbc.Card(card_picker),
                        dbc.Card(card_heatmap),
                    ],
                    width=3
                ),

                dbc.Col(
                    [
                        dbc.Col(card_big_graph),  # justify="start", "center", "end", "between", "around"
#                        dbc.Col(card_table),
                        html.P("Position of hline"),
                        dcc.Slider(                 # https://community.plotly.com/t/solved-has-anyone-made-a-date-range-slider/6531/8
                            id='year-slider', 
                            min=syear, max=eyear, value=(eyear - 4), step=1.0,
                            marks={1: str(syear), 7: str(eyear)}
                        )
                    ],
                    width=6,
                ),
            ],
            no_gutters=True,
        
        ),  
    ],fluid=True
)




@app.callback(Output("monitors", "children"), [Input("monitor", "hover_feature")])
def info_hover(feature):
    if feature is not None:
 #       print(feature)
        return get_info(feature)



@app.callback(
   [Output(component_id='gw-graph', component_property='figure'),
    Output(component_id='gw-scatter', component_property='figure'),
    Output(component_id='gw-heatmap', component_property='figure'),
    ],
   [Input(component_id='xaxis-column', component_property='value'),
    Input(component_id='yaxis-column', component_property='value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input("year-slider", "value")],
    prevent_initial_call=False
   )

def update_graph(meter_no1, meter_no2, startdate, enddate, line_pos): 
        
#    input("Start of Update Graph Press any key to continue")

    dff = pd.DataFrame(columns=['meter_no','read_date_idx','read_date','level'])
    dff1 = pd.DataFrame(columns=['meter_no','read_date_idx','read_date','level'])
    dff2 = pd.DataFrame(columns=['meter_no','read_date_idx','read_date','level'])


    #   Create Rainfall and Streamflow df for the date range

    dfe1 = dfe.loc[startdate:enddate]
    dfk1 = dfk.loc[startdate:enddate]
    
    startyear = startdate[0:3]
    endyear = enddate[0:3]

    print (startdate)
    print (enddate)

    #print(dfk1)

    m1 = '00000'
    m2 = '00000'
    m1_name = ''
    m2_name = ''
    s1_title = 'Bore Comparison'
    

#   input("Before meter info. Press any key to continue")

    if len(meter_no1) > 0:
        dff1 = df[(df['meter_no'] == meter_no1)]
        dff1 = dff1.loc[startdate:enddate]
        m1 = meter_no1 
        m1_name = meters[(meters['meter_no'] == meter_no1)]

    if len(meter_no2) > 0:
        dff2 = df[(df['meter_no'] == meter_no2)]
        dff2 = dff2.loc[startdate:enddate]
        m2 = meter_no2  
        m2_name = meters[(meters['meter_no'] == meter_no2)]  

        dff = pd.merge(dff1,dff2,left_index=True, right_index=True)

#        input("Inside meter info. Press any key to continue")
#   Create concatenated df for the heatmap

        df_join = pd.merge(dff,dfe1,left_index=True, right_index=True)
        df_join1 = df_join.drop(columns=['meter_no_x', 'read_date_x', 'meter_no_y', 'read_date_y'],axis=1)
        df_join2 = pd.merge(df_join1,dfk1,left_index=True, right_index=True)
        df_join3 = df_join2.drop(columns=['meter_no_x', 'read_date_x', 'meter_no_y', 'read_date_y'],axis=1)
       
        df_join3.columns = [m1,m2,'Elfin Crossing','Kaputar Rainfall','MA90'] #
        
        df_join3 = df_join3.dropna() #(axis=0, how='any', thresh=None, subset=None, inplace=False)
        
        df_join3 = df_join3.apply(pd.to_numeric)
        df_join3 = df_join3.drop(columns=['MA90'])
        df_corr = df_join3.corr(method='spearman')
        
        print(df_corr)
        print(df_corr.dtypes)
        
       
#        input("After correlation. Press any key to continue")

#    input("Before make plots. Press any key to continue")
# subplots https://plotly.com/python/subplots/

    fig = make_subplots(
                rows=4, cols=1,
                subplot_titles=("Groundwater", "Elfin Surfacewater", "Kaputar Rainfall", "Kaputar Rainfall MA (90)"))
    
    fig.append_trace(go.Scatter(x=dff['read_date_x'], y=dff['level_x'],name=m1), row=1, col=1)
    fig.append_trace(go.Scatter(x=dff['read_date_x'], y=dff['level_y'],name=m2), row=1, col=1)
    fig.add_vline(x=line_pos, line_width=3, line_dash="dash",line_color="green", row=1, col=1)
    fig.append_trace(go.Scatter(x=dfe1['read_date'], y=dfe1['level'],name='41905'), row=2, col=1)
    fig.append_trace(go.Scatter(x=dfk1['read_date'], y=dfk1['level'],name='054151-2',opacity=1), row=3, col=1)
    fig.append_trace(go.Scatter(x=dfk1['read_date'], y=dfk1['MA90'],name='054151-2 (MA90)',mode='lines',opacity=1), row=4, col=1)

    fig.update_traces(marker_color='#0508fb',selector=dict(type='bar'), row=3, col=1)

    fig.update_yaxes(title_text="(AHD)", row=1, col=1)
    fig.update_yaxes(title_text="(m)", row=2, col=1)
    fig.update_yaxes(title_text="(mm)", row=3, col=1)
    fig.update_yaxes(title_text="(mm)", row=4, col=1)
    
    fig.update_layout(title_text="Groundwater, Surfacewater Comparison",title_font_size=30,height=875,width=930) #height=875,width=930, textfont_color=
    
    # https://plotly.com/python/horizontal-vertical-shapes/
    # fig.add_vline(
    #     x=10, line_width=3, line_dash="dash", 
    #     line_color="green")
    # fig.add_hrect(
    #     y0=0.9, y1=2.6, line_width=0, 
    #     fillcolor="red", opacity=0.2)
    
    fig1 = px.scatter(dff, x='level_x', y='level_y')
    fig1.update_layout(hovermode='closest',xaxis_title=m1,yaxis_title=m2,title='Scatter Plot',title_font_size=30) # ,height=400, width=465 / height=250, width=250 400
    
    fig2 = px.imshow(df_corr)
    fig2.update_layout(hovermode='closest',title='Correlation Heatmap',title_font_size=30) #,height=500, width=500
    
    
    return (fig, fig1, fig2)









def main():

    logs_dir = "/home/admin/dockers/waterdata_frontend/dash/logs/"
    check_file_writable(logs_dir)
    
    setupLogging(' DASH ', logs_dir)
    
    

    


if __name__ == '__main__':
   app.run_server(debug=True,host='192.168.11.6',port=8050)
   