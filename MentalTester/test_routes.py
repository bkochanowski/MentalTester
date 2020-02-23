from flask import Blueprint, render_template, flash, request
from flask_login import login_required, current_user
from .models import Test, Question, AnswerChoices
from .forms import make_form

survey = Blueprint('survey', __name__)


@survey.route('/survey/<int:test_id>', methods=['GET', 'POST'])
@login_required
def get_test_details(test_id):
    show_details = Test.query.filter_by(id=test_id).first()
    all_questions = Question.query.filter_by(test_id=test_id).all()
    choices = [(choice.value, choice.option) for choice in AnswerChoices.query.filter_by(test=test_id).all()]
    if not all_questions:
        flash('Jeszcze nie ma pytań do tego testu.')

    form = make_form(all_questions, choices)

    if request.method == 'POST':
        # this is made only for testing purposes, needs to be changed later
        results = []
        for element in form:
            # import pdb; pdb.set_trace()
            session_id = current_user.id
            if element.id.startswith('q_'):
                results.append(f"id użytkownika:{session_id}, id testu: {test_id}, numer pytania: {element.id}, wynik {element.data}")

        return render_template('test_results.html', results=results)

    return render_template("test_details.html", test=show_details, questions=all_questions, form=form)


@survey.route('/survey/results', methods=['GET', 'POST'])
@login_required
def get_results():
    return render_template('test_results.html')
