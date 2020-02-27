from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from .config import DevelopmentConfig
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    app.config.from_object(DevelopmentConfig)

    from .models import db
    db.init_app(app)
    migrate.init_app(app, db)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User, Test
    from .authorize import MyModelView, MyAdminIndexView

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    admin = Admin(app, index_view=MyAdminIndexView())
    admin.add_view(MyModelView(Test, db.session))
    admin.add_view(MyModelView(User, db.session))

    with app.app_context():
        """blueprint for user authorization routes"""
        from .authorize import auth as auth_blueprint
        app.register_blueprint(auth_blueprint)

        """Blueprint for filling psychological tests"""
        from .test_routes import survey as test_blueprint
        app.register_blueprint(test_blueprint)

        """blueprint for open routes"""
        from .main_routes import main as main_blueprint
        app.register_blueprint(main_blueprint)

        db.create_all()

    return app

