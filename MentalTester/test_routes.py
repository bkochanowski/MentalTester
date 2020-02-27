from collections import defaultdict
from flask import Blueprint, render_template, flash, request
from flask_login import login_required, current_user
from .models import Test, Question, AnswerChoice, Answer, Result, db
from .forms import make_form

survey = Blueprint('survey', __name__)


@survey.route('/survey/<int:test_id>', methods=['GET', 'POST', 'PUT'])
@login_required
def get_test_details(test_id):
    show_details = Test.query.filter_by(id=test_id).first()

    answer_row = Answer.query.filter_by(session_id=current_user.id, test_id=test_id).first()
    if not answer_row:
        flash('Niestety nie możesz brać udziału w tym kwestionariuszu')
        return render_template('test_details.html', test_id=test_id, test=show_details)

    answer_id = answer_row.id
    all_test_questions = Question.query.filter_by(test_id=test_id).all()

    if not all_test_questions:
        flash('Jeszcze nie ma pytań do tego testu.')
        return render_template('profile.html', name=current_user.username)

    choices = [(choice.value, choice.option) for choice in AnswerChoice.query.filter_by(test_id=test_id).all()]

    form = make_form(all_test_questions, choices)

    if request.method == 'POST':
        results = []
        for element in form:
            if element.id.startswith('q_'):
                results.append([f'{element.id.split("_")[2]}', int(element.data)])

        grouped_results = defaultdict(lambda: 0)
        for name, value in results:
            grouped_results[name] += value

        converted_results = dict(grouped_results)
        for key, value in converted_results.items():
            new_factor_answer = Result(answer_id=answer_id, factor_id=int(key), user_score=value, max_factor_value=24)
            db.session.add(new_factor_answer)
            db.session.commit()

        return render_template('test_results.html', test_id=test_id)

    return render_template("test_details.html", test_id=test_id, answer_id=answer_id, test=show_details,
                           questions=all_test_questions,
                           form=form)


@survey.route('/survey/results/<int:test_id>', methods=['GET', 'POST'])
@login_required
def get_results(test_id, test):
    pass
    return render_template('test_results.html')
