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
@main.route("/success/<stocks>/<alert>/<int:user_id>")
def success(stocks, alert, user_id):
    return render_template(
        "success.html",
        stocks=stocks,
        alert=alert,
        user_id=user_id  
    )