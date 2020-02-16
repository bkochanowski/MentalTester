from flask import Blueprint, render_template
from flask_login import login_required
from .models import Test

survey = Blueprint('survey', __name__)


@survey.route('/test')
@login_required
def get_test_details():
    show_test = Test.query.filter_by(id=Test.id).first()
    #
    return render_template("test_details.html", test=show_test)


#
# @survey.route('/question/<int:question_id>')
# @login_required
# def redirect_to_first_question(response, test):
#     first_question = test.questions.order_by('id').first()
#     first_question_url = url_for('question', question_id=first_question.id)
#     response.redirect(url=first_question_url, method='GET')
