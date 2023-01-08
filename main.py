from datetime import timedelta

from flask import Flask, render_template, redirect, request, url_for, session
from flask_mysqldb import MySQL, MySQLdb

from form import about, home, auth, admin, profile, payment, booking, help, reviews

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

# Home
app.add_url_rule('/', methods=['GET', 'POST'], view_func=home.index)

# Auth forms
app.add_url_rule('/login', methods=['GET', 'POST'], view_func=auth.login)
app.add_url_rule('/logout', view_func=auth.logout)
app.add_url_rule('/register', methods=['GET', 'POST'], view_func=auth.register)

# Booking
app.add_url_rule('/booking', methods=['GET', 'POST'], view_func=booking.booking)

# Payment
app.add_url_rule('/payment/<idRoom>', methods=['GET', 'POST'], view_func=payment.payment)

# About
app.add_url_rule('/about', view_func=about.about)

# Admin panel
app.add_url_rule('/admin', methods=['GET', 'POST'], view_func=admin.admin)

# Profile
app.add_url_rule('/profile/<idAccount>', methods=['GET', 'POST'], view_func=profile.profile)

# Reviews
app.add_url_rule('/reviews', view_func=reviews.reviews)

# Help
app.add_url_rule('/help', view_func=help.help)

if __name__ == "__main__":
    app.run(debug=True)
