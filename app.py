from flask import *
from flask_mysqldb import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/home", methods=['GET','POST'])
def home():
    pass

@app.route("/login", methods=['POST', 'GET'])
def login():
    pass

@app.route("/register", methods=['POST','GET'])
def register():
    pass

if __name__ == "__main__":
    app.run(port=5000, debug=True, threaded=True)