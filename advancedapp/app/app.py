from flask import Flask

app = Flask(__name__)

# Pass the required route to the decorator. 
@app.route("/hello") 
def hello(): 
    return "Hello, Welcome to Geeks"
    
@app.route("/") 
def index(): 
    return "Homepage of GeeksFor"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
