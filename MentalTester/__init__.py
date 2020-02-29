from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from .config import DevelopmentConfig


db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)

    app.config.from_object(DevelopmentConfig)
    csrf.init_app(app)

    from .models import db
    db.init_app(app)
    migrate.init_app(app, db)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User, Test, TestFactor, AnswerChoice, Question, Answer
    from .authorize import MyModelView, MyAdminIndexView

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    admin = Admin(app, index_view=MyAdminIndexView())
    admin.add_view(MyModelView(User, db.session))
    admin.add_view(MyModelView(Test, db.session))
    admin.add_view(MyModelView(TestFactor, db.session))
    admin.add_view(MyModelView(AnswerChoice, db.session))
    admin.add_view(MyModelView(Question, db.session))
    admin.add_view(MyModelView(Answer, db.session))

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

        print("--------- DB created ----------")
        print(User.query.filter_by(username="admin").first())
        if not User.query.filter_by(username="admin").first():
            print("------------ No Admin Role found ------------")
            from .authorize import hash_it
            new_admin = User(email='admin@admin.com', username='admin', password=hash_it('admin'), is_admin=1)
            db.session.add(new_admin)
            db.session.commit()

    return app
