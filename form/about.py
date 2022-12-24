from flask import render_template, session


def about():
    return render_template("about.html")
