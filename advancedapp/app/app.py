from flask import Flask, render_template, request, flash
from dash import html, dcc
import dash
from dash.dependencies import Input, Output
from db import *


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', error = error), 404

@app.errorhandler(405)
def page_not_found(error):
    return render_template('error.html', error = error), 405

@app.route("/")
def index(): 
    return render_template('index.html', title="Home")

@app.route("/order", methods=['GET', 'POST']) 
def order():
    if request.method == 'POST':
        # Connect to the database
        Session = sessionmaker(bind=engine)
        session = Session()

        new_data = Data(region=request.form['region'], item_type=request.form['item_type'])
        session.add(new_data)

        # Commit the changes to the database
        session.commit()
        session.close()
        flash('Order created successfully.')

    return render_template('order.html', title="Order")
    

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    return 'To be implemented'

dash_app = dash.Dash(server=app, routes_pathname_prefix="/dash/")
# Create a session
Session = sessionmaker(bind=engine)
session = Session()
dash_app.layout = html.Div([
    html.H1("Data from MySQL Database"),
    html.Div([
        html.Label("Select Region:"),
        dcc.Dropdown(
            id='region-dropdown',
            options=[{'label': region[0], 'value': region[0]} for region in session.query(Data.region).distinct().all()],
            value=None
        ),
    ]),
    html.Div(id='output-data'),
])

# Define callback to update data based on region selection
@dash_app.callback(
    Output('output-data', 'children'),
    [Input('region-dropdown', 'value')]
)
def update_data(region):
    if region:
        try:
            data = session.query(Data).filter_by(region=region).all()
            if data:
                table_rows = [
                    html.Tr([html.Td(getattr(row, col)) for col in Data.__table__.columns.keys()])
                    for row in data
                ]
                return html.Table([
                    html.Thead(html.Tr([html.Th(col) for col in Data.__table__.columns.keys()])),
                    html.Tbody(table_rows)
                ])
            else:
                return html.P("No data available for selected region.")
        except SQLAlchemyError as e:
            return html.P(f"An error occurred: {str(e)}")
    else:
        return html.P("Select a region to view data.")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
