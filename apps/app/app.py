from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required
from db import *
import seeders.order_seeder as order_seeder
import seeders.user_seeder as user_seeder

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Seeding db
order_seeder.seed()
user_seeder.seed()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def user_loader(user_id):
    with Session(engine) as session:
        user = session.query(User).filter_by(id=int(user_id)).first()
    return user

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
        with Session(engine) as session:
            new_data = Order(region=request.form['region'], item_type=request.form['item_type'], price=request.form['price'])
            session.add(new_data)
            session.commit()
        flash('Order created successfully.')

    return render_template('order.html', title="Order")
    
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with Session(engine) as session:
            user = session.query(User).filter_by(username=username).first()

        next = request.args.get('next')

        if user and user.password == password:
            login_user(user)
            session.close()
            flash('Přihlášen.')
            return redirect(next or url_for('index'))
        else:
            flash('Neúspěch.')
            session.close()

    return redirect(url_for('login'))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Odhlášen.')
    return redirect(url_for('index'))

from dash_app import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
