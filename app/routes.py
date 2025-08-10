from flask import request,redirect,url_for,render_template,Blueprint,session
from .models import Subscription,Users
from . import db
from werkzeug.security import generate_password_hash

main = Blueprint('main',__name__)

@main.route("/signup",methods=['GET','POST'])
def signup():
    if request.method=='GET':
        return render_template("sign_up.html")
    else:
        first_name = str(request.form['firstName'])
        last_name = str(request.form['lastName'])
        email = str(request.form['email'])
        password = str(request.form['password'])
        hashed_password = generate_password_hash(password)

        new_user = Users(first_name=first_name,
                         last_name=last_name,
                         email=email,
                         password=hashed_password)
        
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('main.signup_success',first_name=first_name))
    
@main.route("/signup_success/<first_name>")
def signup_success(first_name):
    return render_template("signup_success.html",first_name=first_name)


@main.route("/index.html",methods=['GET'])
def index():
    if request.method == 'GET':
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

