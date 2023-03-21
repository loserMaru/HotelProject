import re

from flask import Flask, render_template, session, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

mysql = MySQL(app)


def reviews():
    acc = ''
    if session:
        cursor = mysql.connection.cursor()
        sesiya = session["username"]
        cursor.execute(f"select * from account where username = '{sesiya}'")
        acc = cursor.fetchall()
    cursor = mysql.connection.cursor()
    cursor.execute(f'''SELECT * FROM reviews''')
    rev = cursor.fetchall()
    if request.method == 'POST':
        if session:
            user = session['username']
            cursor.execute(f'''SELECT * FROM `account` WHERE username = '{user}' ''')
            name = cursor.fetchone()
            description = request.form['desc']
            cursor.execute(f'''INSERT INTO `reviews` (`desc`, `username`) VALUES ('{description}', '{name['username']}') ''')
            mysql.connection.commit()
            return redirect("/reviews")
        else:
            return redirect("/register")
    return render_template("reviews.html", rev=rev, acc=acc)
