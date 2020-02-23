from flask_wtf import FlaskForm
from wtforms import SelectField


def make_form(questions, answers):
    class _Form(FlaskForm):
        pass

    options = answers
    for question in questions:
        setattr(_Form, f"q_{question.id}", SelectField(f'{question.number}, {question.content}:', choices=options)),
    return _Form()
