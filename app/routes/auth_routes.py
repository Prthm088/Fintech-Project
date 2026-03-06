from flask import request, redirect, url_for, render_template, Blueprint, session
from werkzeug.security import generate_password_hash, check_password_hash

from app.models import Users
from app import db

auth = Blueprint("auth", __name__)


# ---------------------------
# SIGNUP
# ---------------------------
@auth.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "GET":
        return render_template("signup.html")

    first_name = request.form["firstName"]
    last_name = request.form["lastName"]
    email = request.form["email"]
    password = request.form["password"]

    hashed_password = generate_password_hash(password)

    new_user = Users(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=hashed_password
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("auth.signup_success", first_name=first_name))


@auth.route("/signup_success/<first_name>")
def signup_success(first_name):
    return render_template("signup_success.html", first_name=first_name)


# ---------------------------
# LOGIN
# ---------------------------
@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        return render_template("login.html")

    email = request.form["email"]
    password = request.form["password"]

    user = Users.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        session["user_id"] = user.id
        return redirect(url_for("main.index"))

    return redirect(url_for("auth.login"))