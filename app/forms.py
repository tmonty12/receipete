from flask_wtf import FlaskForm
from wtforms import FieldList, StringField, PasswordField, BooleanField, SubmitField, SelectMultipleField, TextAreaField, widgets
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User
from app.api import allergies


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class ChangePasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Change')

class CreateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class SearchIngredientsForm(FlaskForm):
    ingredient = StringField('Ingredient', validators=[DataRequired()])
    submit = SubmitField('Search')

class AddIngredientsForm(FlaskForm):
    ingredients = SelectMultipleField(choices=[], option_widget=widgets.CheckboxInput())
    submit = SubmitField('Add Ingredients')

class DeleteIngredientsForm(FlaskForm):
    ingredients = SelectMultipleField(choices=[], option_widget=widgets.CheckboxInput())
    submit = SubmitField('Delete Items')

class EditIngredientForm(FlaskForm):
    expiration_date = DateField('Expiration Date') #format='%d/%m/%Y'
    submit = SubmitField('Update Item')

class SearchRecipesForm(FlaskForm):
    recipe = StringField('Ingredients', validators=[DataRequired()])
    submit = SubmitField('Search')

class EditAllergiesForm(FlaskForm):
    allergies = SelectMultipleField(choices=[(allergy, allergy) for allergy in allergies], option_widget=widgets.CheckboxInput())
    submit = SubmitField('Edit Allergies')

class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Post')

class timeLimitForm(FlaskForm):
    time = StringField('Maximum Cooking Time (minutes)', validators=[DataRequired()], render_kw={"placeholder": "60"})
    submit = SubmitField('Filter')