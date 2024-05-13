from flask import *
from flask_mysqldb import *

app = Flask(__name__)
app.secret_key = "Shit"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'nookncorner'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/home", methods=['GET','POST'])
def home():
    return render_template("home.html")

@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == "POST" and "username" in request.form and "password" in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQL.cursor.DictCursor)
        cursor.execute(f"select * from account where username = '{username}' and password = '{password}'")
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['username'] = account['username']
            session['storename'] = account['storename']
            return redirect(url_for('account'))
        else:
            return render_template('login.html')
    return render_template("login.html")

@app.route("/register", methods=['POST','GET'])
def register():
    if request.method == "POST" and "username" in request.form and "password" in request.form and "phonenum" in request.form and "storename" in request.form and "storetype" in request.form:
        username = request.form['username']
        password = request.form['password']
        phonenum = request.form['phonenum']
        storename = request.form['storename']
        storetype = request.form.get('storetype')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(f"insert into account values('{username}', '{password}', {phonenum}, '{storename}', '{storetype}')")
        cursor.connection.commit()
        return redirect(url_for('account'))
    return render_template("register.html")

@app.route("/account",methods=['POST','GET'])
def account():
    if session['loggedin']:
        if request.method == "POST" and "discountname" in request.form and "validity" in request.form and "amount" in request.form and "itemtype" in request.form:
            discountname = request.form['discountname']
            validity = request.form['validity']
            amount = request.form['amount']
            itemtype = request.form.get('itemtype')
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(f"insert into discount values('{session['storename']}', {validity}, {amount}, '{discountname}', '{itemtype}')")
            cursor.connection.commit()
            return redirect(url_for('account'))
        mcursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        mcursor.execute(f"select * from discount where storename = '{session['storename']}'")
        available = mcursor.fetchall()
        return render_template("account.html", available=available)
    return render_template("login.html")

@app.route("/deleteDiscount/<int:id>", methods=['POST', 'GET'])
def deleteDiscount(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    try:
        cursor.execute(f"delete from discount where id = {id}")
        cursor.connection.commit()
        return redirect(url_for("account"))
    except Exception:
        return Exception, redirect(url_for("home"))

@app.route("/grocery")
def grocery():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select * from account where storetype = 'grocery'")
    store = cursor.fetchall()
    return render_template("grocery.html", store=store)

@app.route("/accessory")
def accessory():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select * from account where storetype = 'accessory'")
    store = cursor.fetchall()
    return render_template("accessory.html", store=store)

@app.route("/clothing")
def clothing():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select * from account where storetype = 'clothing'")
    store = cursor.fetchall()
    return render_template("clothing.html", store=store)

if __name__ == "__main__":
    app.run(port=5000, debug=True, threaded=True)