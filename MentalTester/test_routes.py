from flask import Blueprint, render_template, flash
from flask_login import login_required
from .models import Test, Question, AnswerChoices
from .forms import SurveyForm

survey = Blueprint('survey', __name__)


@survey.route('/survey/<int:test_id>')
@login_required
def get_test_details(test_id):
    show_details = Test.query.filter_by(id=test_id).first()
    all_questions = Question.query.filter_by(test_id=test_id).all()
    if not all_questions:
        flash('Jeszcze nie ma pytań do tego testu.')

    form = SurveyForm()
    form.options.choices = [(choice.id, choice.option) for choice in AnswerChoices.query.filter_by(test=test_id).all()]

    return render_template("test_details.html", test=show_details, questions=all_questions, form=form)
