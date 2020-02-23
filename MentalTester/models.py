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
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id'))

    def __init__(self, name):
        self.name = name


class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    number = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String(200), nullable=False)
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id'))
    answers = db.relationship('Answer', backref='question', lazy='dynamic')

    def __init__(self, content):
        self.content = content

    def next(self):
        return self.test.questions.filter(Question.id > self.id).order_by('id').first()


class AnswerChoices(db.Model):
    __tablename__ = 'choices'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    option = db.Column(db.String(50), nullable=False)
    extra = db.Column(db.String(50), nullable=True)
    test = db.Column(db.Integer, db.ForeignKey('tests.id'))

    def __init__(self, option, extra):
        self.option = option
        self.extra = extra

    def __repr__(self, option, extra):
        self.option = option
        self.extra = extra


    # class below to be changed ASAP!!!!
class Answer(db.Model):
    __tablename__ = 'answers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(50), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))

    @classmethod
    def update_content(cls, session_id, question_id, content):
        existing_answer = cls.query.filter(Answer.session_id == session_id and
                                           Answer.question_id == question_id).first()
        existing_answer.content = content
        db.session.add(existing_answer)
        db.session.commit()

    def __init__(self, content, question, session_id):
        self.content = content
        self.question = question
        self.session_id = session_id
