import os
from app.models import Meal, MealTag, User, MealPlan
from app import create_app, db
import random
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

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
            print("8. Update current plan")
            print("9. Sign out")

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
                update_current_plan(user)
            elif inner_choice == "9":
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
        print(f"Meal: {meal.name} - Tags: {', '.join(tag.name for tag in meal.meal_tags)}")
        print("Ingredients: " + ", ".join(meal.ingredients))
        print("")

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

def update_current_plan(user):
    meal_plans = MealPlan.query.filter(MealPlan.user_id == user.id).all()
    print("Current plan:")
    for i, meal_plan in enumerate(meal_plans):
        print(f"{i+1}. Meal: {meal_plan.meal.name} on {meal_plan.meal_date}")

    choice = input("Enter the number of the meal plan to edit (or '0' to cancel): ")
    if choice == "0":
        return

    try:
        index = int(choice) - 1
        if index < 0 or index >= len(meal_plans):
            print("Invalid choice. Please try again.")
            return

        meal_plan = meal_plans[index]
        print(f"Editing meal plan: {meal_plan.meal.name} on {meal_plan.meal_date}")

        new_meal_name = input("Enter the new meal name: ")
        new_meal_date = input("Enter the new meal date (YYYY-MM-DD): ")

        meal = Meal.query.filter_by(name=new_meal_name, user_id=user.id).first()
        if not meal:
            print("Meal not found.")
            return

        try:
            new_meal_date = datetime.strptime(new_meal_date, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
            return

        meal_plan.meal = meal
        meal_plan.meal_date = new_meal_date
        db.session.commit()
        print("Meal plan updated successfully.")

    except ValueError:
        print("Invalid choice. Please enter a number.")

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        main()
