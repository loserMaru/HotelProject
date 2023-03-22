from datetime import timedelta

from flask import Flask

from database.extension import mysql
from form import about, home, auth, admin, profile, payment, booking, help, reviews

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15)


def create_connection(host, user, password, db):
    connection = False
    app.config['MYSQL_HOST'] = host
    app.config['MYSQL_USER'] = user
    app.config['MYSQL_PASSWORD'] = password
    app.config['MYSQL_DB'] = db
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
    print("Connection to MySQL DB successful")
    connection = True
    return connection


connect_db = create_connection('localhost', 'root', '4863826M', 'hotel_db')

mysql.init_app(app)

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
app.add_url_rule('/profile/<idAccount>/edit', methods=['GET', 'POST'], view_func=profile.edit)

# Reviews
app.add_url_rule('/reviews', methods=['GET', 'POST'], view_func=reviews.reviews)

# Help
app.add_url_rule('/help', view_func=help.help)

if __name__ == "__main__":
    app.run(debug=True)
