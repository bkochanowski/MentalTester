from flask import Blueprint, render_template, redirect, url_for, request
from .models import User
from hashlib import md5
from . import db

authorized = Blueprint('authorized', __name__)


def hash_it(password):
    """method for encrypting passwords"""
    return md5(password.encode('utf-8')).hexdigest()


@authorized.route('/login')
def login():
    return render_template('login.html')


@authorized.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    return redirect(url_for('main.profile'))

    # user = User.query.filter_by(email=email).first()
    # if not user or not check_password_hash(user.password, password):
    # flash('Please check your login details and try again.')
    # return redirect(url_for('authorized.login'))
    # if the above check passes, then we know the user has the right credentials


@authorized.route('/register')
def register():
    return render_template('register.html')


@authorized.route('/register', methods=['POST'])
def register_post():
    email = request.form.get('email')
    username = request.form.get('name')
    password = request.form.get('password')
    hash_password = hash_it(password)

    user = User.query.filter_by(
        email=email).first()  # if this returns a user then the email already exists in db

    if user:  # if a user in db, user redirected to signup page to try again
        return redirect(url_for('authorized.register'))
    new_user = User(email=email, username=username, password=hash_password)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('authorized.login'))


@authorized.route('/logout')
def logout():
    return 'Logout'
