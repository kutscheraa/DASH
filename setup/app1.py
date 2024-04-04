from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

# Načte data
df = pd.read_csv('https://raw.githubusercontent.com/RDeconomist/observatory/main/Bitcoin%20Price.csv')

# Inicializuje aplikaci
app = Dash(__name__)

# Definuje layout aplikace
fig = px.line(df, x='Date', y='24h High (USD)')
app.layout = html.Div([
    html.H1(children='BTC PRICE', style={'textAlign':'center'}),
    dcc.Graph(figure=fig)
])

if __name__ == '__main__':
    app.run(debug=True)
