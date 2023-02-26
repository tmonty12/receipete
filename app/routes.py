from flask import redirect, flash, render_template, request, url_for, request
from app import app, db
from app.forms import LoginForm, CreateAccountForm, SearchIngredientsForm, AddIngredientsForms
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Ingredient
from werkzeug.urls import url_parse
from app.api import query_ingredients

# Landing page containing list of generated Recipes
# login_required decorator will redirect user if they are not logged into an account
@app.route('/')
@app.route('/index')
@login_required
def index():
    return 'Recipes!'

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    # If user is already logged in, redirect them to landing page
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()

    # Ensures that all form fields were validated and had no errors
    if form.validate_on_submit():

        # Will query user based on username submitted in form
        user = User.query.filter_by(username=form.username.data).first()
        print(user)

        # If a user with the username dne or the user entered the wrong password
        # display error to user and redirect back to login page. 
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')

        # If next_page url param dne or is not valid, will redirect to landing page
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    ## TO DO: implement login.html template that includes login form
    # return render_template('login.html', title='Log In', form=form)
    user = {'username' : 'Sarah'}
    ##return render_template('index.html', title = 'Home', user = user)
    return render_template('login.html', title='Sign In', form=form)

# Logout page
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# Create account page
@app.route('/create-account', methods=['GET', 'POST'])
def create_account():
    # If user is already logged in, redirect them to landing page
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = CreateAccountForm()
    if form.validate_on_submit():

        # Create a user, set the password, commit the user to the db and redirect to the login page
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    ## TO DO: implement create-account.html template that includes create account form
    # return render_template('create-account.html', title='Create Account', form=form)
    #return 'Create account page'
    return render_template('register.html', title='Register', form=form)

@app.route('/pantry', methods=['GET', 'POST'])
@login_required
def pantry():
    ingredients = current_user.ingredients.all()
    return render_template('pantry.html', title='Pantry', ingredients=ingredients)

@app.route('/ingredients/search', methods=['GET', 'POST'])
@login_required
def search_ingredients():
    search_form = SearchIngredientsForm()
    add_form = AddIngredientsForms()
    ingredients = []

    if request.form.get('submit') == 'Search' and search_form.validate():
        ingredients = query_ingredients(search_form.ingredient.data)
        ingredients = [(f"{ingredient['id']},{ingredient['name']},{ingredient['image']}", ingredient['name'])  for ingredient in ingredients]
        add_form.ingredients.choices = ingredients

    if request.form.get('submit') == 'Add Ingredients':
        for ingredient in add_form.ingredients.data:
            api_id, name, image = ingredient.split(',')
            ingredient = Ingredient(api_id=int(api_id), name=name, image=image, user=current_user)
            db.session.add(ingredient)
        db.session.commit()

    return render_template('ingredients.html', title='Search Ingredients', search_form=search_form, add_form=add_form, ingredients=ingredients)
