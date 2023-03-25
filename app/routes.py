from flask import redirect, flash, render_template, request, url_for, request
from app import app, db
from app.forms import LoginForm, CreateAccountForm, SearchIngredientsForm, AddIngredientsForm, DeleteIngredientsForm, \
    SearchRecipesForm, EditIngredientForm, EditAllergiesForm, ChangePasswordForm, CommentForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Ingredient, Allergy, Recipe, RecipeIngredient, Comment
from werkzeug.urls import url_parse
from app.api import query_ingredients, query_recipes, query_recipe_information
from datetime import datetime


# Landing page containing list of generated Recipes
# login_required decorator will redirect user if they are not logged into an account
@app.route('/')
@app.route('/index')
@login_required
def index():
    recipes = []
    ingredients = current_user.ingredients.all()
    ingredients_query = ''
    for ingredient in ingredients:
        ingredients_query += f'{ingredient.name},'

    recipes = query_recipes(ingredients_query)
    recipes = [(f"{recipe['id']}", f"{recipe['title']}", f"{recipe['image']}") for recipe in recipes]

    return render_template('recipes.html', title='Recipes', recipes=recipes)


@app.route('/recipe/<id>', methods=['GET', 'POST'])
@login_required
def view_recipe(id):
    form = CommentForm()
    recipe = Recipe.query.filter_by(api_id=id).first()
    comments = []

    if recipe is None:
        recipe_information = query_recipe_information(id)
        recipe = Recipe(api_id=id, name=recipe_information['title'], image=recipe_information['image'], instructions=recipe_information['instructions'], preparation_time=int(recipe_information['preparationMinutes']))
        db.session.add(recipe)
        for extendedIngredient in recipe_information['extendedIngredients']:
            ingredient = RecipeIngredient(name=extendedIngredient['name'], amount=float(extendedIngredient['amount']), unit=extendedIngredient['unit'], image=extendedIngredient['image'], recipe=recipe)
            db.session.add(ingredient)
        db.session.commit()
    else:
        comments = recipe.comments.all()
        for comment in comments:
            comment.username = User.query.filter_by(id=comment.user_id).first().username
    
    if form.validate_on_submit():
        comment = Comment(comment=form.comment.data, recipe=recipe, user=current_user)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('view_recipe', id=id))

    return render_template('recipe_instructions.html', title='Instructions', recipe=recipe, form=form, comments=comments)


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
    user = {'username': 'Sarah'}
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
    # return 'Create account page'
    return render_template('register.html', title='Register', form=form)


@app.route('/pantry', methods=['GET'])
@login_required
def pantry():
    # First need to grab ingredients with expiration date and sort by ascending date.
    # Then grab ingredients without expiration date and append them to the end of ingredients list
    ingredients = current_user.ingredients.filter(Ingredient.expiration_date != None).order_by(Ingredient.expiration_date).all()
    ingredients += current_user.ingredients.filter_by(expiration_date=None).all()
    return render_template('pantry.html', title='Pantry', ingredients=ingredients)


@app.route('/pantry/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit_pantry_item(id):
    ingredient = Ingredient.query.filter_by(id=id).first()
    if not ingredient:
        return redirect(url_for('pantry'))
    form = EditIngredientForm()
    if form.validate_on_submit():
        ingredient.expiration_date = form.expiration_date.data
        db.session.commit()
        return redirect(url_for('pantry'))
    elif ('expiration_date' in form.errors):
        flash(f"Error with expiration date value: {form.errors['expiration_date']}")

    return render_template('edit_pantry_item.html', title='Edit Pantry Item', ingredient=ingredient, form=form)


@app.route('/pantry/delete', methods=['GET', 'POST'])
@login_required
def delete_pantry_items():
    ingredients = current_user.ingredients.all()
    form = DeleteIngredientsForm()
    form.ingredients.choices = [(ingredient.id, f"{ingredient.name},{ingredient.expiration_date.strftime('%Y-%m-%d') if ingredient.expiration_date else ''},{ingredient.image}") for ingredient in ingredients]

    if request.form.get('submit') == 'Delete Items':
        for ingredient in form.ingredients.data:
            ingredient = Ingredient.query.filter_by(id=int(ingredient)).first()
            db.session.delete(ingredient)
            flash(f'You have deleted {ingredient.name} from your pantry.')
        db.session.commit()
        return redirect(url_for('delete_pantry_items'))

    return render_template('delete_pantry_items.html', form=form, ingredients=ingredients)


@app.route('/ingredients/search', methods=['GET', 'POST'])
@login_required
def search_ingredients():
    search_form = SearchIngredientsForm()
    add_form = AddIngredientsForm()
    ingredients = []
    
    if request.form.get('submit') == 'Search' and search_form.validate():
        ingredients = query_ingredients(search_form.ingredient.data)
        if len(ingredients) == 0:
            flash(f"No ingredients matched your query: {search_form.ingredient.data}")
        else:
            ingredients = [(f"{ingredient['id']},{ingredient['name']},{ingredient['image']}",
                            f"{ingredient['name']},{ingredient['image']}") for ingredient in ingredients]
            add_form.ingredients.choices = ingredients

    if request.form.get('submit') == 'Add Ingredients':
        if len(add_form.ingredients.data) == 0:
            flash('You did not select any ingredients to add to your pantry')
        else:
            for ingredient in add_form.ingredients.data:
                api_id, name, image = ingredient.split(',')
                expiration_date = request.form.get(f'expiration-date-{name}')
                if expiration_date != '':
                    expiration_date = datetime.strptime(request.form.get(f'expiration-date-{name}'), '%Y-%m-%d')
                    ingredient = Ingredient(api_id=int(api_id), name=name, image=image, user=current_user, expiration_date=expiration_date)
                else:
                    ingredient = Ingredient(api_id=int(api_id), name=name, image=image, user=current_user)
                db.session.add(ingredient)
                flash(f'You have added {name} to your pantry.')
            db.session.commit()
            return redirect(url_for('search_ingredients'))

    return render_template('ingredients.html', title='Search Ingredients', search_form=search_form, add_form=add_form,
                           ingredients=ingredients)

@app.route('/allergies/edit', methods=['GET', 'POST'])
@login_required
def edit_allergies():
    current_user_allergies = [allergy.type for allergy in current_user.allergies.all()]
    form = EditAllergiesForm(allergies=current_user_allergies)

    if form.validate_on_submit():
        for allergy in current_user.allergies.all():
            if allergy.type not in form.allergies.data:
                db.session.delete(allergy)
        for allergy in form.allergies.data:
            if allergy not in current_user_allergies:
                user_allergy = Allergy(user=current_user, type=allergy)
                db.session.add(user_allergy)
        db.session.commit()
        return redirect(url_for('profile'))

    return render_template('edit_allergies.html', title='Edit Allergies', form=form)

@app.route('/profile', methods=['GET'])
@login_required
def profile():
    return render_template('profile.html', title='Profile', allergies=current_user.allergies.all())

@app.route('/profile/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        if current_user.check_password(form.password2.data):
            flash('Can\'t change password to current password.')
        else:
            current_user.set_password(form.password2.data)
            db.session.commit()
            flash('Congratulations, you have successfully changed your password!')
            return redirect(url_for('profile'))
    return render_template('change_password.html', title='Change Password', form=form)

# @app.route('/recipes', methods=['GET', 'POST'])
# @login_required
# def search_recipes():
#     form = SearchRecipesForm()
#     recipes = []

#     if request.form.get('submit') == 'Search' and form.validate():
#         recipes = query_recipes(form.recipe.data)

#         if len(recipes) == 0:
#             flash(f"No recipes matched your query: {form.ingredient.data}")
#         else:
#             recipes = [f"{recipe['id']},{recipe['title']},{recipe['image']}" for recipe in recipes]


#     print(recipes)
#     return render_template('recipes.html', title='Search Recipes', form=form, recipes=recipes)
