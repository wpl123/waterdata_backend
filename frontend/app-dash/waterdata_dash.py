# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go


df = pd.read_csv("./dash/all_training_data.csv")

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
# app.css.append_css ({“external_url”:https://codepen.io/chriddyp/pen/bwLwgP.css})  ## TODO
app.layout = html.Div(children=[
   html.H4(children='Groundwater Data'),
   generate_table(df)
])

if __name__ == '__main__':
   app.run_server(debug=True)