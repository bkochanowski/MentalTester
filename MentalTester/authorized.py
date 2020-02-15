from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db

authorized = Blueprint('authorized', __name__)


@authorized.route('/login')
def login():
    return render_template('login.html')


@authorized.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = User.hash_it(request.form.get('password'))
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()
    if not user or user.password != password:
        flash('Błędny e-mail lub hasło.')
        return redirect(url_for('authorized.login'))

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))


@authorized.route('/register')
def register():
    return render_template('register.html')


@authorized.route('/register', methods=['POST'])
def register_post():
    email = request.form.get('email')
    username = request.form.get('name')
    password = User.hash_it(request.form.get('password'))
    password2 = User.hash_it(request.form.get('password2'))

    user = User.query.filter_by(
        email=email).first()  # if this returns a user then the email already exists in db

    if user:  # if a user in db, user redirected to register page to try again
        flash('Użytkownik o podanym adresie email już istnieje')
        return redirect(url_for('authorized.register'))

    if password != password2:
        flash('Błąd. Podane hasła nie są identyczne. Spróbuj ponownie.')
        return redirect(url_for('authorized.register'))

    new_user = User(email=email, username=username, password=password)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('authorized.login'))


@authorized.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
