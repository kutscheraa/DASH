from flask import Flask, render_template, request, flash
from db import *
from seeders.data_seeder import seed

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

seed()

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

        new_data = Data(region=request.form['region'], item_type=request.form['item_type'], price=request.form['price'])
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




from dash_app import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
