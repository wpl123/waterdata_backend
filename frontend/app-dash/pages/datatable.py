import dash
import dash_table
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

import pandas as pd

from utils.df_split import df_split
from navbar import create_navbar
from sidebar import create_meter_selector, create_sidebar


markdown_text = '''
        Hover over the data table, use the tools in the top right corner.
        '''

nav = create_navbar()
side = create_sidebar(markdown_text)
m_sel = create_meter_selector()

def make_datatable(data):
    
    df = pd.DataFrame(data)
    shiftPos = df.pop('read_date_x_x')
    df.insert(0,'read_date_x_x', shiftPos)
    
    columns_dict = {'read_date_x_x':'Date',
                    'meter_no_x_x':'GW 1', 
                    'level_x_x':'Level 1',
                    'meter_no_y_x':'GW 2', 
                    'level_y_x':'Level 2', 
                    'meter_no_x_y':'SW', 
                    'level_x_y':'SW Level', 
                    'meter_no_y_y':'RF', 
                    'level_y_y':'Rf Level'}
    df=df.rename(columns=columns_dict)
    
    #dff,dfe,dfk = df_split(df)
    #m1 = str(dff.iloc[0,0])
    #m2 = str(dff.iloc[0,3])
    
    # https://github.com/Coding-with-Adam/Dash-by-Plotly/blob/master/DataTable/datatable_intro_and_sort.py
    #
    layout = dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "hideable": True}    
        #    {"name": i, "id": i, "deletable": True, "selectable": True, "hideable": True}
        #    if i == "meter_no_x_x" or i == "year" or i == "id"
        #    else {"name": i, "id": i, "deletable": True, "selectable": True}
            for i in df.columns
        ],
        data=df.to_dict('records'),                  # the contents of the table
        editable=True,              # allow editing of data inside all cells
        filter_action="native",     # allow filtering of data by user ('native') or not ('none')
        sort_action="native",       # enables data to be sorted per-column by user or not ('none')
        sort_mode="single",         # sort across 'multi' or 'single' columns
        column_selectable="multi",  # allow users to select 'multi' or 'single' columns
        row_selectable="multi",     # allow users to select 'multi' or 'single' rows
        row_deletable=True,         # choose if user can delete a row (True) or not (False)
        selected_columns=[],        # ids of columns that user selects
        selected_rows=[],           # indices of rows that user selects
        page_action="native",       # all data is passed to the table up-front or not ('none')
        page_current=0,             # page number that user is on
        page_size=20,                # number of rows visible per page
        style_cell={                # ensure adequate header width when text is shorter than cell's text
            'minWidth': 95, 'maxWidth': 95, 'width': 95
        },
        #style_cell_conditional=[    # align text columns to left. By default they are aligned to right
        #    {
        #        'if': {'column_id': c},
        #        'textAlign': 'left'
        #    } for c in ['country', 'iso_alpha3']
        #],
        # Styling --> https://dash.plotly.com/datatable/style
        style_header={
        'backgroundColor': 'rgb(30, 30, 30)',
        'color': 'white'
        },
        style_data={                # overflow cells' content into multiple lines
            'whiteSpace': 'normal',
            'height': 'auto',
            'backgroundColor': 'rgb(50, 50, 50)',
            'color': 'white'
        },
        tooltip_delay=1000,     # 0  
        tooltip_duration=2000,  # None
        tooltip_data=[{
            'GW 1': {
                'value': 'Test'
                },
        }]
    ),

    #html.Br(),
    #html.Br(),
        
    #])
    
    return layout





def create_page_datatable(data):
    #print("data: ",data)
    table = make_datatable(data)
    
    layout = dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Maules Creek Water",
                            className='text-centre text-primary mb-4'),width=12)
        ]),
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        dbc.Row(side),
                        dbc.Row(m_sel),
                    ],width=2),
                dbc.Col(table),    
            ]
        )
        
    ])
    return layout