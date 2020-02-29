import datetime
from collections import defaultdict
from flask import Blueprint, render_template, flash, request, url_for, redirect
from flask_login import login_required, current_user
from .models import Test, Question, AnswerChoice, Answer, TestFactor, Result, db
from .forms import make_form
from sqlalchemy import desc

survey = Blueprint('survey', __name__)

actual_day = datetime.datetime.now()


def calculate_percentage(percent, whole):
    return (percent / whole) * 100.00


@survey.route('/test/<int:test_id>', methods=['GET', 'POST', 'PUT'])
@login_required
def get_test_details(test_id):
    show_details = Test.query.filter_by(id=test_id).first()

    new_answer = Answer(session_id=current_user.id, test_id=test_id, answer_time=actual_day)
    db.session.add(new_answer)
    db.session.commit()

    get_answer_row = Answer.query.filter_by(session_id=current_user.id, test_id=test_id).order_by(
        desc(Answer.answer_time)).first()
    max_choice_value = AnswerChoice.query.filter_by(test_id=test_id).order_by(desc(AnswerChoice.value)).first()
    answer_id = get_answer_row.id
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
            questions_count = Question.query.filter_by(test_id=test_id, has_factor=int(key)).count()
            max_factor_sum = (max_choice_value.value * questions_count)
            user_percent_score = calculate_percentage(value, max_factor_sum)
            new_factor_answer = Result(answer_id=answer_id, factor_id=int(key), user_score=value,
                                       max_factor_value=max_factor_sum, percent_score=user_percent_score,
                                       submit_date=actual_day)

            db.session.add(new_factor_answer)
            db.session.commit()

        return redirect(url_for('survey.results', test_id=test_id))

    return render_template("test_details.html", test_id=test_id, answer_id=answer_id,
                           test=show_details,
                           questions=all_test_questions,
                           form=form)


@survey.route('/results/<int:test_id>', methods=['GET', 'POST'])
@login_required
def results(test_id):
    show_details = Test.query.filter_by(id=test_id).first()
    show_factors = TestFactor.query.filter_by(test_id=test_id).order_by(TestFactor.id).all()
    answer_row = Answer.query.filter_by(session_id=current_user.id, test_id=test_id).order_by().first()
    how_many_factors = TestFactor.query.filter_by(test_id=test_id).count()
    factor_results = Result.query.filter_by(answer_id=answer_row.id, submit_date=answer_row.answer_time).order_by(Result.factor_id).limit(how_many_factors).all()

    return render_template('test_results.html', test=show_details, results=factor_results, factors=show_factors)
