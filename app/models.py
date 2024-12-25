from datetime import datetime

from flask_login import UserMixin
from . import db

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    allergies = db.Column(db.JSON)
    meals = db.relationship('Meal', backref='user', lazy=True)

class Meal(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  name = db.Column(db.String(100), nullable=False)
  ingredients = db.Column(db.JSON)
  meal_tags = db.relationship('MealTag', secondary='meal_mealtag', back_populates="meals")

class MealTag(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), nullable=False)
  meals = db.relationship('Meal', secondary='meal_mealtag', back_populates="meal_tags")

meal_mealtag = db.Table('meal_mealtag',
  db.Column('meal_id', db.Integer, db.ForeignKey('meal.id'), primary_key=True),
  db.Column('mealtag_id', db.Integer, db.ForeignKey('meal_tag.id'), primary_key=True)
)

class MealPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    meal_id = db.Column(db.Integer, db.ForeignKey('meal.id'), nullable=False)
    meal_type = db.Column(db.String(20), nullable=False)
    meal_date = db.Column(db.Date, nullable=False)
    is_eaten = db.Column(db.Boolean, default=False)
    rating = db.Column(db.Integer)
    comment = db.Column(db.String(200))
    user = db.relationship('User', backref='mealplans')
    meal = db.relationship('Meal', backref='mealplans')
