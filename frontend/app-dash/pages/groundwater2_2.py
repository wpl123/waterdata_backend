import dash
from dash import html
from navbar2_2 import create_navbar
from sidebar2_2 import create_sidebar

dash.register_page(__name__, path='/groundwater')

nav = create_navbar()
side = create_sidebar()

header = html.H3('Groundwater Data')


def create_page_groundwater():
    layout = html.Div([
        nav,
        side,
    ])
    return layout