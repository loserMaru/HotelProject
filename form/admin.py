from flask import Flask, render_template, session, redirect, request

from flask_mysqldb import MySQL

app = Flask(__name__)

mysql = MySQL(app)


def admin():
    if session:
        if session['username'] != 'admin':
            return redirect('/')
    else:
        return redirect('/')
    cursor = mysql.connection.cursor()
    msg = ''
    msgr = ''
    if request.method == 'POST' and 'number' in request.form:
        num = request.form['number']
        status = request.form['status']
        rtype = request.form['roomType']
        print(num, status, rtype)
        try:
            cursor.execute(f"SELECT * FROM room WHERE roomNumber={num}")
            x = cursor.fetchone()
            if x is None:
                cursor.execute(f'''INSERT INTO `room` (`roomNumber`, `status`, `RoomType_idRoomType`) 
                                VALUES ('{num}', '{status}', '{rtype}')''')
                mysql.connection.commit()
                msgr = 'Номер успешно создан'
            elif x['roomNumber'] == int(num):
                msg = 'Такой номер уже существует'
        except(Exception,):
            msg = 'Данные неверны'

    cursor.execute(f"SELECT * FROM guest")
    guest = cursor.fetchall()
    return render_template('admin.html', msg=msg, msgr=msgr, guest=guest)
