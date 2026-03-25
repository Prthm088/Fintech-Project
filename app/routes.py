from flask import request, redirect, url_for, render_template, Blueprint, session
from werkzeug.security import generate_password_hash, check_password_hash

from .models import Subscription, Users, Stock
from . import db

main = Blueprint('main', __name__)


# Landing Page
@main.route("/")
def landingPage():
    return render_template('dashboard.html')


# ---------------------------
# SIGNUP
# ---------------------------
@main.route("/signup", methods=['GET', 'POST'])
def signup():

    if request.method == 'GET':
        return render_template("signup.html")

    first_name = request.form['firstName']
    last_name = request.form['lastName']
    email = request.form['email']
    password = request.form['password']

    hashed_password = generate_password_hash(password)

    new_user = Users(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=hashed_password
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.signup_success', first_name=first_name))


@main.route("/signup_success/<first_name>")
def signup_success(first_name):
    return render_template("signup_success.html", first_name=first_name)


# ---------------------------
# LOGIN
# ---------------------------
@main.route("/login", methods=['GET', 'POST'])
def login():

    if request.method == 'GET':
        return render_template("login.html")

    email = request.form['email']
    password = request.form['password']

    user = Users.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        session['user_id'] = user.id
        return redirect(url_for("main.index"))

    return redirect(url_for("auth.login"))


# ---------------------------
# DASHBOARD
# ---------------------------
@main.route("/index")
def index():
    return render_template('index.html')


# ---------------------------
# STOCK SUBSCRIPTION
# ---------------------------
@main.route("/stock", methods=["GET", "POST"])
def stock():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    stocks = Stock.query.all()

    if request.method == "POST":

        selected_stocks = request.form.getlist("stocks")
        notification_method = request.form.get("notification_method")

        stock_names = []

        for stock_id in selected_stocks:

            # Get stock object
            stock = Stock.query.get(stock_id)

            if stock:
                stock_names.append(stock.symbol)

            # Check existing subscription
            existing = Subscription.query.filter_by(
                user_id=session["user_id"],
                stock_id=stock_id,
                alert_type="stock"
            ).first()

            # Save subscription if not exists
            if not existing:
                sub = Subscription(
                    user_id=session["user_id"],
                    stock_id=stock_id,
                    alert_type="stock",
                    notification_method=notification_method
                )

                db.session.add(sub)

        db.session.commit()

        # Convert list   string for success page
        stocks_display = ", ".join(stock_names)

        return redirect(
            url_for(
                "main.success",
                stocks=stocks_display,
                alert=notification_method
            )
        )

    return render_template("stock.html", stocks=stocks)
# ---------------------------
# SUCCESS PAGE
# ---------------------------
@main.route("/success/<stocks>/<alert>")
def success(stocks, alert):
    return render_template(
        "success.html",
        stocks=stocks,
        alert=alert
    )

# ---------------------------
# IPO PAGE
# ---------------------------
@main.route("/ipo")
def ipo():
    return render_template('ipo.html')