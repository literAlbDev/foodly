import os
from app.models import Meal, MealTag, User, MealPlan
from app import create_app, db
import random
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

def plan_meals(user_id, unwanted_tags):
    # Retrieve user allergies from the User model
    user = User.query.get(user_id)
    user_allergies = user.allergies

    # Query meals that do not contain any of the user's allergies
    meals = Meal.query.filter(Meal.user_id == user_id).filter(~Meal.ingredients.contains(user_allergies))

    # Randomly select meals for the next 3 days
    planned_meals = random.sample(list(meals), 3)
    # Create MealPlan objects for each planned meal with their dates
    meal_plans = []
    today = datetime.now().date()
    for i, meal in enumerate(planned_meals):
        date = today + timedelta(days=i)
        meal_plan = MealPlan(meal=meal, meal_date=date, user=user, meal_type='dinner')
        meal_plans.append(meal_plan)

    # Save the meal plans to the database
    db.session.add_all(meal_plans)
    db.session.commit()

    return meal_plans

# if app is run directly, a cli version of the app is run which does: sign in and/or sign up, adding allergies and meals, and planning meals

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    while True:
        input("Press Enter to continue...")
        clear()
        print("1. Sign in")
        print("2. Sign up")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            sign_in()
        elif choice == "2":
            sign_up()
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

    print("Done!")

def sign_in():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password_hash, password):
        print("Successfully signed in!")
        while True:
            input("Press Enter to continue...")
            clear()
            print("1. Add allergies")
            print("2. Add meals")
            print("3. Plan meals")
            print("4. See current tags")
            print("5. See current meals")
            print("6. See current plan")
            print("7. Update existing meal")
            print("8. Sign out")

            inner_choice = input("Enter your choice: ")

            if inner_choice == "1":
                add_allergies(user)
            elif inner_choice == "2":
                add_meal(user)
            elif inner_choice == "3":
                plan_meals(user)
            elif inner_choice == "4":
                see_current_tags()
            elif inner_choice == "5":
                see_current_meals(user)
            elif inner_choice == "6":
                see_current_plan(user)
            elif inner_choice == "7":
                update_meal(user)
            elif inner_choice == "8":
                break
            else:
                print("Invalid choice. Please try again.")

    else:
        print("Invalid username or password.")

def sign_up():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        print("Username already exists.")
    else:
        user = User(username=username, password_hash=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        print("Successfully signed up!")

def add_allergies(user):
    allergies = input("Enter your allergies (comma-separated): ").split(",")

    user.allergies = allergies
    db.session.commit()
    print("Allergies added successfully.")

def add_meal(user):
    meal_name = input("Enter the meal name: ")
    ingredients = input("Enter the ingredients (comma-separated): ").split(",")
    tags = input("Enter the tags (comma-separated): ").split(",")

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
    meal.tags = meal_tags

    db.session.add(meal)
    db.session.commit()
    print("Meal added successfully.")

def plan_meals(user):
    unwanted_tags = input("Enter unwanted tags (comma-separated): ").split(",")

    meals = Meal.query.filter(Meal.user_id == user.id).filter(~Meal.ingredients.contains(user.allergies)).filter(~Meal.tags.any(MealTag.name.in_(unwanted_tags)))
    planned_meals = random.sample(list(meals), 3)

    meal_plans = []
    today = datetime.now().date()
    for i, meal in enumerate(planned_meals):
        date = today + timedelta(days=i)
        meal_plan = MealPlan(meal=meal, meal_date=date, user=user, meal_type='dinner')
        meal_plans.append(meal_plan)

    db.session.add_all(meal_plans)
    db.session.commit()

    for meal_plan in meal_plans:
        print(f"Planned meal: {meal_plan.meal.name} on {meal_plan.meal_date}")

def see_current_tags():
    tags = MealTag.query.all()
    print("Current tags:")
    for tag in tags:
        print(tag.name)

def see_current_meals(user):
    meals = Meal.query.filter(Meal.user_id == user.id).all()
    print("Current meals:")
    for meal in meals:
        print(meal.name)

def see_current_plan(user):
    meal_plans = MealPlan.query.filter(MealPlan.user_id == user.id).all()
    print("Current plan:")
    for meal_plan in meal_plans:
        print(f"Meal: {meal_plan.meal.name} on {meal_plan.meal_date}")

def update_meal(user):
    meal_name = input("Enter the meal name to update: ")
    meal = Meal.query.filter_by(name=meal_name, user_id=user.id).first()

    if meal:
        new_name = input("Enter the new meal name: ")
        new_ingredients = input("Enter the new ingredients (comma-separated): ").split(",")

        meal.name = new_name
        meal.ingredients = new_ingredients
        db.session.commit()
        print("Meal updated successfully.")
    else:
        print("Meal not found.")

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        main()
