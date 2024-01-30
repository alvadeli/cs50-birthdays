import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///birthdays_test.db" 
db = SQLAlchemy(app)

class birthday(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    day = db.Column(db.Integer, nullable=False)

with app.app_context():    
    db.create_all()

# Configure CS50 Library to use SQLite database
#db = SQL("sqlite:///birthdays.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        # get name
        name = request.form.get("name")
        if not name:
            return redirect("/")

        # get month as valid int
        month = request.form.get("month")
        if not month:
            return redirect("/")
        try:
            month = int(month)
        except:
            return redirect("/")
        if month < 0 or month > 12:
            return redirect("/")

        # get day as valid int
        day = request.form.get("day")
        if not day:
            return redirect("/")
        try:
            day = int(day)
        except:
            return redirect("/")

        if day < 0 or day > 31:
            return redirect("/")

        #db.execute("INSERT INTO birthdays(name,month,day) VALUES(?, ?, ?)", name, month, day)
        new_birthday = birthday(name=name, month=month, day=day)
        db.session.add(new_birthday)
        db.session.commit()

        return redirect("/")

    else:

        # TODO: Display the entries in the database on index.html
        #birthdays = db.execute("SELECT * FROM birthdays")
        birthdays = db.session.execute(db.select(birthday))

        return render_template("index.html", birthdays=birthdays)