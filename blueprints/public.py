from flask import Blueprint, flash, redirect, render_template, request, session
from werkzeug.security import generate_password_hash
from database import DatabaseHandler
from validation.isAuthed import isAuthed
from validation.containsSymbol import containsSymbol
from validation.containsNumber import containsNumber
from validation.isValidLength import isValidLength

public = Blueprint("public",__name__)
db = DatabaseHandler()

@public.before_request
def privateGate():
    if isAuthed() and request.path != "/home":
        return redirect("/home")

@public.route("/", methods = ["POST","GET"])
def signup():

    if request.method == "GET":

        return render_template("signup.html")

    formdata = request.form
    username = formdata.get("username")
    password = formdata.get("password")
    repassword = formdata.get("repassword")
    librarianPermissions = formdata.get("librarianPermissions") == "True"

    success = True
    if not isValidLength(username,4,16):
        success = False
        flash("Username must be between 4-16 characters")

    if containsSymbol(username) == True:
        success = False
        flash("Username cannot contain symbols/spaces")

    if containsSymbol(password) == True:
        success = False
        flash("Password cannot contain symbols/spaces")

    if not containsNumber(password) == True:
        success = False
        flash("Password must contain a number")

    if not isValidLength(password,8,35):
        success = False
        flash("Password must be between 8-35 characters")

    if password!= repassword:
        success = False
        flash("Passwords do not match")

    if not success:
        return redirect("/")
    
    hashedPassword = generate_password_hash(password)

    db_success, message = db.createUser(username,hashedPassword,librarianPermissions)

    if not db_success:
       flash(message)
       return redirect ("/")
    

    session["currentUser"] = username
    return redirect("/home")
