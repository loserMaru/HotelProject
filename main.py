from flask import Flask, render_template, redirect, request, url_for, session
from flask_session import Session
from flask_mysqldb import MySQL, MySQLdb
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

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


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


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


@app.route('/reviews')
def reviews():
    return render_template("reviews.html")


@app.route('/help')
def help():
    return render_template("help.html")


@app.route('/login', methods=['GET','POST'])
def login():
    log = ''
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute(f"SELECT * FROM account WHERE username='{username}' and password='{password}' ")
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['username'] = account['username']
            log = 'Logged in successfuly'
        else:
            msg = 'Incorrect username/password'
    return render_template("login.html", msg=msg, log=log)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(request.referrer)


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        passconfirm = request.form['confirm']

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM account WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        # elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        #     msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password:
            msg = 'Please fill out the form!'
        elif password != passconfirm:
            msg = "Passwords don't match"
        else:
            cursor.execute(f'''INSERT INTO `account` (`username`, `password`) VALUES ('{username}', '{password}') ''')
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template("register.html", msg=msg)


@app.route('/admin')
def admin():
    if session['username'] != 'admin':
        return redirect('/home')
    return render_template('admin.html')


if __name__ == "__main__":
    app.run(debug=True)
