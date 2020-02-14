from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'No1Knows!'  # this key needs to be updated later on!
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:password@localhost/psyapp"
    db.init_app(app)

    # blueprint for restricted routes
    from .authorized import authorized as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for open routes
    from .main_routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
