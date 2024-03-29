# Data dashboards in Dash
**Obsah:**
 1. Setup
 2. Jednoduchá aplikace
 4. Prokročilá aplikace
## 1. Setup
Nainstaluj pomocí commandu globálně nebo do virtuálního prostředí.
Společně s dashem se ti nainstaluje i grafická knihovna plotly.
Dash aplikace pracují s flaskem, proto je tu command i pro flask.


    pip install dash, flask, pandas
    
## 1.1. Test aplikace
Z githubu stáhni [app.py](https://github.com/kutscheraa/DASH/blob/main/setup/app.py) ve složce setup a otestuj instalaci.

    python app.py
## 2. Jednoduchá aplikace
Teď si vytvoříme jednoduchou aplikace, která bude v reálném čase ukazovat využítí RAM.
Na aplikaci si vysvětlíme jak funguje dash layout a callback.
## 2.1. Inicializace a app layout
Naimportujeme si vše potřebné jako je psutil (system info - ram), datetime, dash, plotly.
Z modulu collections importujeme deque (obousměrná fronta) pro ukládání hodnot využití RAM, to nám zajistí plynulý pohyb grafu.

    import  dash
    from  dash  import  Output, Input, dcc, html
    import  psutil
    import  plotly.graph_objs  as  go
    import  datetime
    from  collections  import  deque
Teď si vytvoříme základní layout našeho dashboardu.

**html div** seskupuje různé části našeho dashboardu

**dcc.graph** je komponenta z knihovny dash_core_components

**interval** jak často se graf updatuje můžete zvolit jakýkoliv 

**n_intervals** volte 0 - jedná se o počáteční hodnotu grafu

    app.layout  =  html.Div([
    dcc.Graph(id="live-update-graph"),
    dcc.Interval(
    id='interval-component',
    interval=1000, # Interval v milisekundách
    n_intervals=0) ])

## 3. Pokročilá aplikace