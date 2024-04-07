import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import datetime
import psutil
from collections import deque

dash.register_page(__name__, name='2) Simple app', title='Simpleapp')

# Assuming that the 'assets' directory is at the same level as your script
from assets.fig_layout import my_figlayout, my_linelayout

# Vytvoření fronty pro ukládání dat o využití RAM
data_memory = deque(maxlen=50)
data_time = deque(maxlen=50)

layout = dbc.Container(
    [
            dbc.Row([
        dbc.Col([html.H3(['LIVE RAM USAGE'])], width=12, className='row-titles')
    ],
    className='row-content'
    ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Interval(
                        id='interval-component',
                        interval=1500,  #v milisekundách
                        n_intervals=0
                    )
                )
            ],
            className='row-content'
        ),

    dbc.Row([
        dbc.Col([], width = 2),
        dbc.Col([
            dcc.Loading(id='p1_1-loading', type='circle', children=dcc.Graph(id='live-update-graph', className='my-graph'))
        ], width = 8),
        dbc.Col([], width = 2)
    ], className='row-content')

    ]
)

# Callback pro aktualizaci grafu v reálném čase
@callback(Output('live-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    # Načtení dat o využití RAM
    x = datetime.datetime.now()
    y = psutil.virtual_memory().percent

    # Přidání nových dat do fronty
    data_memory.append(y)
    data_time.append(x)

    # Vytvoření grafu
    fig = go.Figure(layout=my_figlayout)
    fig.add_trace(go.Scatter(x=list(data_time), y=list(data_memory), mode='lines+markers'))

    fig.update_layout(xaxis_title='Time', yaxis_title='RAM Usage (%)', height = 500)
    fig.update_traces(overwrite=True, line=my_linelayout)

    return fig