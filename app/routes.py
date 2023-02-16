from flask import redirect, flash, render_template, request
from app import app
from app.forms import LoginForm, CreateAccountForm
from flask_login import current_user, login_user, logout_user
from app.models import User
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
@login_required
def index():
    return "Recipes!"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(usernam=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    ## TO DO: implement login.html template that includes login form
    # return render_template('login.html', title='Log In', form=form)
    return 'Login page'

@app.route('/logout')
def logout():
    logout_user()
    return redierct(url_for('index'))

@app.route('/create-account', methods=['GET', 'POST'])
def create_account():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = CreateAccountForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    ## TO DO: implement create-account.html template that includes create account form
    # return render_template('create-account.html', title='Create Account', form=form)
    return 'Create account page'