import dash_bootstrap_components as dbc
from dash import html


def create_navbar():
    
    navbar = html.H1('Maules Creek Water')
    
    # Create the Navbar using Dash Bootstrap Components
#    navbar = dbc.NavbarSimple(
#        children=[
#            dbc.DropdownMenu(
#                nav=True,
#                in_navbar=True,
#                label="Menu", # Label given to the dropdown menu
#                children=[
#                    # In this part of the code we create the items that will appear in the dropdown menu on the right
#                    # side of the Navbar.  The first parameter is the text that appears and the second parameter 
#                    # is the URL extension.
#                    dbc.DropdownMenuItem("Home", href='/'), # Hyperlink item that appears in the dropdown menu
#                    dbc.DropdownMenuItem(divider=True), # Divider item that appears in the dropdown menu 
#                    dbc.DropdownMenuItem(divider=True), 
#                    dbc.DropdownMenuItem("Summary", href='/summary'), # Hyperlink item that appears in the dropdown menu
#                    dbc.DropdownMenuItem(divider=True), 
#                    dbc.DropdownMenuItem("Surfacewater", href='/surfacewater'), # Hyperlink item that appears in the dropdown menu
#                    dbc.DropdownMenuItem(divider=True), 
#                    dbc.DropdownMenuItem("Groundwater", href='/groundwater'), # Hyperlink item that appears in the dropdown menu
#                    dbc.DropdownMenuItem(divider=True), 
#                    dbc.DropdownMenuItem("Rainfall", href='/rainfall'), # Hyperlink item that appears in the dropdown menu
#                ],
#            ),
#        ],
#        brand="Home",  # Set the text on the left side of the Navbar
#        brand_href="/",  # Set the URL where the user will be sent when they click the brand we just created "Home"
#        sticky="top",  # Stick it to the top... like Spider Man crawling on the ceiling?
#        color="dark",  # Change this to change color of the navbar e.g. "primary", "secondary" etc.
#        dark=True,  # Change this to change color of text within the navbar (False for light text)
#    )

    return navbar
