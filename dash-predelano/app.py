from dash import Dash, dcc
import dash_bootstrap_components as dbc
import dash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import *
import seeders.order_seeder as order_seeder
import seeders.user_seeder as user_seeder

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
	   suppress_callback_exceptions=True, prevent_initial_callbacks=True)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
server = app.server

# Seeding db
#order_seeder.seed()
#user_seeder.seed()

############################################################################################
# Import shared components

from assets.footer import _footer
from assets.nav import _nav

############################################################################################
# App Layout
app.layout = dbc.Container([
	
	dbc.Row([
        dbc.Col([_nav], width = 2),
        dbc.Col([
            dbc.Row([dash.page_container])
	    ], width = 10),
    ]),
    dbc.Row([
        dbc.Col([], width = 2),
        dbc.Col([
            dbc.Row([_footer])
	    ], width = 10),
    ]),
     dcc.Store(id='browser-memo', data=dict(), storage_type='session')
], fluid=True)

############################################################################################
# Run App
if __name__ == '__main__':
	app.run_server(debug=True)
