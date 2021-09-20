import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import plotly.graph_objs as go
import plotly.express as px
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash_extensions.javascript import arrow_function

from dash.dependencies import Input, Output


card_main = dbc.Card(
    [
        dbc.CardImg(src="/assets/ball_of_sun.jpg", top=True, bottom=False,
                    title="Image by Kevin Dinkel", alt='Learn Dash Bootstrap Card Component'),
        dbc.CardBody(
            [
                html.H4("Learn Dash with Charming Data", className="card-title"),
                html.H6("Lesson 1:", className="card-subtitle"),
                html.P(
                    "Choose the year you would like to see on the bubble chart.",
                    className="card-text",
                ),
                dcc.Dropdown(id='user_choice', options=[{'label': yr, "value": yr} for yr in df.year.unique()],
                             value=2007, clearable=False, style={"color": "#000000"}),
                # dbc.Button("Press me", color="primary"),
                # dbc.CardLink("GirlsWhoCode", href="https://girlswhocode.com/", target="_blank"),
            ]
        ),
    ],
    color="dark",   # https://bootswatch.com/default/ for more card colors
    inverse=True,   # change color of text (black or white)
    outline=False,  # True = remove the block colors from the background and header
)


card_question = dbc.Card(
    [
        dbc.CardBody([
            html.H4("Question 1", className="card-title"),
            html.P("What was India's life expectancy in 1952?", className="card-text"),
            dbc.ListGroup(
                [
                    dbc.ListGroupItem("A. 55 years"),
                    dbc.ListGroupItem("B. 37 years"),
                    dbc.ListGroupItem("C. 49 years"),
                ], flush=True)
        ]),
    ], color="warning",
)

card_graph = dbc.Card(
        dcc.Graph(id='my_bar', figure={}), body=True, color="secondary",
)