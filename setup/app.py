from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

# Načte data
df = pd.read_csv('https://raw.githubusercontent.com/RDeconomist/observatory/main/Bitcoin%20Price.csv')

# Inicializuje aplikaci
app = Dash(__name__)

# Definuje layout aplikace
app.layout = html.Div([
    html.H1(children='BTC', style={'textAlign':'center'}),
    dcc.Graph(id='graph-content')
])

# Definuje callback pro aktualizaci grafu
@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    dff = df[df.Currency==value]
    return px.line(dff, x='Date', y='24h High (USD)')

if __name__ == '__main__':
    app.run(debug=True)