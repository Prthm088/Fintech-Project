from flask import request,render_template,Blueprint

main = Blueprint('main',__name__)

@main.route("/",methods=['GET'])
def index():
    return render_template('index.html')

@main.route("/stocks",methods=['GET'])
def stocks():
    return render_template('stock.html')

@main.route("/ipo",methods=['GET'])
def ipo():
    return render_template('ipo.html')

