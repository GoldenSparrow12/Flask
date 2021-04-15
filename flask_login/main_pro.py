
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
            return render_template('profile.html')
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg)

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
        elif not username or not password:
            msg = 'Please fill out the form !'       
        else:
            if len(password) <8:
                msg = 'Password Must Greater than 8'
            elif re.search('[A-Z]',password) is None:
                msg = 'Capital Letter Missing in Password'
            elif re.search('[0-9]',password) is None:
                msg = 'Number Missing in Password'
            elif re.search('[!@#$%^&*()_]',password) is None:
                msg = 'Symbol Missing in Password'
            else:
                cursor.execute('INSERT INTO login_details (username,password) VALUES (%s,%s);', (username, password))
                mysql.connection.commit()
                msg = 'You have successfully registered !'

    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)

@app.route('/logout')
def logout():
    session.clear()
    return render_template('first.html')

@app.route('/')
def hello_world():
    return render_template('first.html')


if __name__ == '__main__':
    app.run(debug=True)
