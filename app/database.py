import os.path
from app import app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

# osdir = os.path.abspath(os.path.dirname(__file__))
#
# app.config['SQLALCHEMY_DATABASE_URL'] = \
#     'sqlite:///' + os.path.join(osdir, 'pantry.db')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#
# # app.config['SECRET KEY'] = "guess-me"
# db = SQLAlchemy(app)


class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food_name = db.Column(db.String(100), nullable=False)
    expiration = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())

    def __repr__(self):
        return f'<Food {self.food_name}>'
