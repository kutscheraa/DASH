# dash_app.py
import dash
from app import app
from dash import html, dcc
from dash.dependencies import Input, Output
from db import Session, engine, Order, func, SQLAlchemyError
from flask_login import login_required
import dash_bootstrap_components as dbc

import json
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

# Read the GeoJSON file
with open('static/kraje.json', 'r', encoding='utf-8') as f:
    geojson = json.load(f)

dash_app = dash.Dash(server=app, routes_pathname_prefix="/dash/")

def protect_dashviews(dash_app):
    for view_func in dash_app.server.view_functions:
        if view_func.startswith(dash_app.config['routes_pathname_prefix']):
            dash_app.server.view_functions[view_func] = login_required(
                dash_app.server.view_functions[view_func])

protect_dashviews(dash_app)
with Session(engine) as session:
    dash_app.layout = html.Div([
        html.H1("Data from MySQL Database"),
        html.Div([
            html.Label("Select Region:"),
            dcc.Dropdown(
                id='region-dropdown',
                options=[{'label': region[0], 'value': region[0]} for region in session.query(Order.region).distinct().all()],
                value=None
            ),
        ]),
        html.Div(id='output-data'),
        dcc.Graph(
            id='geojson-map',
            config={'scrollZoom': False},
        ),
        html.Div([
            dcc.Graph(
                id="pie-percentage"
            ),
            dcc.Graph(
                id="pie-types"
            ),
        ], style={'display': 'flex', 'flex-direction': 'row'}),
        dcc.Graph(id='orders-per-day')
    ])

@dash_app.callback(
    Output('orders-per-day', 'figure'),
    [Input('region-dropdown', 'value')]
)
def update_orders_per_day(region):
    with Session(engine) as session:
        if region:
            data = session.query(func.date(Order.created_at), func.count(Order.created_at)).filter_by(region=region).group_by(func.date(Order.created_at)).all()
        else:
            data = session.query(func.date(Order.created_at), func.count(Order.created_at)).group_by(func.date(Order.created_at)).all()

    df = pd.DataFrame(data, columns=['date', 'count'])

    fig = go.Figure(data=[go.Scatter(x=df['date'], y=df['count'])])
    fig.update_layout(
        title='Orders per day',
        xaxis_title='Date',
        yaxis_title='Number of orders'
    )
    return fig

@dash_app.callback(
    Output("pie-types", "figure"),
    [Input('region-dropdown', 'value')]
)
def update_pie_percentage(region_dropdown):
    with Session(engine) as session:
        # Query the database to get the count of items per region
        result = session.query(Order.item_type, func.count(Order.item_type)).group_by(Order.item_type).all()
    
    # Create a DataFrame from the query result
    df = pd.DataFrame(result, columns=['item_type', 'count'])

    fig = px.pie(df, 
                values='count', 
                names='item_type', 
                hole=0.5, 
                color_discrete_sequence=px.colors.sequential.RdBu
                )
    return fig


@dash_app.callback(
    Output("pie-percentage", "figure"),
    [Input('region-dropdown', 'value')]
)
def update_pie_percentage(region_dropdown):
    with Session(engine) as session:
        # Query the database to get the count of items per region
        result = session.query(Order.region, func.count(Order.region)).group_by(Order.region).all()
    
    # Create a DataFrame from the query result
    df = pd.DataFrame(result, columns=['region', 'count'])

    fig = px.pie(df, 
                values='count', 
                names='region', 
                hole=0.5, 
                color_discrete_sequence=px.colors.sequential.RdBu
                )
    return fig


# Define callback to update the map
@dash_app.callback(
    Output('geojson-map', 'figure'),
    [Input('region-dropdown', 'value')]
)
def update_map(region_dropdown):
    with Session(engine) as session:
        # Query the database to get the count of items per region
        result = session.query(Order.region, func.count(Order.region)).group_by(Order.region).all()
    
    # Create a DataFrame from the query result
    df = pd.DataFrame(result, columns=['region', 'count'])
    # Create a DataFrame with all possible regions
    all_regions = pd.DataFrame({
        'region': [
            'Hlavní město Praha', 'Středočeský kraj', 'Jihočeský kraj', 'Plzeňský kraj',
            'Karlovarský kraj', 'Ústecký kraj', 'Liberecký kraj', 'Královéhradecký kraj',
            'Pardubický kraj', 'Kraj Vysočina', 'Jihomoravský kraj', 'Olomoucký kraj',
            'Zlínský kraj', 'Moravskoslezský kraj'
        ]
    })
    # Merge with main DataFrame
    df = pd.merge(all_regions, df, on='region', how='left')
    # Fill NaN values with 0
    df['count'] = df['count'].fillna(0)
    fig = px.choropleth_mapbox(df, 
                            geojson=geojson, 
                            locations='region', 
                            featureidkey="properties.name:cs", 
                            color='count',
                            labels={'count': 'orders'},
                            mapbox_style="white-bg",
                            zoom=6.2, 
                            center={"lat": 49.7437522, "lon": 15.3386356},
                            )

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig

# Define callback to update data based on region selection
@dash_app.callback(
    Output('output-data', 'children'),
    [Input('region-dropdown', 'value')]
)
def update_data(region):
    if region:
        try:
            with Session(engine) as session:
                data = session.query(Order).filter_by(region=region).all()
            if data:
                table_rows = [
                    html.Tr([html.Td(getattr(row, col)) for col in Order.__table__.columns.keys()])
                    for row in data
                ]
                return html.Table([
                    html.Thead(html.Tr([html.Th(col) for col in Order.__table__.columns.keys()])),
                    html.Tbody(table_rows)
                ])
            else:
                return html.P("No data available for selected region.")
        except SQLAlchemyError as e:
            return html.P(f"An error occurred: {str(e)}")
    else:
        return html.P("Select a region to view data.")
