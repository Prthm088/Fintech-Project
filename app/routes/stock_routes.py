from flask import request, redirect, url_for, render_template, Blueprint, session
from app.models import Subscription, Stock
from app import db
from app.services.subscription_manager import refresh_subscriptions
stock_bp = Blueprint("stock", __name__)


# ---------------------------
# STOCK SUBSCRIPTION
# ---------------------------
@stock_bp.route("/stock", methods=["GET", "POST"])
def stock():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    stocks = Stock.query.all()

    if request.method == "POST":

        selected_stocks = request.form.getlist("stocks")
        notification_method = request.form.get("notification_method")

        stock_names = []

        for stock_id in selected_stocks:

            stock = Stock.query.get(stock_id)

            if stock:
                stock_names.append(stock.symbol)

            existing = Subscription.query.filter_by(
                user_id=session["user_id"],
                stock_id=stock_id,
                alert_type="stock"
            ).first()

            if not existing:

                sub = Subscription(
                    user_id=session["user_id"],
                    stock_id=stock_id,
                    alert_type="stock",
                    notification_method=notification_method
                )

                db.session.add(sub)

        db.session.commit()
        refresh_subscriptions()

        stocks_display = ", ".join(stock_names)

        return redirect(
            url_for(
                "main.success",
                stocks=stocks_display,
                alert=notification_method
            )
        )

    return render_template("stock.html", stocks=stocks)