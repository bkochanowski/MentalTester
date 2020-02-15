from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from .models import User
from hashlib import md5
from . import db

authorized = Blueprint('authorized', __name__)


def hash_it(password):
    """method for encrypting passwords with salt"""
    return md5(password.encode('utf-8')).hexdigest()


@authorized.route('/login')
def login():
    return render_template('login.html')


@authorized.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = hash_it(request.form.get('password'))
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()
    if not user or not user.password == password:
        flash('Błędny email lub hasło. Sprawdź czy dobrze wpisałeś dane')
        return redirect(url_for('authorized.login'))
        # if the above check passes, I know the user has the right credentials
    else:
        login_user(user, remember=remember)
        return redirect(url_for('main.profile'))


@authorized.route('/register')
def register():
    return render_template('register.html')


@authorized.route('/register', methods=['POST'])
def register_post():
    email = request.form.get('email')
    username = request.form.get('name')
    password = hash_it(request.form.get('password'))
    password2 = hash_it(request.form.get('password2'))

    if password != password2:
        flash('Wpisane hasła nie są takie same. Spróbuj ponownie')
        return redirect(url_for('authorized.register'))

    user = User.query.filter_by(
        email=email).first()  # if this returns a user then the email already exists in db

    if user:  # if a user in db, user redirected to signup page to try again
        flash('Już istnieje użytkownik o podanym adresie mailowym')
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
