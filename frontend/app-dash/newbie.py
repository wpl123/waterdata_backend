import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

controls = dbc.Card(
    [
        dbc.FormGroup(
            [
               dbc.Label('Choose input or dropdown'),
               dbc.RadioItems(
                   id='radio',
                   options=[
                       {'label': 'input', 'value': 'input'},
                       {'label': 'dropdown', 'value': 'dropdown'},
                   ],
                   value='input',
               ),
            ]
        ),
        dbc.FormGroup(id='input-form', children=
            [
                dbc.Label('Input', id='input-label'),
                dbc.Input(
                    id='input',
                    type='number',
                    min=1, max=100, step=1, value=5
                ),
            ]
        ),
        dbc.FormGroup(id='dropdown-form', children=
            [
                dbc.Label('Dropdown', id='dropdown-label'),
                dcc.Dropdown(
                    id='dropdown',
                    options=[
                        {'label': 'Hello'+str(i), 'value': 'Hello'+str(i)} for i in range(100)
                    ],
                    multi=True,
                    placeholder='Say Hello',
                ),
            ]
        ),
    ],
    body=True,
    color='light',
)

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(controls, md=4)
            ],
            align='center',
        ),
    ],
    fluid=True,
)

@app.callback([Output('input-form', 'style'), Output('dropdown-form', 'style')],
    [Input('radio', 'value')])
def visibility(selected_type):

    if selected_type == 'input':

        return {'display': 'block'}, {'display': 'none'}

    else:

        return {'display': 'none'}, {'display': 'block'}

if __name__ == '__main__':
    app.run_server(debug=True)