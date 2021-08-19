import dash

import dash_core_components as dcc

import dash_html_components as html

import pandas as pd


data = pd.read_csv("all_training_data")

data = data.query("meter_no == 'conventional' and region == 'Albany'")

data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")

data.sort_values("Date", inplace=True)


app = dash.Dash(__name__)