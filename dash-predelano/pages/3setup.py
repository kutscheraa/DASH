import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go

dash.register_page(__name__, path='/setup', name='1) Setup', title='Setupapp')

# Assuming that the 'assets' directory is at the same level as your script
from assets.fig_layout import my_figlayout, my_linelayout

# Load the data
data_csv = data = pd.read_csv('https://raw.githubusercontent.com/RDeconomist/observatory/main/Bitcoin%20Price.csv')

### PAGE LAYOUT ###############################################################################################################

layout = dbc.Container([
    # title
    dbc.Row([
        dbc.Col([html.H3(['BTC VALUE HISTORY'])], width=12, className='row-titles')
    ]),

    # data input
    dbc.Row([
        dbc.Col([], width = 3),
        dbc.Col([html.P(['Select a dataset:'], className='par')], width=2),
        dbc.Col([
            dcc.RadioItems(id='radio-dataset', options=['BTC'], value = 'BTC', persistence=True, persistence_type='session')
        ], width=4),
        dbc.Col([], width = 3)
    ], className='row-content'),

    # raw data fig
    dbc.Row([
        dbc.Col([], width = 2),
        dbc.Col([
            dcc.Loading(id='p1_1-loading', type='circle', children=dcc.Graph(id='fig-pg1', className='my-graph'))
        ], width = 8),
        dbc.Col([], width = 2)
    ], className='row-content')
    
])

### PAGE CALLBACKS ###############################################################################################################

# Update fig
@callback(
    Output(component_id='fig-pg1', component_property='figure'),
    Input(component_id='radio-dataset', component_property='BTC')
)
def plot_data(value):
    fig = None
    global data

    fig = go.Figure(layout=my_figlayout)
    fig.add_trace(go.Scatter(x=data['Date'], y=data['24h High (USD)'], line=dict()))

    fig.update_layout(xaxis_title='Date', yaxis_title='24h High (USD)', height = 500)
    fig.update_traces(overwrite=True, line=my_linelayout)

    return fig