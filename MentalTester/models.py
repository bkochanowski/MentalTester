from flask_login import UserMixin
from . import db
from hashlib import md5


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))  # string must be long, because it will be hashed

    def hash_it(self):
        """method for encrypting passwords with salt"""
        return md5(self.password.encode('UTF8MB4')).hexdigest()

    def __init__(self, email, username, password):
        self.username = username
        self.email = email
        self.password = password

    # classes below need to be verified


class Test(db.Model):
    __tablename__ = 'tests'

    id = db.Column(db.Integer, primary_key=True)
    test_title = db.Column(db.String, nullable=False)
    questions = db.relationship('Question', backref='test', lazy='dynamic')

    def __init__(self, test_title):
        self.test_title = test_title

    @property
    def has_questions(self):
        return self.questions.count() > 0


class Question(db.Model):
    __tablename__ = 'questions'

    TEXT = 'text'
    NUMERIC = 'numeric'
    BOOLEAN = 'boolean'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    kind = db.Column(db.Enum(TEXT, NUMERIC, BOOLEAN,
                             name='question_kind'))
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id'))
    answers = db.relationship('Answer', backref='question', lazy='dynamic')

    def __init__(self, content, kind=TEXT):
        self.content = content
        self.kind = kind

    def next(self):
        return self.test.questions.filter(Question.id > self.id).order_by('id').first()


class Answer(db.Model):
    __tablename__ = 'answers'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(50), nullable=False)
    session_id = db.Column(db.String, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))

    def __init__(self, content, question, session_id):
        self.content = content
        self.question = question
        self.session_id = session_id
