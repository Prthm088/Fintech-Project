from flask import render_template, Blueprint

main = Blueprint("main", __name__)


# Landing Page
@main.route("/")
def landingPage():
    return render_template("dashboard.html")


# Dashboard
@main.route("/index")
def index():
    return render_template("index.html")


# Success Page
@main.route("/success/<stocks>/<alert>")
def success(stocks, alert):
    return render_template(
        "success.html",
        stocks=stocks,
        alert=alert
    )