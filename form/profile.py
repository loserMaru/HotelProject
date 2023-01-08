import re

from flask import Flask, render_template, session, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

mysql = MySQL(app)


def profile(idAccount):
    if not session:
        return redirect('/register')
    print(session['username'])
    sesiya = session['username']
    cursor = mysql.connection.cursor()
    cursor.execute(f'''SELECT * FROM `account` where username = '{sesiya}' ''')
    name = cursor.fetchone()

    return render_template('profile.html', name=name)
