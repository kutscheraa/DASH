from app import app
from dash import html, dcc
import dash
from dash.dependencies import Input, Output
from db import *

import json
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

# Read the GeoJSON file
with open('static/kraje.json', 'r', encoding='utf-8') as f:
    geojson = json.load(f)
df = pd.read_csv('static/test.csv')

dash_app = dash.Dash(server=app, routes_pathname_prefix="/dash/")

# Create a session
Session = sessionmaker(bind=engine)
session = Session()
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

# Define callback to update the map
@dash_app.callback(
    Output('geojson-map', 'figure'),
    [Input('region-dropdown', 'value')]
)
def update_map(region_dropdown):
    fig = px.choropleth_mapbox(df, geojson=geojson, locations='name-cz', featureidkey="properties.name:cs", color='num',
                           color_continuous_scale="plasma",
                           range_color=(0, 12),
                           labels={'num': 'Náhodná proměnná'},
                           mapbox_style="carto-positron",
                           zoom=6.2, center={"lat": 49.7437522, "lon": 15.3386356},
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
    