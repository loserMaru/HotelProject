import re

from flask import Flask, render_template, session, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

mysql = MySQL(app)


def help():
    return render_template("help.html")
