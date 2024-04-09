import dash
from dash import html, Input, Output, callback, dcc
import dash_bootstrap_components as dbc
from sqlalchemy.orm import sessionmaker
from db import *

dash.register_page(__name__, path='/order', name='3) Order', title='Order')

# Rozhraní aplikace
layout = dbc.Container([
    dbc.Row([
        dbc.Col([html.H3(['ORDER INSERT'])], width=12, className='row-titles')
    ]),
    dbc.Row([
        dbc.Col(dbc.Label('Item-type:'), width=2),
        dbc.Col(dcc.Dropdown(options = [
    "Electronics",
    "Clothing",
    "Books",
    "Home Appliances",
    "Toys",
    "Sports Equipment",
    "Jewelry",
    "Furniture",
    "Tools",
    "Food",
    "Other"
], id='item-type'), width=8),
    ]),
    dbc.Row([
        dbc.Col(dbc.Label('Region:'), width=2),
        dbc.Col(dcc.Dropdown(options = [
    "Hlavní město Praha",
    "Středočeský kraj",
    "Jihočeský kraj",
    "Plzeňský kraj",
    "Karlovarský kraj",
    "Ústecký kraj",
    "Liberecký kraj",
    "Královéhradecký kraj",
    "Pardubický kraj",
    "Kraj Vysočina",
    "Jihomoravský kraj",
    "Olomoucký kraj",
    "Zlínský kraj",
    "Moravskoslezský kraj"
], id='region'), width=8),
    ]),
    dbc.Row([
        dbc.Col(dbc.Label('Price:'), width=2),
        dbc.Col(dcc.Dropdown(options=["100","200","300","400","500"], id='price'), width=8),
    ]),
    dbc.Row([
        dbc.Col(html.Button('Confirm', id='submit-val', n_clicks=0, className='my-button'), width=3, style={'text-align':'left', 'margin':'5px 1px 1px 1px'}),
        dbc.Col(html.Div(id='output-state'), width=9),
    ]),
], className='')

# Callback pro vkládání nových objednávek do databáze
@callback(
    Output('output-state', 'children'),
    [Input('submit-val', 'n_clicks')],
    [dash.dependencies.State('item-type', 'value'),
     dash.dependencies.State('region', 'value'),
     dash.dependencies.State('price', 'value')]
)
def insert_order(n_clicks, item_type, region, price):
    if n_clicks > 0:
        Session = sessionmaker(bind=engine)
        session = Session()
        new_order = Order(item_type=item_type, region=region, price=price)
        session.add(new_order)
        session.commit()
        session.close()
        return html.Div([
            html.H3('New order inserted:'),
            html.P(f'Item-type: {item_type}'),
            html.P(f'Region: {region}'),
            html.P(f'Price: {price}')
        ])
