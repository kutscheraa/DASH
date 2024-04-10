# Data dashboards in Dash
**Obsah:**
 1. Setup
 2. Jednoduchá aplikace
 4. Prokročilá aplikace
## 1. Setup
Naklonuj si repozitář a nainstaluj vše potřebné.

*Společně s dashem se ti nainstaluje i grafická knihovna **plotly**.
Dash aplikace pracují s **flaskem**, proto je tu command i pro flask.*

První si naklonujeme repozitář, pak vytvoříme virtuální prostředí.

```python    
git clone https://github.com/kutscheraa/DASH
cd DASH
py -m venv venv
```

Aktivace a instalace potřebných knihoven. Doporučujeme použít Command Prompt místo PowerShell, který občas vyhodí chybu při spouštění scriptu.

```python   
./venv/Scripts/activate
py -m pip install -r requirements.txt

python app.py
``` 

## 1.1. Test aplikace
Otestuj instalaci spuštěním `app.py`.

```python
# app.py

from dash import Dash, dcc
import dash_bootstrap_components as dbc
import dash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Dash(__name__, 
        external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
	    suppress_callback_exceptions=True, prevent_initial_callbacks=True)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

server = app.server

app.layout = dbc.Container([
	"Hello world!"
], fluid=True)

if __name__ == '__main__':
	app.run_server(debug=True)
```
Dále vytvoříme `📁assets` v kořenovém adresáři a `assets/nav.py`. Kde vytvoříme menu a hlavičku pro naší aplikaci.
```python
# assets/nav.py

from dash import html
import dash_bootstrap_components as dbc
import dash

_nav = dbc.Container([
	dbc.Row([
        dbc.Col([
            html.Div([
                html.I(className="fa-solid fa-chart-simple fa-2x")],
		    className='logo')
        ], width = 4),
        dbc.Col([html.H1(['JELÍNEK KUČERA'], className='app-header')], width = 8)
	]),
	dbc.Row([
        dbc.Nav(
	        [dbc.NavLink(page["name"], active='exact', href=page["path"]) for page in dash.page_registry.values()],
	        vertical=True, pills=True, class_name='my-nav')
    ])
])
```
V `📁assets` vytvoříme soubor `footer.py`. Zde umístíme informace, které chceme aby byli zobrazeny dole na stránce jako footer.
```python
# assets/footer.py

from dash import html
import dash_bootstrap_components as dbc

_footer = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col([html.Hr([], className = 'hr-footer')], width = 12)
        ]),
        dbc.Row([
	        dbc.Col([], width = 1),
            dbc.Col(['Created with Plotly Dash'], width = 3),
            dbc.Col([], width =6),
	        dbc.Col([
                html.Ul([
                    html.Li([
                        html.A([ html.I(className="fa-brands fa-github me-3 fa-1x")], href='https://github.com/kutscheraa/DASH'),
                    ])
                ], className='list-unstyled d-flex justify-content-center justify-content-md-start')
            ], width = 2)
        ])
    ], fluid=True)
], className = 'footer')
```
Naimportujeme námi vytvořené komponenty do `app.py` a přidáme do layoutu.
```python
# app.py

from dash import Dash, dcc
import dash_bootstrap_components as dbc
import dash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# from db import *

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
	   suppress_callback_exceptions=True, prevent_initial_callbacks=True)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
server = app.server

############################################################################################
# Import shared components

from assets.footer import _footer
from assets.nav import _nav

############################################################################################
# App Layout
app.layout = dbc.Container([
	dbc.Row([
        dbc.Col([_nav], width = 2),
        dbc.Col([
            dbc.Row([dash.page_container])
	    ], width = 10),
    ]),
    dbc.Row([
        dbc.Col([], width = 2),
        dbc.Col([
            dbc.Row([_footer])
	    ], width = 10),
    ]),
    dcc.Store(id='browser-memo', data=dict(), storage_type='session')
], fluid=True)

############################################################################################
# Run App
if __name__ == '__main__':
	app.run_server(debug=True)

```
Vytvoříme v kořenovém adresáři ještě jeden adresář `📁pages` a v něm soubor `1setup.py`
```python
# pages/1setup.py

import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go

dash.register_page(__name__, path='/', name='1) Setup', title='Setupapp')

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
```
A v `app.py` přidáme parametr `use_pages=True`. Dále vytvoříme v `📁assets` další soubor `fig_layout.py`
```python
# assets/fig_layout.py

import plotly.graph_objects as go

###### FIG LAYOUT
font_style = {
    'color' : '#f6f6f6'
}

margin_style = {
    'b': 10,
    'l': 50,
    'r': 8,
    't': 50,
    'pad': 0
}

xaxis_style = {
    'linewidth' : 1,
    'linecolor' : 'rgba(0, 0, 0, 0.35%)',
    'showgrid' : False,
    'zeroline' : False
}

yaxis_style = {
    'linewidth' : 1,
    'linecolor' : 'rgba(0, 0, 0, 0.35%)',
    'showgrid' : True,
    'gridwidth' : 1,
    'gridcolor' : 'rgba(0, 0, 0, 0.11%)',
    'zeroline' : False
}

###### FIG LAYOUT (for all components)
my_figlayout = go.Layout(
    paper_bgcolor='rgba(0,0,0,0)', # Figure background is controlled by css on dcc.Graph() components
    plot_bgcolor='rgba(0,0,0,0)',
    font = font_style,
    margin = margin_style,
    xaxis = xaxis_style,
    yaxis = yaxis_style,
    height = 300
)

###### FIG LAYOUT 2 (for map)
my_figlayout2 = go.Layout(
    paper_bgcolor='rgba(0,0,0,0)', # Figure background is controlled by css on dcc.Graph() components
    plot_bgcolor='rgba(0,0,0,0)',
    font = font_style,
    margin = margin_style,
    xaxis = xaxis_style,
    yaxis = yaxis_style,
    height = 400
)


###### TRACES LAYOUT (for line plots)
my_linelayout = {
    'width' : 3,
    'color' : '#3DED97'
}
```

## 2. Vlastní styly
V `📁assets` vytvoříme soubor `custom_style.css`
```css
/* === ANY ELEMENT OVERRIDE ===*/
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    color: #f6f6f6 !important;
}

/* === BASE ===*/
html,
body {
    height: 100vh;
    background-image: linear-gradient(109.6deg, rgb(0, 0, 0) 11.2%, rgb(11, 132, 145) 91.1%);
    overflow-x: hidden;
    font-size: 18px;
}

/* === dcc.Graphh components ===*/
.dash-graph.my-graph {
    background-color: rgba(0,0,0,11.0%);
    border-radius: 25px;
}

/* === NAV ===*/
.logo {
    padding: 23px 1px 1px 1px;
    text-align: center;
    vertical-align: middle;
    text-shadow: 0px 0px 50px #4be9fa;
}

.app-brand {
    font-size: 35px;
    font-weight: 200;
    text-shadow: 0px 0px 50px #4be9fa;
}

.my-nav {
    font-size: 18px !important;
}

.nav-pills .nav-link.active {
    background-color: #042f33;
}

/* === FOOTER ===*/
.hr-footer {
    height: 5px;
}

.footer {
    font-size: 15px;
}


.guide {
    text-align: left;
    font-size: 16px;
    font-weight: 100; 
}

.row-content {
    margin: 20px 0px 20px 0px;
    justify-content: space-between;
}

.par {
    text-align: center;
}

input[type='radio'] {
    accent-color: #042f33;
    margin: 5px 5px 5px 5px;
}

input:hover {
    box-shadow: 0 0 10px #3DED97;
}

input[type='text'] {
    size: 50px;
    border-radius: 25px;
    border: solid 1px #3DED97;
    accent-color: #042f33;
    background-color: #042f33;
    padding: 12px 20px;
    margin: 5px 0;
    position: relative;
    left: -75%;
}

input[type='password'] {
    border-radius: 25px;
    border: solid 1px #3DED97;
    accent-color: #042f33;
    background-color: #042f33;
    padding: 12px 20px;
    margin: 5px 0;
    position: relative;
    left: -75%;
}

.row-titles {
    padding: 10px 0px 20px 0px;
    text-align: center;
    text-decoration: solid;
}

.dash-dropdown {
    margin: 5px 0px 5px 0px;
}
/* === BUTTON ===*/
.my-button {
    background-color: #042f33;
    border: solid 1px #3DED97;
    border-radius: 25px;
    padding: 10px 20px 10px 20px;
    font-size: 18px;
    margin: 0px;
    box-shadow: 0 0 5px #042f33;
}

.my-button:hover {
    box-shadow: 0 0 10px #3DED97;
}

.my-button:active {
    box-shadow: 0 0 10px #3DED97;
  }

/* === MAP DROPDOWN ===*/
.Select-control, .Select-menu-outer {
    background-color: #042f33 !important;
    border-width: 1px;
    border-color: #042f33 !important;
  }

/* === LOADING ===*/
.dash-sk-circle .dash-sk-child:before {
    background-color: #3DED97 !important;
    box-shadow: 0 0 20px #3DED97 !important;
}

```
## 3. Callback
V `assets/1setup.py` naimportujeme vytvořený `fig_layout` pomocí `from assets.fig_layout import my_figlayout, my_linelayout`.
```python
# v pages/1setup.py

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
```
Celý kód `pages/1setup.py`
```python
# pages/1setup.py

import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go

dash.register_page(__name__, path='/', name='1) Setup', title='Setupapp')

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
```
Teď si vytvoříme jednoduchou aplikaci, která bude v reálném čase ukazovat využítí RAM. V `📁pages` vytvoříme další soubor `2simpleapp.py`
```python
# pages/2simpleapp.py

import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import datetime
import psutil
from collections import deque

dash.register_page(__name__, path='/simpleapp', name='2) Simple app', title='Simpleapp')

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
```
```python
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
```
Na aplikaci si vysvětlíme jak funguje dash **layout** a **callback**.
## 2.1. Inicializace a app layout
Naimportujeme si vše potřebné jako je psutil (system info - ram), datetime, dash, plotly.
Z modulu collections importujeme deque (obousměrná fronta) pro ukládání hodnot využití RAM, to nám zajistí plynulý pohyb grafu.

    import  dash
    from  dash  import  Output, Input, dcc, html
    import  psutil
    import  plotly.graph_objs  as  go
    import  datetime
    from  collections  import  deque

**Vytvoříme základní layout našeho dashboardu.**

 - **html div** seskupuje různé části našeho dashboardu
 - **dcc.graph** je komponenta z knihovny dash_core_components
 - **interval** jak často se graf updatuje můžete zvolit jakýkoliv
 - **n_intervals** volte 0 - jedná se o počáteční hodnotu grafu

       
       app.layout = html.Div([
       dcc.Graph(id="live-update-graph"),
       dcc.Interval(
       id='interval-component',
       interval=1000, # Interval v milisekundách
       n_intervals=0)])

## 2.2. Callback a graf

    data_memory = deque(maxlen=50)
    data_time = deque(maxlen=50)
    
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
dodělat
## 3. Pokročilá aplikace
