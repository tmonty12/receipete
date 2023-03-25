from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime


# Tells flask how to get user object given an id
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# User table
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    ingredients = db.relationship('Ingredient', backref='user', lazy='dynamic')
    allergies = db.relationship('Allergy', backref='user', lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    api_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    expiration_date = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Ingredient {self.name}>'

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    api_id = db.Column(db.Integer, index=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    instructions = db.Column(db.Text)
    preparation_time = db.Column(db.Integer, nullable=False, default=0)
    ingredients = db.relationship('RecipeIngredient', backref='recipe', lazy='dynamic')
    comments = db.relationship('Comment', backref='recipe', lazy='dynamic')

    def __repr__(self):
        return f'<Recipe {self.name}>'

class RecipeIngredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    image=db.Column(db.String(100), nullable=False)
    unit = db.Column(db.String(100), nullable=False)

class Allergy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(64), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Allergy {self.type}>'

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_api_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comment = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return f'<Comment {self.id}>'
