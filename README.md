# Data dashboards in Dash
# Obsah

0. [Intro](#0-intro)
1. [Setup](#1-setup)
2. [Hello world!](#2-hello-world)
    1. [Komponenty](#21-komponenty)
    2. [Stránka](#22-stránky)
    3. [Vlastní styly](#23-vlastní-styly)
    4. [Callback](#24-callback)
3. [Druhá aplikace](#3-druhá-aplikace)
4. [Připojení databáze](#4-připojení-databáze)
5. [Tvorba objednávky](#5-tvorba-objednávky)
6. [Statistiky objednávek](#6-statistiky-objednávek)

## 0 Intro
Aby jsi se v projektu lépe vyznal, je lepší znát základní koncepty.
Každá naše aplikace má vyhrazenou svou page, na které je základem layout. Layout je tvořen z několika komponent, které se skládají dohromady.

Pro vysvětlení si vezmeme layout aplikace **1setup**
```python
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

V **layoutu** je definováno, že se jedná o **Container**, který obsahuje několik řádků **dbc.Row**. Každý řádek obsahuje několik sloupců **dbc.Col**. V tomto případě je layout rozdělen na 3 řádky. **První řádek** obsahuje nadpis **html.H3**, **druhý řádek** obsahuje vstupní data = výstup (zobrazujeme čísté csv a nijak ho needitujeme). Třetí dbc.Row obsahuje dcc.Loading, který je zde pro zobrazení loadingu, když se načítají data. **dcc.Loading** má definované id, type a children. **ID** je unikátní identifikátor, **type** je typ loadingu a **children** je komponenta, která se má zobrazit (**dcc.Graph**). Každý sloupec **dbc.Col** má definovanou šířku (width) a třídu (className). **ClassName** používáme pro dodatečné stylování (protože bootstrap...).

**Po layoutu vždy definujeme callback** a ten si teď vysvětlíme.
**Callback** je definovaná funkce v rámci aplikace, která se spouští interakcí uživatele. Uživatel například klikne na button a tím spustí python funkci.

Pro vysvětlení si vezmeme callback aplikace **1setup**
```python
@callback(
Output(component_id='fig-pg1', component_property='figure'),
Input(component_id='radio-dataset', component_property='BTC')
)
```
V outputu je definováno, že se jedná o **figure** a vstup je **radio-dataset**. Vstup je definován jako **BTC**, což je hodnota z **dcc.RadioItems**. Výstupem je **figure**, který je definován v layoutu.

**Po callbacku vždy následuje definování funkce, která se spustí při interakci uživatele.**
```python
def plot_data(value):
    fig = None
    global data

    fig = go.Figure(layout=my_figlayout)
    fig.add_trace(go.Scatter(x=data['Date'], y=data['24h High (USD)'], line=dict()))

    fig.update_layout(xaxis_title='Date', yaxis_title='24h High (USD)', height = 500)
    fig.update_traces(overwrite=True, line=my_linelayout)

    return fig
```
V této funkci je definováno několik věcí. **Global data** definují data, která se budou zobrazovat. 
**Data** samotná jsou z externího csv filu:
```python
data_csv  =  data  =  pd.read_csv('https://raw.githubusercontent.com/RDeconomist/observatory/main/Bitcoin%20Price.csv')
```
 V souboru jsou sloupce Currency, Date, Closing Price (USD), 24h Open (USD), 24h High (USD), 24h Low (USD).
 My z nich pracujeme pouze s **Date** a **24h High (USD)**, která extrahujeme takto:
```python
fig.add_trace(go.Scatter(x=data['Date'], y=data['24h High (USD)'], line=dict()))
```
Dále vytváříme prázdný graf **fig = go.Figure(layout=my_figlayout)**, který má definovaný layout. Přidáváme do grafu **trace** (data - už popsáno výše) a nakonfigurujeme layout. Nakonec vrátíme graf.
**V případě záseku je ideální použít [bootstrap docs](https://dash-bootstrap-components.opensource.faculty.ai/docs/components/), nebo [dash docs](https://dash.plotly.com/dash-core-components).**

## 1. Setup
Naklonuj si repozitář a nainstaluj vše potřebné.

První si naklonujeme repozitář, pak vytvoříme virtuální prostředí.

```bash   
git clone https://github.com/kutscheraa/DASH
cd DASH
py -m venv venv
```

Aktivace a instalace potřebných knihoven. Doporučujeme použít Command Prompt místo PowerShell, který občas vyhodí chybu při spouštění scriptu.

```bash
./venv/Scripts/activate
py -m pip install -r requirements.txt

python app.py
``` 

## 2. Hello world
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
## 2.1. Komponenty
Jak jsme již bylo zmíněno. Stránky jsou složeny z jednotlivých komponent, které ve finále tvoří stránku. My si teď dvě takové vytvoříme - header a footer.

Vytvoříme `📁assets` v kořenovém adresáři a `assets/nav.py`. Kde vytvoříme menu a hlavičku pro naší aplikaci. 

V hlavním containeru budou dva řádky, v tom prvním vytvoříme `dbc.Div` element s logem a v tom druhém bude samotná navigace `dbc.Nav`.
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
A v `📁assets` vytvoříme druhý soubor `footer.py`. Zde umístíme informace, které chceme, aby byli zobrazeny dole na stránce jako footer.
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
Naimportujeme námi vytvořené komponenty do `app.py` a přidáme do layoutu. Celý kód vypadá takto:
<details>
  <summary>KOMPLETNÍ KOD</summary>
  
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
], fluid=True)

############################################################################################
# Run App
if __name__ == '__main__':
	app.run_server(debug=True)

```
</details>
## 2.2. Stránky
Vytvoříme v kořenovém adresáři ještě jeden adresář `📁pages` a v něm soubor `1setup.py`.

Každou jednotlivou stránku je nutné zaregistrovat `dash.register_page`. A nastavit parametry: 
- *path* = cílový endpoint
- *name* = název
- *title* = titulek

Pomocí `pandas` načteme csv z URL a vytvoříme dataframe. Se kterým dále pracujeme. Pozor však na živá data. Pokud je definujeme před layoutem jsou načtena pouze jednou a to při startu aplikace. Jak udělat, aby byla načteny při každém refreshnutí stránky, si ukážeme později.
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
A v `app.py` přidáme parametr instanci dashe `use_pages=True`. 

Jako poslední krok vytvoříme v `📁assets` soubor `fig_layout.py`, který bude obsahovat defaultní stylování a layout pro naše grafy.
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

## 2.3. Vlastní styly
Dash podporuje přidávání vlastních CSS nebo JavaScript do vašich aplikací.
Do složky assets můžete vkládat soubory CSS a JavaScript. Dash automaticky obsluhuje všechny soubory, které jsou v této složce obsaženy. Ve výchozím nastavení je adresa URL  `📁assets`, ale můžete si ji přizpůsobit pomocí argumentu `assets_url_path` v instanci `dash.Dash`.


V `📁assets` tedy vytvoříme soubor `custom_style.css`
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
V `assets/1setup.py` první naimportujeme vytvořený `fig_layout` pomocí `from assets.fig_layout import my_figlayout, my_linelayout`.
## 2.4. Callback
Poslední částí co nám zbývá k správné funkčnosti aplikace je callback.

Funkce `plot_data` bere vstupní hodnotu value a vytváří graf na základě těchto dat. Používá globální proměnnou data, která je očekávána mít určitou strukturu s daty. V tomto kódu se předpokládá, že data obsahuje sloupce "Date" a "24h High (USD)", které jsou použity pro osy x a y grafu.

Graf je vytvořen pomocí objektu `go.Figure` z knihovny Plotly, kde se přidává stopa (trace) typu "scatter", která reprezentuje body na grafu. Následně se aktualizuje vzhled grafu pomocí různých nastavení, jako jsou titulky os, velikost a formát čar atd.

Nakonec je vytvořen grafický objekt `fig` a ten je vrácen jako výstup z funkce.
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
<details>
  <summary>Celý kód `pages/1setup.py`</summary>
  
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
</details>
## 3. Druhá aplikace
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

from assets.fig_layout import my_figlayout, my_linelayout
```
Vytvoření fronty pro ukládání dat o využití RAM
```python
data_memory = deque(maxlen=50)
data_time = deque(maxlen=50)
```
Vytvoříme kontejner s třemi řádky.
- První řádek obsahuje záhlaví "LIVE RAM USAGE".
- Druhý řádek obsahuje komponentu dcc.Interval, která vyvolává aktualizaci každých 1,5 sekundy.
- Třetí řádek obsahuje prázdné sloupce na začátku a na konci s šířkou 2, a mezi nimi sloupec s načítáním (Loading) a grafem (Graph), který se aktualizuje v reálném čase.
```python
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
Vytvoříme callback funkci, která bude spouštěna pomocí intervalového komponentu `interval-component`.

- Nejprve se načtou data o využití paměti RAM.
- Časová značka x se získá aktuálním časem, zatímco využití paměti y se získá pomocí knihovny psutil.
- Tyto nové hodnoty se přidají do fronty (`data_memory` a `data_time`), aby bylo možné sledovat historii dat.
- Poté se vytvoří nový graf pomocí knihovny Plotly. Do grafu se přidává nový bod s časovou značkou a využitím paměti.
- Následně se graf aktualizuje, nastavuje se jeho layout a layout pro čáry.
- Graf je nakonec vrácen a zobrazen v aplikaci.
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
## 4. Připojení databáze
Protože naše poslední aplikace bude využívat databázi tak si jí nadefinujeme. Jako první vytvoříme soubor v kořenovém adresáři `db.py`.
```python
# db.py

from sqlalchemy import create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

# Create the SQLAlchemy engine
engine = create_engine('mysql+mysqlconnector://doadmin:AVNS_IbKFOzKgR7dClGtqzJX@db-mysql-gui-do-user-14112159-0.c.db.ondigitalocean.com:25060/defaultdb')

# Create a base class for declarative class definitions
Base = declarative_base()

from models.order import Order

# Create tables in the database if they don't exist
Base.metadata.create_all(engine)
```
Dále si vytvoříme ve `📁models` soubor `order.py`, ve kterém si nadeklarujeme model objednávky.

Budeme potřebovat atributy:
- id
- region
- item_type
- price
- created_at
```python
# models/order.py

import dash
from dash import html
from db import Base
from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    region = Column(String(30))
    item_type = Column(String(30))
    price = Column(Integer)
    created_at = Column(DateTime, default=datetime.now)
```
## 5. Tvorba objednávky
Nyní vytvoříme formulář na přidávání záznamů do naší databáze.
```python
# pages/3order.py

import dash
from dash import html, Input, Output, callback, dcc
import dash_bootstrap_components as dbc
from sqlalchemy.orm import sessionmaker
from db import *

dash.register_page(__name__, path='/order', name='3) Order', title='Order')
```
Layout bude obsahovat několik řádků `dbc.Row` a sloupců `dbc.Col`, které organizují prvky formuláře.
A tři dropdowny:
- První dropdown nabízí výběr typu zboží (Electronics, Clothing, atd.).
- Druhý dropdown umožňuje vybrat region (např. Hlavní město Praha, Středočeský kraj, atd.).
- Třetí dropdown je určen pro cenu (100, 200, 300, 400, 500).

Po stisknutí tlačítka "Confirm" se spustí akce a výstup se zobrazí v `html.Div`.
```python
layout = dbc.Container([
    dbc.Row([
        dbc.Col([html.H3(['ORDER INSERT'])], width=12, className='row-titles')
    ]),
    dbc.Row([
        dbc.Col(dbc.Label('Item-type:'), width=2),
        dbc.Col(dcc.Dropdown(options = [
    "Electronics",
    "Clothing",
    "Books",
    "Home Appliances",
    "Toys",
    "Sports Equipment",
    "Jewelry",
    "Furniture",
    "Tools",
    "Food",
    "Other"
], id='item-type'), width=8),
    ]),
    dbc.Row([
        dbc.Col(dbc.Label('Region:'), width=2),
        dbc.Col(dcc.Dropdown(options = [
    "Hlavní město Praha",
    "Středočeský kraj",
    "Jihočeský kraj",
    "Plzeňský kraj",
    "Karlovarský kraj",
    "Ústecký kraj",
    "Liberecký kraj",
    "Královéhradecký kraj",
    "Pardubický kraj",
    "Kraj Vysočina",
    "Jihomoravský kraj",
    "Olomoucký kraj",
    "Zlínský kraj",
    "Moravskoslezský kraj"
], id='region'), width=8),
    ]),
    dbc.Row([
        dbc.Col(dbc.Label('Price:'), width=2),
        dbc.Col(dcc.Dropdown(options=["100","200","300","400","500"], id='price'), width=8),
    ]),
    dbc.Row([
        dbc.Col(html.Button('Confirm', id='submit-val', n_clicks=0, className='my-button'), width=3, style={'text-align':'left', 'margin':'5px 1px 1px 1px'}),
        dbc.Col(html.Div(id='output-state'), width=9),
    ]),
], className='')
```
Callback pro vkládání nových objednávek do databáze.

- Otevřeme session pro práci s databází.
- Vytvoříme novou objednávku s předanými hodnotami typu zboží, regionu a ceny.
- Přidáme novou objednávku do databáze pomocí `session.add(new_order)`.
- Potvrdí změny v databázi pomocí `session.commit()`.
- Uzavře session pomocí `session.close()`.
- A jako poslední vrátíme HTML element `html.Div`, který obsahuje informace o nově vložené objednávce.
```python
@callback(
    Output('output-state', 'children'),
    [Input('submit-val', 'n_clicks')],
    [dash.dependencies.State('item-type', 'value'),
     dash.dependencies.State('region', 'value'),
     dash.dependencies.State('price', 'value')]
)
def insert_order(n_clicks, item_type, region, price):
    if n_clicks > 0:
        Session = sessionmaker(bind=engine)
        session = Session()
        new_order = Order(item_type=item_type, region=region, price=price)
        session.add(new_order)
        session.commit()
        session.close()
        return html.Div([
            html.H3('New order inserted:'),
            html.P(f'Item-type: {item_type}'),
            html.P(f'Region: {region}'),
            html.P(f'Price: {price}')
        ])
```
## 6. Statistiky objednávek
```python
# pages/4advancedapp.py

import dash
from dash import html, Input, Output, callback, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import json
from sqlalchemy.orm import sessionmaker
from db import *

dash.register_page(__name__, path='/advancedapp', name='4) Advanced app', title='Advancedapp')

df = pd.DataFrame()

from assets.fig_layout import my_figlayout, my_linelayout, my_figlayout2

# Load geojson data
with open('data/kraje.json', 'r', encoding='utf-8') as f:
    geojson = json.load(f)

# Define the app layout
def set_layout():
    # Read data from DB
    Session = sessionmaker(bind=engine)
    session = Session()
    all_orders = session.query(Order).all()
    order_data = [{"id": order.id, "region": order.region, "item_type": order.item_type, "price": order.price, "created_at": order.created_at} for order in all_orders]
    global df
    df = pd.DataFrame(order_data)
    session.close()
    df['created_at'] = pd.to_datetime(df['created_at'])
    return dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Label("Select Region:"),
            dcc.Dropdown(
                id='region-dropdown',
                options=[{'label': region, 'value': region} for region in df['region'].dropna().unique()],
                value=None
            ),
        ])
    ], className='row-content'),

    dbc.Row([
        dbc.Col([], width=2),
        dbc.Col([
            dcc.Loading(
                id='p1_1-loading',
                type='circle',
                children=dcc.Graph(id='geojson-map', className='my-graph', config={'scrollZoom': False})
            )
        ], width=8),
        dbc.Col([], width=2)
    ], className='row-content'),

    dbc.Row([
        dbc.Col([], width=2),
        dbc.Col([
            dcc.Loading(
                id='p1_1-loading',
                type='circle',
                children=dcc.Graph(id='pie-percentage', className='my-graph')
            )
        ], width=8),
        dbc.Col([], width=2)
    ], className='row-content'),

    dbc.Row([
        dbc.Col([], width=2),
        dbc.Col([
            dcc.Loading(
                id='p1_1-loading',
                type='circle',
                children=dcc.Graph(id='pie-types', className='my-graph')
            )
        ], width=8),
        dbc.Col([], width=2)
    ], className='row-content'),

    dbc.Row([
        dbc.Col([], width=2),
        dbc.Col([
            dcc.Loading(
                id='p1_1-loading',
                type='circle',
                children=dcc.Graph(id='orders-per-day', className='my-graph')
            )
        ], width=8),
        dbc.Col([], width=2)
    ], className='row-content'),
])
layout = set_layout
# Define callback to update orders per day chart
@callback(
    Output('orders-per-day', 'figure'),
    [Input('region-dropdown', 'value')]
)
def update_orders_per_day(region):
    if region:
        data = df[df['region'] == region].groupby(df['created_at'].dt.date).size().reset_index(name='count')
    else:
        data = df.groupby(df['created_at'].dt.date).size().reset_index(name='count')

    fig = go.Figure(data=[go.Bar(x=data['created_at'], y=data['count'])], layout=my_figlayout)
    fig.update_layout(
        title='Orders per day',
        xaxis_title='Date',
        yaxis_title='Number of orders'
    )
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1d", step="day", stepmode="backward"),
                dict(count=7, label="1w", step="day", stepmode="backward"),
                dict(count=30, label="1m", step="day", stepmode="backward"),
                dict(count=365, label="1y", step="day", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    return fig

# Define callback to update pie percentage chart
@callback(
    Output("pie-percentage", "figure"),
    [Input('region-dropdown', 'value')]
)
def update_pie_percentage(region):
    if region:
        data = df[df['region'] == region].groupby('item_type').size().reset_index(name='count')
    else:
        data = df.groupby('item_type').size().reset_index(name='count')

    fig = px.pie(data, 
                values='count', 
                names='item_type', 
                hole=0.5,
                color_discrete_sequence=px.colors.sequential.RdBu
                )
    
    fig.layout = my_figlayout
    fig.update_traces(textinfo='percent+label')  # percentage + description
    fig.update_layout(title='Orders by item type')  # title
    return fig

# Define callback to update pie types chart
@callback(
    Output("pie-types", "figure"),
    [Input('region-dropdown', 'value')]
)
def update_pie_types(region):
    if region:
        data = df[df['region'] == region].groupby('item_type')['price'].sum().reset_index()
    else:
        data = df.groupby('item_type')['price'].sum().reset_index()

    fig = px.pie(data, 
                values='price', 
                names='item_type', 
                hole=0.5, 
                color_discrete_sequence=px.colors.sequential.RdBu
                )
    
    fig.layout = my_figlayout
    fig.update_traces(textinfo='percent+label')
    fig.update_layout(title='Final sum per item-type (CZK)')
    return fig


# Define callback to update the map
@callback(
    Output('geojson-map', 'figure'),
    [Input('region-dropdown', 'value')]
)
def update_map(region):
    if region:
        data = df[df['region'] == region].groupby('region').size().reset_index(name='count')
    else:
        data = df.groupby('region').size().reset_index(name='count')

    fig = px.choropleth_mapbox(data, 
                            geojson=geojson, 
                            locations='region', 
                            featureidkey="properties.name:cs", 
                            color='count',
                            labels={'count': 'orders'},
                            mapbox_style="carto-positron",
                            zoom=6.0, 
                            center={"lat": 49.7437522, "lon": 15.3386356},
                            )

    fig.update_layout(my_figlayout2)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig

# Define callback to update data based on region selection
@callback(
    Output('output-data', 'children'),
    [Input('region-dropdown', 'value')]
)
def update_data(region):
    if region:
        data = df[df['region'] == region]
        if data.empty:
            return html.P("No data available for selected region.")
        else:
            table_rows = [
                html.Tr([html.Td(getattr(row, col)) for col in df.columns.keys()])
                for row in data.to_dict('records')
            ]
            return html.Table([
                html.Thead(html.Tr([html.Th(col) for col in df.columns.keys()])),
                html.Tbody(table_rows)
            ])
    else:
        return html.P("Select a region to view data.")

```
