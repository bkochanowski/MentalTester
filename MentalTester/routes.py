from flask import render_template
from .models import User
from . import app

@app.route('/')
def index():
    return render_template('Index')

@app.route('/profile')
def profile():
    return render_template('Profile')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/logout')
def logout():
    return render_template('logout')