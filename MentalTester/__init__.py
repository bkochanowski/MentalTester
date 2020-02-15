from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'No1Knows!'  # this key needs to be updated later on!
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:kochan88@localhost/psyapp"
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'authorize.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # user_id is the primary key of that table, so I need to use it in the query for the user
        return User.query.get(int(user_id))

    """blueprint for restricted routes"""
    from .authorized import authorized as auth_blueprint
    app.register_blueprint(auth_blueprint)

    """blueprint for open routes"""
    from .main_routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
