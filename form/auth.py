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
            log = 'Вход выполнен успешно'
        else:
            msg = 'Неверное имя пользователя или пароль'
    return render_template("login.html", msg=msg, log=log)


def register():
    msg = ''
    msgr = ''
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
            msg = 'Аккаунт с таким логином уже существует!'
        # elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        #     msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Логин должен содержать только буквы и цифры!'
        elif not username or not password:
            msg = 'Пожалуйста, заполните это поле!'
        elif password != passconfirm:
            msg = "Пароли не совпадают"
        else:
            cursor.execute(f'''INSERT INTO `account` (`username`, `password`) VALUES ('{username}', '{password}') ''')
            mysql.connection.commit()
            msgr = 'Вы успешно зарегистрировались!'
    elif request.method == 'POST':
        msg = 'Пожалуйста, заполните это поле!'
    return render_template("register.html", msg=msg, msgr=msgr)


def logout():
    session.clear()
    return redirect(request.referrer)
