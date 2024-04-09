import dash
from dash import html, Input, Output, callback, dcc
import dash_bootstrap_components as dbc
import dash_auth
from dash_auth import BasicAuth
from sqlalchemy.orm import sessionmaker
from db import *

dash.register_page(__name__, path='/', name='Login', title='Login')

# sql
def check_credentials(username, password):
    Session = sessionmaker(bind=engine)
    session = Session()
    user = session.query(User).filter_by(username=username, password=password).first()
    session.close()
    return user is not None

# layout
layout = dbc.Container([
    dbc.Row([
        dbc.Col([html.H3(['LOGIN'])])
    ]),
    dbc.Row([
        dbc.Col(html.Label('Username:')),
        dbc.Col(dcc.Input(id='username', type='text', value=''))
    ]),
    dbc.Row([
        dbc.Col(html.Label('Password:')),
        dbc.Col(dcc.Input(id='password', type='password', value=''))
    ]),
    dbc.Row([
        dbc.Col(html.Button('Login', id='login-button', n_clicks=0, className='my-button', style={'left':'19%', 'position':'relative', 'margin':'10px'}))
    ]),
    dbc.Row([
        dbc.Col(html.Div(id='login-output'))
    ]),
], fluid=True, style={'padding':'50px'})

# callback to verify user
@callback(
    Output('login-output', 'children'),
    [Input('login-button', 'n_clicks')],
    [dash.dependencies.State('username', 'value'),
     dash.dependencies.State('password', 'value')]
)
def authenticate_user(n_clicks, username, password):
    if n_clicks > 0:
        if check_credentials(username, password):
            return dbc.Row([
                dbc.Col(html.H3('Login successful'), width=12),
                dbc.Col(html.P(f'Welcome, {username}!'), width=12)
            ], className='row-titles')
        else:
            return dbc.Row([
                dbc.Col(html.H3('Login failed'), width=12),
                dbc.Col(html.P('Incorrect username or password.'), width=12)
            ], className='row-titles')
