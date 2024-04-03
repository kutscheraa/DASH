from app import app
from dash import html, dcc
import dash
from dash.dependencies import Input, Output
from db import *

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
])

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