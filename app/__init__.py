from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():

    app = Flask(__name__)

    app.config.from_object("app.app_config.Config")

    db.init_app(app)

    from app.routes import main, auth, stock_bp, ipo_bp

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(stock_bp)
    app.register_blueprint(ipo_bp)

    return app