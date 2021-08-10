from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))  # string must be long, because it will be hashed
    is_admin = db.Column(db.Integer, default=int(0))

    def __init__(self, email, username, password, is_admin):
        self.username = username
        self.email = email
        self.password = password
        self.is_admin = is_admin


class Test(db.Model):
    __tablename__ = 'tests'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    test_title = db.Column(db.String(60), nullable=False)
    test_instructions = db.Column(db.String(200), nullable=False)
    questions = db.relationship('Question', backref='test', lazy='dynamic')
    factors = db.relationship('TestFactor', backref='test_factor', lazy='dynamic')

    def __init__(self, test_title, test_instructions):
        self.test_title = test_title
        self.test_instructions = test_instructions

    def __repr__(self):
        return f'przynależy do: --{self.test_title}--'


class TestFactor(db.Model):
    __tablename__ = 'factors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id'), nullable=False)

    def __init__(self, name, description, test_id):
        self.name = name
        self.description = description
        self.test_id = test_id


class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    number = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String(200), nullable=False)
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id'), nullable=False)
    has_factor = db.Column(db.Integer, db.ForeignKey('factors.id'), nullable=False)

    def __init__(self, number, content, test_id, has_factor):
        self.number = number
        self.content = content
        self.test_id = test_id
        self.has_factor = has_factor


class AnswerChoice(db.Model):
    __tablename__ = 'choices'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    option = db.Column(db.String(50), nullable=False)
    value = db.Column(db.Integer, nullable=False)
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id'), nullable=False)

    def __init__(self, option, value, test_id):
        self.option = option
        self.value = value
        self.test_id = test_id

    def __repr__(self, option, value):
        self.option = option
        self.value = value

    # classes below need to be verified!


class Answer(db.Model):
    __tablename__ = 'answers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    session_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id'), nullable=False)
    answer_time = db.Column(db.DateTime, nullable=False)
    factor_results = db.relationship('Result', backref='results.answer_id', lazy='dynamic')

    def __init__(self, session_id, test_id, answer_time):
        self.session_id = session_id
        self.test_id = test_id
        self.answer_time = answer_time


class Result(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    answer_id = db.Column(db.Integer, db.ForeignKey('answers.id'), nullable=False)
    factor_id = db.Column(db.Integer, nullable=False)
    user_score = db.Column(db.Integer, nullable=False)
    max_factor_value = db.Column(db.Integer, nullable=False)
    percent_score = db.Column(db.Float, nullable=False)
    submit_date = db.Column(db.DateTime, nullable=False)
    when_submit = db.relationship('Answer', backref='results.answer_time')
