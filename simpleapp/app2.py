import dash
from dash import Output, Input, dcc, html
import psutil
import plotly.graph_objs as go
import datetime
from collections import deque

app = dash.Dash(__name__)

# Vytvoření fronty pro ukládání dat o využití RAM
data_memory = deque(maxlen=50)
data_time = deque(maxlen=50)

# Layout dashboardu
app.layout = html.Div([
    dcc.Graph(id="live-update-graph"),
    dcc.Interval(
        id='interval-component',
        interval=1000,  # Interval v milisekundách
        n_intervals=0
    )
])

# Callback pro aktualizaci grafu v reálném čase
@app.callback(Output('live-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    # Načtení dat o využití RAM
    x = datetime.datetime.now()
    y = psutil.virtual_memory().percent

    # Přidání nových dat do fronty
    data_memory.append(y)
    data_time.append(x)

    # Vytvoření grafu
    trace = go.Scatter(x=list(data_time), y=list(data_memory), mode='lines+markers')
    layout = go.Layout(title='Real-time RAM Usage', xaxis=dict(title='Time'), yaxis=dict(title='RAM Usage (%)'))
    return {'data': [trace], 'layout': layout}

# Spuštění aplikace
if __name__ == '__main__':
    app.run_server(debug=True)
