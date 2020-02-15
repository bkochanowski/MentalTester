from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))  # string must be long, because it will be hashed

    def __init__(self, email, username, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

    #classes below need to be verified
class Test(db.Model):
    __tablename__ = 'tests'

    id = db.Column(db.Integer, primary_key=True)
    test_title = db.Column(db.String, nullable=False)
    questions = db.relationship('Question', backref='survey', lazy='dynamic')

    def __init__(self, test_title):
        self.test_title = test_title


class Question(db.Model):
    __tablename__ = 'questions'

    TEXT = 'text'
    NUMERIC = 'numeric'
    BOOLEAN = 'boolean'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    kind = db.Column(db.Enum(TEXT, NUMERIC, BOOLEAN,
                             name='question_kind'))
    survey_id = db.Column(db.Integer, db.ForeignKey('surveys.id'))
    answers = db.relationship('Answer', backref='question', lazy='dynamic')

    def __init__(self, content, kind=TEXT):
        self.content = content
        self.kind = kind

    def next(self):
        return self.survey.questions.filter(Question.id > self.id).order_by('id').first()


class Answer(db.Model):
    __tablename__ = 'answers'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    session_id = db.Column(db.String, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
