from flask import Flask, render_template, request
from dash import html
import dash


app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', error = error), 404

@app.errorhandler(405)
def page_not_found(error):
    return render_template('error.html', error = error), 405

@app.route("/")
def index(): 
    return render_template('index.html', title="Home")

@app.route("/order") 
def order(): 
    return render_template('order.html', title="Order")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    return 'To be implemented'

dash_app = dash.Dash(server=app, routes_pathname_prefix="/dash/")
dash_app.layout = html.Div("This is the Dash app.")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
