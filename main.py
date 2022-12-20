from flask import Flask, render_template, redirect, url_for
from flask import request
from flask_mysqldb import MySQL, MySQLdb

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
    msg = ''
    print(idRoom)
    cursor = mysql.connection.cursor()
    cursor.execute(f"select status from room where idRoom={idRoom}")
    status = cursor.fetchone()
    cursor.execute(f"SELECT roomNumber FROM room WHERE idRoom={idRoom}")
    number = cursor.fetchone()
    print(status['status'])

    if status['status'] == 'busy':
        return redirect(url_for('booking'))

    cursor = mysql.connection.cursor()
    if request.method == 'POST':
        f = request.form['name']
        l = request.form['lname']
        p = request.form['phone']
        e = request.form['email']
        chkin = request.form['checkin']
        chkout = request.form['checkout']
        if chkin > chkout:
            msg = 'Укажите дату верно'
        else:
            try:
                cursor.execute(f'''INSERT INTO `guest` (`fname`, `lname`, `phone`, `email`, `checkin`, `checkout`) 
                VALUES ('{f}', '{l}', '{p}', '{e}', '{chkin}', '{chkout}')''')
                cursor.execute(f"SELECT idRoom FROM room WHERE idRoom={idRoom}")
                id = cursor.fetchone()
                print(id)
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


@app.route('/login')
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        mysql.connection.cursor()
        cursor.execute(f"SELECT * FROM account WHERE username= $s and password= $s", (username, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            return 'Logged in successfuly'
        else:
            msg = 'Incorrect username/password'
    return render_template("login.html", msg=msg)


@app.route('/register')
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']

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
        else:
            cursor.execute('INSERT INTO accounts VALUES (%s, %s)', (username, password,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template("register.html", msg=msg)


if __name__ == "__main__":
    app.run(debug=True)
