from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))  # string must be long, because it will be hashed

    def __init__(self, email, username, password):
        self.username = username
        self.email = email
        self.password = password


class Test(db.Model):
    __tablename__ = 'tests'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    test_title = db.Column(db.String(60), nullable=False)
    test_instructions = db.Column(db.String(200), nullable=False)
    questions = db.relationship('Question', backref='test', lazy='dynamic')
    factors = db.relationship('TestFactors', backref='test_factor', lazy='dynamic')

    def __init__(self, test_title, test_instructions):
        self.test_title = test_title
        self.test_instructions = test_instructions

    @property
    def has_questions(self):
        return self.questions.count() > 0


class TestFactors(db.Model):
    __tablename__ = 'factors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id'), nullable=False)
    question_factor = db.relationship('Question', backref='questions.has_factor', lazy='dynamic')

    def __init__(self, name):
        self.name = name


class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    number = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String(200), nullable=False)
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id'))
    has_factor = db.Column(db.Integer, db.ForeignKey('factors.id'), nullable=False)
    answers = db.relationship('Answer', backref='question', lazy='dynamic')

    def __init__(self, content):
        self.content = content

    def next(self):
        return self.test.questions.filter(Question.id > self.id).order_by('id').first()


class AnswerChoices(db.Model):
    __tablename__ = 'choices'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    option = db.Column(db.String(50), nullable=False)
    value = db.Column(db.Integer, nullable=True)
    test = db.Column(db.Integer, db.ForeignKey('tests.id'))

    def __init__(self, option, value):
        self.option = option
        self.value = value

    def __repr__(self, option, value):
        self.option = option
        self.value = value

    # class below to be changed ASAP!!!!


class Answer(db.Model):
    __tablename__ = 'answers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    given_value = db.Column(db.Integer, nullable=True)
    session_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))

    @classmethod
    def update_content(cls, given_value, session_id, question_id):
        existing_answer = cls.query.filter(Answer.session_id == session_id and
                                           Answer.question_id == question_id).first()
        existing_answer.given_value = given_value
        db.session.add(existing_answer)
        db.session.commit()

    def __init__(self, given_value, session_id, question_id):
        self.given_value = given_value
        self.question_id = question_id
        self.session_id = session_id

    def __repr__(self, given_value, session_id, question_id):
        self.given_value = given_value
        self.question_id = question_id
