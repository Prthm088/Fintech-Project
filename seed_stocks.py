from app import create_app, db
from app.models import Stock

app = create_app()

with app.app_context():

    stocks = [
        {"symbol": "RELIANCE", "name": "Reliance Industries", "token": "2885"},
        {"symbol": "TCS", "name": "Tata Consultancy Services", "token": "11536"},
        {"symbol": "INFY", "name": "Infosys", "token": "1594"},
        {"symbol": "HDFCBANK", "name": "HDFC Bank", "token": "1333"},
        {"symbol": "ICICIBANK", "name": "ICICI Bank", "token": "4963"},
    ]

    for s in stocks:
        stock = Stock(**s)
        db.session.add(stock)

    db.session.commit()

    print("Stocks inserted successfully")