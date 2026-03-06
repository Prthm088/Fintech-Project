from app import db

class Stock(db.Model):
    __tablename__ = "stocks"

    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    token = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"<Stock {self.symbol}>"