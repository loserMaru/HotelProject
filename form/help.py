import re

from flask import Flask, render_template, session, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

mysql = MySQL(app)


def help():
    acc = ''
    if session:
        cursor = mysql.connection.cursor()
        sesiya = session["username"]
        cursor.execute(f"select * from account where username = '{sesiya}'")
        acc = cursor.fetchall()
    return render_template("help.html", acc=acc)
