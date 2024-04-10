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
python -m venv venv
```

Aktivace a instalace potřebných knihoven. Doporučujeme použít Command Prompt místo PowerShell, který občas vyhodí chybu při spouštění scriptu.

```python   
./venv/Scripts/activate
python -m pip install -r requirements.txt

python app.py
``` 

## 1.1. Test aplikace
Otestuj instalaci spuštěním test appky.

    cd setup
    python app1.py

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
```python
# app.py

from dash import Dash, dcc
import dash_bootstrap_components as dbc
import dash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# from db import *

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
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
## 2. Jednoduchá aplikace
Teď si vytvoříme jednoduchou aplikaci, která bude v reálném čase ukazovat využítí RAM.
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
