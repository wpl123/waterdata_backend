import dash
from dash import html, dcc, callback, Input, Output

dash.register_page(__name__)


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
layout = html.Div(children=[
    html.H1(children='This is our Analytics page'),
	html.Div([
        "Select a city: ",
        dcc.RadioItems(['New York City', 'Montreal','San Francisco'],
        'Montreal',
        id='analytics-input')
    ]),
	html.Br(),
    html.Div(id='analytics-output'),
])