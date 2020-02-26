from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user
from .models import Test

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    all_tests = Test.query.all()
    if not all_tests:
        flash("Brak testów w bazie!")
        return render_template('profile.html', name=current_user.username)

    return render_template('profile.html', tests=all_tests, name=current_user.username)
