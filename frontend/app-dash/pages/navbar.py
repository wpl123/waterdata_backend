import dash_bootstrap_components as dbc
from dash import html


def create_navbar():
    
    #navbar = html.H4('Maules Creek Water')
    #navbar = dbc.Row(
    #    [dbc.Col(html.Div("Navigate"), width=2), dbc.Col(html.Div("Maules Creek Water"), width=10)]
    #) 
    navbar = dbc.Col(html.H1("Maules Creek Water", className='text-centre text-primary mb-4'),width=12)
    return navbar
