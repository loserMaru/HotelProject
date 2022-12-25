from flask import Flask, render_template, session, redirect

from flask_mysqldb import MySQL

app = Flask(__name__)

mysql = MySQL(app)


def admin():
    if session['username'] != 'admin':
        return redirect('/')
    return render_template('admin.html')
