import re

from flask import Flask, render_template, session, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

mysql = MySQL(app)


def payment(idRoom):
    acc = ''
    if session:
        cursor = mysql.connection.cursor()
        sesiya = session["username"]
        cursor.execute(f"select * from account where username = '{sesiya}'")
        acc = cursor.fetchall()
    if not session.get("username"):
        return redirect("/login")
    if session['username'] == 'admin':
        return redirect('/booking')
    msg = ''
    cursor = mysql.connection.cursor()
    cursor.execute(f"select status from room where idRoom={idRoom}")
    status = cursor.fetchone()
    cursor.execute(f"SELECT roomNumber FROM room WHERE idRoom={idRoom}")
    number = cursor.fetchone()

    if status['status'] == 'busy':
        return redirect(url_for('booking'))

    if request.method == 'POST':
        f = request.form['name']
        l = request.form['lname']
        p = request.form['phone']
        e = request.form['email']
        chkin = request.form['checkIn']
        chkout = request.form['checkOut']
        if chkin > chkout:
            msg = 'Укажите дату верно'
        else:
            try:
                cursor.execute(f'''INSERT INTO `guest` (`fname`, `lname`, `phone`, `email`) 
                VALUES ('{f}', '{l}', '{p}', '{e}')''')
                cursor.execute(f"SELECT idRoom FROM room WHERE idRoom={idRoom}")
                id = cursor.fetchone()
                cursor.execute(f'''UPDATE `room` SET status = 'busy', checkIn = '{chkin}', checkOut='{chkout}' 
                                where idRoom='{id["idRoom"]}' ''')
                mysql.connection.commit()
            except(Exception,):
                msg = 'Данные неверны'
    cursor.close()
    return render_template('payment.html', msg=msg, number=number, acc=acc)
