from datetime import timedelta

from flask import Flask, render_template, redirect, request, url_for, session
from flask_mysqldb import MySQL, MySQLdb

from form import about, home, auth

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15)

mysql = MySQL(app)


def create_connection(host, user, password, db):
    connection = False
    try:
        app.config['MYSQL_HOST'] = host
        app.config['MYSQL_USER'] = user
        app.config['MYSQL_PASSWORD'] = password
        app.config['MYSQL_DB'] = db
        app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
        print("Connection to MySQL DB successful")
        connection = True
        return connection

    except MySQLdb.OperationalError as e:
        print(f'MySQL server has gone away: {e}, trying to reconnect')
        raise e


connect_db = create_connection('localhost', 'root', '4863826M', 'hotel_db')

app.add_url_rule('/', view_func=home.index)

app.add_url_rule('/about', view_func=about.about)

# Auth forms
app.add_url_rule('/login', methods=['GET', 'POST'], view_func=auth.login)
app.add_url_rule('/logout', view_func=auth.logout)
app.add_url_rule('/register', methods=['GET', 'POST'], view_func=auth.register)


@app.route('/booking', methods=['GET', 'POST'])
def booking():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select * from roomtype, room where room.RoomType_idRoomType = roomtype.idRoomType and room.status = 'free'")
    room = cursor.fetchall()
    return render_template("booking.html", room=room)


@app.route('/payment/<idRoom>', methods=['GET', 'POST'])
def payment(idRoom):
    if not session.get("username"):
        return redirect("/login")
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
                cursor.execute(f'''INSERT INTO `guest` (`fname`, `lname`, `phone`, `email`, `checkIn`, `checkOut`) 
                VALUES ('{f}', '{l}', '{p}', '{e}', '{chkin}', '{chkout}')''')
                cursor.execute(f"SELECT idRoom FROM room WHERE idRoom={idRoom}")
                id = cursor.fetchone()
                cursor.execute(f'''UPDATE `room` SET status = 'busy' where idRoom='{id["idRoom"]}' ''')
                mysql.connection.commit()
            except:
                msg = 'Данные неверны'
    cursor.close()
    return render_template('payment.html', msg=msg, number=number)


@app.route('/admin')
def admin():
    if session['username'] != 'admin':
        return redirect('/')
    return render_template('admin.html')


@app.route('/reviews')
def reviews():
    return render_template("reviews.html")


@app.route('/help')
def help():
    return render_template("help.html")


if __name__ == "__main__":
    app.run(debug=True)
