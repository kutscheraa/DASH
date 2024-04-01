from flask import Flask, render_template, request

app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', error = error), 404

@app.errorhandler(405)
def page_not_found(error):
    return render_template('error.html', error = error), 405

@app.route("/")
@app.route("/index")
@app.route("/home")
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
