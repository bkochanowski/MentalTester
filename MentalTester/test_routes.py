from flask import Blueprint, render_template, flash
from flask_login import login_required
from .models import Test, Question

survey = Blueprint('survey', __name__)


@survey.route('/survey/<int:test_id>')
@login_required
def get_test_details(test_id):
    show_details = Test.query.filter_by(id=test_id).first()
    all_questions = Question.query.filter_by(test_id=test_id).all()
    if not all_questions:
        flash('Jeszcze nie ma pytań do tego testu.')
    return render_template("test_details.html", test=show_details, questions=all_questions)


#
# @survey.route('/question/<int:question_id>')
# @login_required
# def redirect_to_first_question(response, test):
#     first_question = test.questions.order_by('id').first()
#     first_question_url = url_for('question', question_id=first_question.id)
#     response.redirect(url=first_question_url, method='GET')
