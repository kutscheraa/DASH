# dash_app.py
from app import app
from dash import html, dcc, dash_table
import dash
from dash.dependencies import Input, Output
from db import *

import json
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Read the GeoJSON file
with open('static/kraje.json', 'r', encoding='utf-8') as f:
    geojson = json.load(f)

dash_app = dash.Dash(server=app, routes_pathname_prefix="/dash/")

dash_app.layout = html.Div([
    html.H1("Data from MySQL Database"),
    html.Div([
        html.Label("Select Region:"),
        dcc.Dropdown(
            id='region-dropdown',
            options=[{'label': region[0], 'value': region[0]} for region in session.query(Data.region).distinct().all()],
            value=None
        ),
    ]),
    html.Div(id='output-data'),
    dcc.Graph(
        id='geojson-map',
        config={'scrollZoom': False},
        figure={},
    ),
])

session.commit()
session.close()

# Define callback to update the map
@dash_app.callback(
    Output('geojson-map', 'figure'),
    [Input('region-dropdown', 'value')]
)
def update_map(region_dropdown):
    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()
    # Query the database to get the count of items per region
    result = session.query(Data.region, func.count(Data.region)).group_by(Data.region).all()
    
    session.commit()
    session.close()
    
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
            data = session.query(Data).filter_by(region=region).all()
            if data:
                table_rows = [
                    html.Tr([html.Td(getattr(row, col)) for col in Data.__table__.columns.keys()])
                    for row in data
                ]
                return html.Table([
                    html.Thead(html.Tr([html.Th(col) for col in Data.__table__.columns.keys()])),
                    html.Tbody(table_rows)
                ])
            else:
                return html.P("No data available for selected region.")
        except SQLAlchemyError as e:
            return html.P(f"An error occurred: {str(e)}")
    else:
        return html.P("Select a region to view data.")
    