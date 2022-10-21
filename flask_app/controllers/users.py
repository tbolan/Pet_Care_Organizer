from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models import user
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/user/submit", methods = ["POST"])
def new_user():
    if not user.User.validate_user(request.form):
        return redirect("/")
    pw_hash = bcrypt.generate_password_hash(request.form["password"])
    data = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "password" : pw_hash
    }
    user.User.save(data)
    user_info = user.User.get_by_email(data)
    session["first_name"] = user_info.first_name
    session["last_name"] = user_info.last_name
    session["id"] = user_info.id
    return redirect("/jobs")


@app.route("/user/login", methods = ["POST"])
def login_post():
    data = {
        "email" : request.form["email"],
    }
    user_in_db = user.User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email or Password", "login")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
        flash("Invalid Email or Password", "login")
        return redirect("/")
    session["id"] = user_in_db.id
    session["first_name"] = user_in_db.first_name
    session["last_name"] = user_in_db.last_name
    return redirect("/jobs")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

