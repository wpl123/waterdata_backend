# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import pymysql

import plotly.graph_objs as go
import plotly.express as px
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
app = dash.Dash(__name__, external_stylesheets=dbc.themes.CYBORG)
#app = dash.Dash(__name__)

mysql = MySQLUtil()
mysql.dbConnect(host ='192.168.11.6', user = 'root', psw = 'water', db_name = 'waterdata', port=30000)

app = dash.Dash()


meters = pd.DataFrame(get_meters(mysql), columns=['meter_no','meter_name','meter_type','lat','lon'])
df = pd.concat([get_meter_data(mysql, meters.iloc[i,0], meters.iloc[i,2]) for i in range(len(meters))])
df.columns = ['meter_no','read_date_idx','read_date','level']
df['read_date_idx'] = pd.to_datetime(df['read_date_idx'])
df.set_index('read_date_idx',inplace=True,drop=True)
sdate = df.iloc[0,1]
edate = df.iloc[-1,1]

#df1 = pd.melt(df, id_vars =['read_date'])


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
### Dash and Markdown

Dash apps can be written in Markdown.
Dash uses the [CommonMark](http://commonmark.org/)
specification of Markdown.
Check out their [60 Second Markdown Tutorial](http://commonmark.org/help/)
if this is your first introduction to Markdown!
'''

app.layout = html.Div(children=[
   html.H2(children='Maules Ck Groundwater Monitoring'),

    html.Div([
            
      dl.Map(center=[-30, 150], zoom=10, children=[
         dl.TileLayer(),
         dl.GeoJSON(data=maulesck),  # in-memory geojson (slowest option)
         dl.GeoJSON(data=brisbane, format="geobuf"),  # in-memory geobuf (smaller payload than geojson)
         dl.GeoJSON(url="/assets/us-state-capitals.json", id="capitals"),  # geojson resource (faster than in-memory)
         dl.GeoJSON(url="/assets/us-states.pbf", format="geobuf", id="states",
                  hoverStyle=arrow_function(dict(weight=5, color='#666', dashArray=''))),  # geobuf resource (fastest option)
      ], style={'width': '50%', 'height': '50vh', 'margin': "autoPanPaddingTopLeft", "display": "block"}, id="map"),
    ],),
    
    
   # html.Div(children='''
   #    Dashboard: Maules Creek Data Monitoring Visualisations.
   # '''),
   # 
   # dcc.Markdown(children=markdown_text),
 
   html.Div([

      dcc.Dropdown(
         id='xaxis-column',
         options=[{'label': i, 'value': i} for i in meters['meter_no']],
         value='Meter_Number1'
      ),
    ],
    style={'width': '30%', 'height': '130%', 'display': 'inline-block'}),



   html.Div([
      dcc.Dropdown(
         id='yaxis-column',
         options=[{'label': i, 'value': i} for i in meters['meter_no']],
         value='Meter_Number2'
      ),
   ],
   style={'width': '30%', 'display': 'inline-block'}), 
   
   
   html.Div([

       dcc.DatePickerRange(
        id='my-date-picker-range',  # ID to be used for callback
        calendar_orientation='horizontal',  # vertical or horizontal
        day_size=39,  # size of calendar image. Default is 39
        end_date_placeholder_text="End Date",  # text that appears when no end date chosen
        with_portal=True,  # if True calendar will open in a full screen overlay portal
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
        minimum_nights=2,  # minimum number of days between start and end date

        persistence=True,
        persisted_props=['start_date','end_date'],
        persistence_type='session',  # session, local, or memory. Default is 'local'

        updatemode='bothdates'  # singledate or bothdates. Determines when callback is triggered
    ),
   ],
   style={'width': '30%', 'display': 'inline-block'}), 

   dcc.Graph(
      id='example-graph',
      figure={}
   )
])




@app.callback(
   Output(component_id='example-graph', component_property='figure'),
   [Input(component_id='xaxis-column', component_property='value'),
    Input(component_id='yaxis-column', component_property='value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')],
#   Input('study_type', 'value'),
#   Input('year--slider', 'value')
    prevent_initial_call=False
   )

def update_graph(meter_no1, meter_no2, start_date, end_date): 
        

    dff = pd.DataFrame(columns=['meter_no','read_date_idx','read_date','level'])
    dff1 = pd.DataFrame(columns=['meter_no','read_date_idx','read_date','level'])
    dff2 = pd.DataFrame(columns=['meter_no','read_date_idx','read_date','level'])
    
    
    if len(meter_no1) > 0:
        dff1 = df[(df['meter_no'] == meter_no1)]
        dff1 = dff1.loc[start_date:end_date]
    
    #     raise dash.exceptions.PreventUpdate    
    
    if len(meter_no2) > 0:
        dff2 = df[(df['meter_no'] == meter_no2)]
        dff2 = dff2.loc[start_date:end_date]
        dff = pd.merge(dff1,dff2,left_index=True, right_index=True)
        
    
    fig = px.line(dff, x='read_date_x', y=['level_x','level_y'])
    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest',xaxis_title='Time',yaxis_title='AHD',title='Comparison')
    
    return fig
    



def main():

    logs_dir = "/home/admin/dockers/waterdata_frontend/dash/logs/"
    check_file_writable(logs_dir)
    
    setupLogging(' DASH ', logs_dir)
    
    

    


if __name__ == '__main__':
   app.run_server(debug=True)
   