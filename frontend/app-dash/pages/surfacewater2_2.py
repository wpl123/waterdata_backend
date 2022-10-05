import dash
from dash import html
from navbar2_2 import create_navbar
from sidebar2_2 import create_sidebar

dash.register_page(__name__, path='/surfacewater')

nav = create_navbar()
side = create_sidebar()

header = html.H3('Surfacewater Data')


def create_page_surfacewater():
    layout = html.Div([
        nav,
        side,
    ])
    return layout