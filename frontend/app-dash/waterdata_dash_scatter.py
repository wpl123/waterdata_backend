# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

from dash.dependencies import Input, Output

import pymysql
from utils.dbutils import *
from utils.flutils import *

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


def get_data():

   
   logs_dir = "/home/admin/dockers/waterdata_frontend/dash/logs/"
   check_file_writable(logs_dir)
   
   setupLogging(' DASH ', logs_dir)
   
   # mysql = MySQLUtil()
   # mysql.dbConnect(host ='192.168.11.6', user = 'root', psw = 'water', db_name = 'waterdata', port=30000)

   connection = pymysql.connect(
      # host='192.168.208.1',
      host='192.168.11.6',
      user='root', 
      password='water',
      database='waterdata',
      port=30000)


   try:
      with connection.cursor() as cursor:
   
         sql = ('''  SELECT 
                        `A`.`read_date`, 
                        `A`.`meter_no` AS `bl_meter1`, `A`.`bl_ahd` AS `bl_ahd1`, `A`.`mean_temp` AS `mean_temp1`,
                        `B`.`meter_no` AS `bl_meter2`, `B`.`bl_ahd` AS `bl_ahd2`, `B`.`mean_temp` AS `mean_temp2`,
                        `E`.`meter_no` AS `bl_meter3`, `E`.`bl_ahd` AS `bl_ahd3`, `E`.`mean_temp` AS `mean_temp3`,
                        `F`.`meter_no` AS `bl_meter4`, `F`.`bl_ahd` AS `bl_ahd4`, `F`.`mean_temp` AS `mean_temp4`,
                        `C`.`meter_no` AS `meter_no3`, `C`.`sl_read1` AS `sl_read1`,
                        `D`.`meter_no` AS `meter_no4`, `D`.`rf_read1` AS `rf_read1`
                  FROM   
                        `groundwater` AS `A`  
                  INNER JOIN
                        `groundwater` `B` ON (`B`.`meter_no` = "GW967137.2.2" AND `B`.`read_date` = `A`.`read_date` )
                  INNER JOIN
                        `groundwater` `E` ON (`E`.`meter_no` = "GW967138.1.1" AND `E`.`read_date` = `A`.`read_date` )
                  INNER JOIN
                        `groundwater` `F` ON (`F`.`meter_no` = "GW967138.2.2" AND `F`.`read_date` = `A`.`read_date` )
                  INNER JOIN
                        `surfacewater` `C` ON (`C`.`meter_no` = "CF419051" AND `C`.`read_date` = `A`.`read_date` )
                  INNER JOIN
                        `rainfall` `D` ON (`D`.`meter_no` = "54151" AND `D`.`read_date` = `A`.`read_date` )
                  WHERE  
                        `A`.`meter_no` = "GW967137.1.1"
                  ''')
         
         
         sql1 = ('''  SELECT `meter_no`, `meter_name` FROM `meters` 
               ''')

         sql2 = (''' SELECT `meter_no`, `read_date`, `bl_ahd` AS `level` 
                     FROM `groundwater`         
                     WHERE `meter_no` = '{0} AND `read_date` >= '{}' AND `read_date` <= '{}'
                  ''')
         sql3 = (''' SELECT `meter_no`, `read_date`, `sl_read1` AS `level` 
                     FROM `surfacewater`         
                     WHERE `meter_no` = '{0} AND `read_date` >= '{}' AND `read_date` <= '{}'
                  ''')
         sql4 = (''' SELECT `meter_no`, `read_date`, `rf_read1` AS `level` 
                     FROM `rainfall`         
                     WHERE `meter_no` = '{0} AND `read_date` >= '{}' AND `read_date` <= '{}'
                  ''')

   
         df1 = pd.read_sql_query(sql, connection, parse_dates=['read_date','%Y-%m-%d'], coerce_float=True)
         df2 = pd.read_sql_query(sql1, connection)
   except:
         
      print("Error: unable to convert the data")

   connection.close() 
   # df = pd.DataFrame(mysql.execQuery(sql))
   # df.columns['read_date','bl_meter1','bl_ahd1','mean_temp1','bl_meter2','bl_ahd2','mean_temp2','bl_meter3','bl_ahd3','mean_temp3','bl_meter4','bl_ahd4','mean_temp4','meter_no3','sl_read1','meter_no4','rf_read1']
   return([df1,df2])



def generate_table(dataframe, max_rows=10):
   return html.Table(
      # Header
      [html.Tr([html.Th(col) for col in dataframe.columns])] +
      # Body
      [html.Tr([
         html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
      ]) for i in range(min(len(dataframe), max_rows))]
   )
	
app = dash.Dash()

values = []
data = []
meters = []

values = get_data()
data = values[0]

meters = values[1]
study = ['scatter','bar','line','heatmap']


fig = px.scatter(data, x="bl_ahd1", y="bl_ahd2")


markdown_text = '''
### Dash and Markdown

Dash apps can be written in Markdown.
Dash uses the [CommonMark](http://commonmark.org/)
specification of Markdown.
Check out their [60 Second Markdown Tutorial](http://commonmark.org/help/)
if this is your first introduction to Markdown!
'''

app.layout = html.Div(children=[
   html.H1(children='GW936137.1.1 V GW936137.2.2'),

   html.Div(children='''
      Dashboard: Maules Creek Data Monitoring Visualisations.
   '''),

   dcc.Markdown(children=markdown_text),

   html.Div([

      dcc.Dropdown(
         id='xaxis-column',
         options=[{'label': i, 'value': i} for i in meters['meter_no']],
         value='Meter_Number1'
      ),
      
      # dcc.Slider(
      #    id='year-slider',
      #    min=data['read_date'].min(),
      #    max=data['read_date'].max(),
      #    value=data['read_date'].min(),
      #    marks={str(read_date): str(read_date) for read_date in data['read_date'].unique()},
      #    step=None
      #    ),
# 
# 
      # dcc.RadioItems(
      #    id='xaxis-type',
      #    options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
      #    value='Linear',
      #    labelStyle={'display': 'inline-block'}
      # )
   ],
   style={'width': '33%', 'display': 'inline-block'}),

   
   html.Div([
      dcc.Dropdown(
         id='yaxis-column',
         options=[{'label': i, 'value': i} for i in meters['meter_no']],
         value='Meter_Number'
      ),
   ],
   style={'width': '33%', 'display': 'inline-block'}), 
   
   
   html.Div([
      dcc.Dropdown(
         id='study_type',
         options=[{'label': i, 'value': i} for i in study],
         value='Study'
      ),
   ],
   style={'width': '33%', 'display': 'inline-block'}), 

   dcc.Graph(
      id='example-graph',
      figure=fig
   )
])

@app.callback(
   Output('indicator-graphic', 'figure'),
   Input('xaxis-column', 'value'),
   Input('yaxis-column', 'value'),
   Input('study_type', 'value'),
#   Input('year--slider', 'value')
   )



def update_graph(xaxis_column_name, yaxis_column_name,
               study_name):
               
   print(study_name)
      
#   dff = data[data[col] = xaxis_column_name]
#    dff = df[df['Year'] == year_value]
#
#   fig = px.scatter(x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
#                     y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
#                     hover_name=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'])
#
#   fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')
#
#   fig.update_xaxes(title=xaxis_column_name,
#                     type='linear' if study_type == 'Linear' else 'log')
#
#   fig.update_yaxes(title=yaxis_column_name,
#                     type='linear' if study_type == 'Linear' else 'log')
#
#   return fig

# app.layout = html.Div([
#    dcc.Graph(
#       id='life-exp-vs-gdp',
#       figure={
#          'data': [
#             go.Scatter(
#                x=df[df['read_date'] == i]['bl_ahd1'],
#                y=df[df['read_date'] == i]['bl_ahd2'],
#                text=df[df['bl_ahd1'] == i]['bl_ahd2'],
#                mode='markers',
#                opacity=0.7,
#                marker={
#                   'size': 15,
#                   'line': {'width': 0.5, 'color': 'white'}
#                },
#                name=i
#             ) for i in df.bl_meter1.unique()
#          ],
#          'layout': go.Layout(
#             xaxis={'type': 'log', 'title': 'Date Title'},
#             yaxis={'title': 'AHD Title'},
#             margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
#             legend={'x': 0, 'y': 1},
#             hovermode='closest'
#          )
#       }
#    )
# ])

if __name__ == '__main__':
   app.run_server(debug=True)
   