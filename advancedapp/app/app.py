from flask import Flask, render_template

app = Flask(__name__)
    
@app.route("/")
@app.route("/index")
@app.route("/home")
def index(): 
    return render_template('index.html', title="Home")

@app.route("/order") 
def order(): 
    return render_template('order.html', title="Order")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
