from flask import Flask, render_template, session, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

mysql = MySQL(app)


def profile(idAccount):
    if not session:
        return redirect('/login')
    acc = ''
    picture = ''
    if session:
        cursor = mysql.connection.cursor()
        sesiya = session["username"]
        cursor.execute(f"select * from account where username = '{sesiya}'")
        acc = cursor.fetchall()
        cursor.execute(f"select `img` from `account` where username = '{sesiya}'")
        picture = cursor.fetchone()
    sesiya = session['username']
    cursor = mysql.connection.cursor()
    cursor.execute(f'''SELECT * FROM `account` where username = '{sesiya}' ''')
    name = cursor.fetchone()

    return render_template('profile.html', name=name, acc=acc, picture=picture)


def edit(idAccount):
    msg = ""
    cursor = mysql.connection.cursor()
    if not session:
        return redirect('/login')
    acc = ''
    if session:
        cursor = mysql.connection.cursor()
        sesiya = session["username"]
        cursor.execute(f"select * from account where username = '{sesiya}'")
        acc = cursor.fetchall()
    if request.method == 'POST' and ('pic' in request.form) and (request.form['pic'] != '') \
            and not ('password' in request.form == '') or ('confirm' in request.form == ''):
        pic = request.form['pic']
        try:
            cursor.execute(f'''UPDATE `account` SET `img`='{pic}' where `idAccount`={idAccount} ''')
            mysql.connection.commit()
            return redirect('/profile/1')
        except(Exception,):
            msg = 'Error'
    elif request.method == 'POST' and ('password' in request.form) and (request.form['password'] != '') \
            and ('confirm' in request.form) and (request.form['confirm'] != '') and 'pic' in request.form == '':
        password = request.form['password']
        confirm = request.form['confirm']
        try:
            cursor.execute(f'''UPDATE `account` SET `password`='{password}' 
                where `idAccount`={idAccount} and `password` = '{confirm}' ''')
            mysql.connection.commit()
            return redirect('/profile/2')
        except(Exception,):
            msg = 'Error'
    elif request.method == 'POST' and ('pic' in request.form) and (request.form['pic'] != '') \
            and ('password' in request.form) and (request.form['password'] != '') and ('confirm' in request.form) \
            and (request.form['confirm'] != ''):
        pic = request.form['pic']
        password = request.form['password']
        confirm = request.form['confirm']
        try:
            cursor.execute(f'''UPDATE `account` SET `img`='{pic}' where `idAccount`={idAccount} ''')
            cursor.execute(f'''UPDATE `account` SET `password`='{password}' 
                where `idAccount`={idAccount} and `password` = '{confirm}' ''')
            mysql.connection.commit()
            return redirect('/profile/3')
        except(Exception,):
            msg = 'Error'
    elif request.method == 'POST' and 'password' in request.form:
        msg = 'Заполните нужные поля'
    return render_template('edit.html', acc=acc, msg=msg)
