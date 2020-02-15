from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import DevelopmentConfig

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config.from_object(DevelopmentConfig)

    from .models import db
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'authorized.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for restricted routes
    from .authorized import authorized as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for open routes
    from .main_routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
