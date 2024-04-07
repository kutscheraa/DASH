import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/', name='Home', title='Homepage')

layout = dbc.Container([
    # title
    dbc.Row([
        dbc.Col([
            html.H3(['Welcome!']),
            html.P([html.B(['App Overview'])], className='par')
        ], width=12, className='row-titles')
    ]),
    # Guidelines
    dbc.Row([
        dbc.Col([], width = 2),
        dbc.Col([
            html.P([html.B('1) Setup'),html.Br(),
                    'Test application to verify instalation.'], className='guide'),
            html.P([html.B('2) Simple app'),html.Br(),
                    'Simple application with line graph from csv.',html.Br(),
                    'The app could work with any .csv file.'], className='guide'),
            html.P([html.B('3) Advanced app'),html.Br(),
                    'Application with map, two pie charts and line graph.',html.Br(),
                    'App uses geojson data to create map and data extracted from mysql database.',html.Br(),
                    'Data is used to show orders per region, % of each item type and so on.'], className='guide'),
        ], width = 8),
        dbc.Col([], width = 2)
    ])
])
