import re

from flask import Flask, render_template, session, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

mysql = MySQL(app)


def booking():
    acc = ''
    if session:
        cursor = mysql.connection.cursor()
        sesiya = session["username"]
        cursor.execute(f"select * from account where username = '{sesiya}'")
        acc = cursor.fetchall()
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select * from roomtype, room where room.RoomType_idRoomType = roomtype.idRoomType and room.status = 'free'")
    room = cursor.fetchall()
    return render_template("booking.html", room=room, acc=acc)
