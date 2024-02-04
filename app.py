import os

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select

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

        new_birthday = birthday(name=name, month=month, day=day)
        db.session.add(new_birthday)
        db.session.commit()

        return redirect("/")

    else:
        birthdays = db.session.execute(select(birthday)).scalars()
        return render_template("index.html", birthdays=birthdays)