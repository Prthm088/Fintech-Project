from flask import request,redirect,url_for,render_template,Blueprint
from .models import Subscription
from . import db

main = Blueprint('main',__name__)

@main.route("/")
def index():
    return render_template('index.html')

@main.route("/stocks",methods=['GET','POST'])
def stocks():
    if request.method == 'GET':
        return render_template('stock.html')
    else:
        stocks = request.form.get('stocks')
        alert = request.form.get('alert_method')
        new_sub = Subscription(stock_name=stocks, alert_type=alert)
        db.session.add(new_sub)
        db.session.commit()

        return redirect(url_for('main.success',stocks=stocks,alert=alert))

@main.route("/success/<stocks>/<alert>",methods=['GET'])
def success(stocks,alert):
    return render_template('success.html',stocks=stocks,alert=alert)



@main.route("/ipo",methods=['GET'])
def ipo():
    return render_template('ipo.html')

