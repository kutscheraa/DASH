import dash
from dash import html, Input, Output, callback, dcc
import dash_bootstrap_components as dbc
import dash_auth    
from sqlalchemy.orm import sessionmaker
from db import *
from app import app

dash.register_page(__name__, path='/login', name='Login', title='Login')


# Konfigurace uživatelské autentizace s SQLAlchemy
def check_credentials(username, password):
    Session = sessionmaker(bind=engine)
    session = Session()
    user = session.query(User).filter_by(username=username, password=password).first()
    session.close()
    return user is not None

auth = dash_auth.BasicAuth(
    app,
    check_credentials
)

# Rozhraní aplikace
layout = html.Div([
    html.H1("Přihlášení"),
    html.Label('Uživatelské jméno:'),
    dcc.Input(id='username', type='text', value=''),
    html.Label('Heslo:'),
    dcc.Input(id='password', type='password', value=''),
    html.Button('Přihlásit', id='login-button', n_clicks=0),
    html.Div(id='login-output')
])

# Callback pro ověření přihlašovacích údajů
@callback(
    Output('login-output', 'children'),
    [Input('login-button', 'n_clicks')],
    [dash.dependencies.State('username', 'value'),
     dash.dependencies.State('password', 'value')]
)
def authenticate_user(n_clicks, username, password):
    if n_clicks > 0:
        if check_credentials(username, password):
            return html.Div([
                html.H3('Přihlášení úspěšné'),
                html.P(f'Vítejte, {username}!')
            ])
        else:
            return html.Div([
                html.H3('Přihlášení selhalo'),
                html.P('Nesprávné uživatelské jméno nebo heslo.')
            ])
