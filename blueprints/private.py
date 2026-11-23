from flask import Blueprint, flash, redirect, render_template, request, session

from database import DatabaseHandler
from validation.isAuthed import isAuthed



private = Blueprint("private",__name__)
db = DatabaseHandler()

@private.before_request
def privateGate():
    if not isAuthed():
        return redirect("/")

@private.route("/home")
def home():
    return render_template("home.html")

@private.route("/signout")
def signout():

    session.clear()

    return redirect("/")