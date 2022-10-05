import dash
from dash import html
from navbar2_2 import create_navbar
from sidebar2_2 import create_sidebar

dash.register_page(__name__, path='/rainfall')

nav = create_navbar()
side = create_sidebar()
header = html.H3('Rainfall Data')


def create_page_rainfall():
    layout = html.Div([
        nav,
        side,
    ])
    return layout