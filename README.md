# Data dashboards in Dash
**Obsah:**
 1. Setup
 2. Jednoduchá aplikace
 4. Prokročilá aplikace
## 1. Setup
Naklonuj si repozitář a nainstaluj vše potřebné.
*Společně s dashem se ti nainstaluje i grafická knihovna plotly.
Dash aplikace pracují s flaskem, proto je tu command i pro flask.*


    
    git clone https://github.com/kutscheraa/DASH
    cd DASH
    python3 -m venv venv
    source venv/bin/activate
    pip install dash, flask, pandas
    
    
## 1.1. Test aplikace
Otestuj instalaci spuštěním test appky.

    python app.py
## 2. Jednoduchá aplikace
Teď si vytvoříme jednoduchou aplikaci, která bude v reálném čase ukazovat využítí RAM.
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

**Teď si vytvoříme základní layout našeho dashboardu.**

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