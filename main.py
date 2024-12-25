import os
from app.models import Meal, MealTag, User, MealPlan
from app import create_app, db
import random
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def sign_in(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        return user
    return None


def sign_up(username, password):
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return False
    user = User(username=username,
                password_hash=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()
    return True


def add_allergies(user, allergies):
    user.allergies = allergies
    db.session.commit()


def add_meal(user, meal_name, ingredients, tags):
    meal = Meal(name=meal_name, ingredients=ingredients, user_id=user.id)
    meal_tags = []
    for tag_name in tags:
        tag = MealTag.query.filter_by(name=tag_name).first()
        if tag:
            meal_tags.append(tag)
        else:
            new_tag = MealTag(name=tag_name)
            db.session.add(new_tag)
            meal_tags.append(new_tag)
    meal.meal_tags = meal_tags
    db.session.add(meal)
    db.session.commit()


def plan_meals(user, unwanted_tags, start_date, end_date):
    meals = Meal.query.filter(Meal.user_id == user.id)
    if unwanted_tags:
        meals = meals.filter(~Meal.meal_tags.any(
            MealTag.name.in_(unwanted_tags)))
    if user.allergies:
        for allergy in user.allergies:
            meals = meals.filter(~Meal.ingredients.contains(allergy))

    # Convert start_date and end_date to datetime objects
    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Invalid date format. Please use YYYY-MM-DD.")

    # Get existing meal plans within the date range
    existing_meal_plans = MealPlan.query.filter(
        MealPlan.user_id == user.id,
        MealPlan.meal_date >= start_date,
        MealPlan.meal_date <= end_date
    ).all()
    existing_dates = {meal_plan.meal_date for meal_plan in existing_meal_plans}

    planned_meals = random.choices(
        list(meals), k=(end_date - start_date).days + 1)
    meal_plans = []
    current_date = start_date

    for meal in planned_meals:
        while current_date in existing_dates:
            current_date += timedelta(days=1)

        meal_plan = MealPlan(meal=meal, meal_date=current_date,
                             user=user, meal_type='dinner')
        db.session.add(meal_plan)
        meal_plans.append(meal_plan)
        # existing_dates.add(current_date)
        current_date += timedelta(days=1)

    db.session.commit()
    return meal_plans


def get_current_tags():
    return MealTag.query.all()


def get_current_meals(user):
    return Meal.query.filter(Meal.user_id == user.id).all()


def get_current_plan(user):
    return MealPlan.query.filter(MealPlan.user_id == user.id).all()


def update_meal(user, meal_name, new_name, new_ingredients):
    meal = Meal.query.filter_by(name=meal_name, user_id=user.id).first()
    if meal:
        meal.name = new_name
        meal.ingredients = new_ingredients
        db.session.commit()
        return True
    return False


def update_current_plan(user, index, new_meal_name, new_meal_date):
    meal_plans = MealPlan.query.filter(MealPlan.user_id == user.id).all()
    if index < 0 or index >= len(meal_plans):
        return False
    meal_plan = meal_plans[index]
    meal = Meal.query.filter_by(name=new_meal_name, user_id=user.id).first()
    if not meal:
        return False
    try:
        new_meal_date = datetime.strptime(new_meal_date, "%Y-%m-%d").date()
    except ValueError:
        return False
    meal_plan.meal = meal
    meal_plan.meal_date = new_meal_date
    db.session.commit()
    return True
