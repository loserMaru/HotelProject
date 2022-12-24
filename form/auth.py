import re

from flask import Flask, render_template, session, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

mysql = MySQL(app)


def login():
    log = ''
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute(f"SELECT * FROM account WHERE username='{username}' and password='{password}' ")
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['username'] = account['username']
            session.permanent = True
            log = 'Logged in successfuly'
        else:
            msg = 'Incorrect username/password'
    return render_template("login.html", msg=msg, log=log)


def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        passconfirm = request.form['confirm']

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM account WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        # elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        #     msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password:
            msg = 'Please fill out the form!'
        elif password != passconfirm:
            msg = "Passwords don't match"
        else:
            cursor.execute(f'''INSERT INTO `account` (`username`, `password`) VALUES ('{username}', '{password}') ''')
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template("register.html", msg=msg)


def logout():
    session.clear()
    return redirect(request.referrer)
