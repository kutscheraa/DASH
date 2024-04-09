import dash
from dash import html, Input, Output, callback, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import json
from sqlalchemy.orm import sessionmaker
from db import *

dash.register_page(__name__, path='/advancedapp', name='4) Advanced app', title='Advancedapp')

# Read data from CSV file
df = pd.read_csv('data/orders.csv')
df['created_at'] = pd.to_datetime(df['created_at'])

from assets.fig_layout import my_figlayout, my_linelayout, my_figlayout2

# Load geojson data
with open('data/kraje.json', 'r', encoding='utf-8') as f:
    geojson = json.load(f)

# Define the app layout
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Label("Select Region:"),
            dcc.Dropdown(
                id='region-dropdown',
                options=[{'label': region, 'value': region} for region in df['region'].unique()],
                value=None
            ),
        ])
    ], className='row-content'),

    dbc.Row([
        dbc.Col([], width=2),
        dbc.Col([
            dcc.Loading(
                id='p1_1-loading',
                type='circle',
                children=dcc.Graph(id='geojson-map', className='my-graph', config={'scrollZoom': False})
            )
        ], width=8),
        dbc.Col([], width=2)
    ], className='row-content'),

    dbc.Row([
        dbc.Col([], width=2),
        dbc.Col([
            dcc.Loading(
                id='p1_1-loading',
                type='circle',
                children=dcc.Graph(id='pie-percentage', className='my-graph')
            )
        ], width=8),
        dbc.Col([], width=2)
    ], className='row-content'),

    dbc.Row([
        dbc.Col([], width=2),
        dbc.Col([
            dcc.Loading(
                id='p1_1-loading',
                type='circle',
                children=dcc.Graph(id='pie-types', className='my-graph')
            )
        ], width=8),
        dbc.Col([], width=2)
    ], className='row-content'),

    dbc.Row([
        dbc.Col([], width=2),
        dbc.Col([
            dcc.Loading(
                id='p1_1-loading',
                type='circle',
                children=dcc.Graph(id='orders-per-day', className='my-graph')
            )
        ], width=8),
        dbc.Col([], width=2)
    ], className='row-content'),
])

# Define callback to update orders per day chart
@callback(
    Output('orders-per-day', 'figure'),
    [Input('region-dropdown', 'value')]
)
def update_orders_per_day(region):
    if region:
        data = df[df['region'] == region].groupby(df['created_at'].dt.date).size().reset_index(name='count')
    else:
        data = df.groupby(df['created_at'].dt.date).size().reset_index(name='count')

    fig = go.Figure(data=[go.Bar(x=data['created_at'], y=data['count'])], layout=my_figlayout)
    fig.update_layout(
        title='Orders per day',
        xaxis_title='Date',
        yaxis_title='Number of orders'
    )
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1d", step="day", stepmode="backward"),
                dict(count=7, label="1w", step="day", stepmode="backward"),
                dict(count=30, label="1m", step="day", stepmode="backward"),
                dict(count=365, label="1y", step="day", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    return fig

# Define callback to update pie percentage chart
@callback(
    Output("pie-percentage", "figure"),
    [Input('region-dropdown', 'value')]
)
def update_pie_percentage(region):
    if region:
        data = df[df['region'] == region].groupby('item_type').size().reset_index(name='count')
    else:
        data = df.groupby('item_type').size().reset_index(name='count')

    fig = px.pie(data, 
                values='count', 
                names='item_type', 
                hole=0.5,
                color_discrete_sequence=px.colors.sequential.RdBu
                )
    
    fig.layout = my_figlayout
    fig.update_traces(textinfo='percent+label')  # Zobrazuje percentá a popisky
    fig.update_layout(title='Orders by item type')  # Pridáva titulok pre lepšiu identifikáciu
    return fig

# Define callback to update pie types chart
@callback(
    Output("pie-types", "figure"),
    [Input('region-dropdown', 'value')]
)
def update_pie_types(region):
    if region:
        data = df[df['region'] == region].groupby('item_type')['price'].sum().reset_index()
    else:
        data = df.groupby('item_type')['price'].sum().reset_index()

    fig = px.pie(data, 
                values='price', 
                names='item_type', 
                hole=0.5, 
                color_discrete_sequence=px.colors.sequential.RdBu
                )
    
    fig.layout = my_figlayout
    fig.update_traces(textinfo='percent+label')  # Zobrazuje percentá a popisky
    fig.update_layout(title='Final sum per item-type (CZK)')  # Pridáva titulok pre lepšiu identifikáciu
    return fig


# Define callback to update the map
@callback(
    Output('geojson-map', 'figure'),
    [Input('region-dropdown', 'value')]
)
def update_map(region):
    if region:
        data = df[df['region'] == region].groupby('region').size().reset_index(name='count')
    else:
        data = df.groupby('region').size().reset_index(name='count')

    fig = px.choropleth_mapbox(data, 
                            geojson=geojson, 
                            locations='region', 
                            featureidkey="properties.name:cs", 
                            color='count',
                            labels={'count': 'orders'},
                            mapbox_style="carto-positron",
                            zoom=6.0, 
                            center={"lat": 49.7437522, "lon": 15.3386356},
                            )

    fig.update_layout(my_figlayout2)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig

# Define callback to update data based on region selection
@callback(
    Output('output-data', 'children'),
    [Input('region-dropdown', 'value')]
)
def update_data(region):
    if region:
        data = df[df['region'] == region]
        if data.empty:
            return html.P("No data available for selected region.")
        else:
            table_rows = [
                html.Tr([html.Td(getattr(row, col)) for col in df.columns.keys()])
                for row in data.to_dict('records')
            ]
            return html.Table([
                html.Thead(html.Tr([html.Th(col) for col in df.columns.keys()])),
                html.Tbody(table_rows)
            ])
    else:
        return html.P("Select a region to view data.")
