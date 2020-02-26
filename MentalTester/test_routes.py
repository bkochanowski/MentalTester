import collections, functools, operator
from flask import Blueprint, render_template, flash, request
from flask_login import login_required, current_user
from .models import Test, Question, AnswerChoice, Answer, Result, db
from .forms import make_form

survey = Blueprint('survey', __name__)


@survey.route('/survey/<int:test_id>', methods=['GET', 'POST'])
@login_required
def get_test_details(test_id):
    show_details = Test.query.filter_by(id=test_id).first()

    answer_id = Answer.query.filter_by(session_id=current_user.id, test_id=test_id).first()
    if not answer_id:
        flash('ten użytkownik jeszcze nie odpowiedział')
    # db.session.add(new_answer)
    # db.session.commit()

    all_test_questions = Question.query.filter_by(test_id=test_id).all()
    if not all_test_questions:
        flash('Jeszcze nie ma pytań do tego testu.')
        return render_template('profile.html', name=current_user.username)

    choices = [(choice.value, choice.option) for choice in AnswerChoice.query.filter_by(test_id=test_id).all()]

    form = make_form(all_test_questions, choices)

    if request.method == 'POST':
        results = []
        # sample output [['factor1', 2], ['factor2', 2], ['factor1', 2], ['factor2', 2], ['factor3', 4], ['factor3', 4]]
        # test_factors = [(factor.id, factor.name) for factor in TestFactor.query.filter_by(test_id=test_id).all()]
        for element in form:
            if element.id.startswith('q_'):
                results.append([f'factor{element.id.split("_")[2]}', int(element.data)])

        grouped_results = {}
        for name, value in results:
            grouped_results.setdefault(name, []).append(value)
            # sample output: {'factor1': [4, 2], 'factor2': [2, 2], 'factor3': [2, 2]}

        return render_template('test_results.html', results_lst=results, grouped_results=grouped_results,
                               questions=all_test_questions)

    return render_template("test_details.html", test_id=test_id, test=show_details, questions=all_test_questions,
                           form=form)


@survey.route('/survey/results', methods=['GET', 'POST'])
@login_required
def get_results(test_id, test):
    pass
    return render_template('test_results.html')
