from flask import Blueprint, render_template

ipo_bp = Blueprint("ipo", __name__)


@ipo_bp.route("/ipo")
def ipo():
    return render_template("ipo.html")