
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re


app = Flask(__name__)
app.secret_key = 'secret key'
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'login'

mysql = MySQL(app)


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM login_details WHERE username = % s AND password = % s;', (username, password))
        result = cursor.fetchone()
        if result:
            session['loggedin'] = True
            session['username'] = result['username']
            msg = 'Login Succesfully'
            return render_template('profile.html',msg=msg)
        else:
            msg = 'Incorrect username/password !'
    return render_template('home.html', msg=msg)

@app.route('/register', methods = ['GET','POST'])
def register():
    msg=''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM login_details WHERE username = %s ;',(username,))
        result = cursor.fetchone()
        if result:
            msg = 'Account already exists !'       
        else:
            if len(password) <8:
                msg = 'Password Greater than 8'
            elif re.search('[A-Z]',password) is None:
                msg = 'Capital Letter Missing '
            elif re.search('[0-9]',password) is None:
                msg = 'Number Missing'
            elif re.search('[!@#$%^&*()_]',password) is None:
                msg = 'Symbol Missing'
            else:
                cursor.execute('INSERT INTO login_details (username,password) VALUES (%s,%s);', (username, password))
                mysql.connection.commit()
                msg = 'You have successfully registered !'
                return render_template('profile.html', msg = msg)
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)

@app.route('/logout')
def logout():
    session.clear()
    return render_template('home.html')

@app.route('/forgot', methods = ['GET','POST'])
def forgot():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM login_details WHERE username = %s ;',(username,))
        result = cursor.fetchone()
        if result:
            msg = result['password']
            return render_template('forgot.html',msg=msg)
        else:
            msg = 'Account not exists !' 
    return render_template('forgot.html',msg=msg)

@app.route('/')
def hello_world():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
