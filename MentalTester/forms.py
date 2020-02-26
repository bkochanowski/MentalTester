from flask_wtf import FlaskForm
from wtforms import SelectField


def make_form(questions, answers):
    class _Form(FlaskForm):
        pass

    options = answers
    for question in questions:
        id_plus_factor = f'{question.id}_{question.has_factor}'
        setattr(_Form, f"q_{id_plus_factor}", SelectField(f'{question.number}, {question.content}:', choices=options))
    return _Form()
