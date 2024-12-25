import random
from app import create_app, db
from app.models import User, Meal, MealTag
from werkzeug.security import generate_password_hash

def create_test_data():
    # Create a single user
    user = User(username='t', password_hash=generate_password_hash('t'))
    db.session.add(user)
    db.session.commit()

    # Create meal tags
    tags = ['Vegetarian', 'Vegan', 'Gluten-Free', 'Dairy-Free', 'Nut-Free']
    meal_tags = [MealTag(name=tag) for tag in tags]
    db.session.add_all(meal_tags)
    db.session.commit()

    # Create meals
    meals = [
        Meal(name='Spaghetti Bolognese', ingredients=['spaghetti', 'beef', 'tomato sauce'], user_id=user.id),
        Meal(name='Vegetable Stir Fry', ingredients=['broccoli', 'carrot', 'soy sauce'], user_id=user.id),
        Meal(name='Chicken Salad', ingredients=['chicken', 'lettuce', 'tomato'], user_id=user.id),
        Meal(name='Beef Tacos', ingredients=['beef', 'taco shells', 'lettuce', 'cheese'], user_id=user.id),
        Meal(name='Quinoa Salad', ingredients=['quinoa', 'cucumber', 'tomato', 'feta'], user_id=user.id),
        Meal(name='Grilled Cheese Sandwich', ingredients=['bread', 'cheese', 'butter'], user_id=user.id),
        Meal(name='Pancakes', ingredients=['flour', 'milk', 'eggs', 'syrup'], user_id=user.id),
        Meal(name='Lentil Soup', ingredients=['lentils', 'carrot', 'celery', 'onion'], user_id=user.id),
        Meal(name='Fish Tacos', ingredients=['fish', 'taco shells', 'cabbage', 'lime'], user_id=user.id)
    ]
    db.session.add_all(meals)
    db.session.commit()

    # Assign tags to meals
    meals[0].meal_tags.append(meal_tags[0])  # Spaghetti Bolognese - Vegetarian
    meals[1].meal_tags.append(meal_tags[1])  # Vegetable Stir Fry - Vegan
    meals[2].meal_tags.append(meal_tags[2])  # Chicken Salad - Gluten-Free
    meals[3].meal_tags.append(meal_tags[3])  # Beef Tacos - Dairy-Free
    meals[4].meal_tags.append(meal_tags[0])  # Quinoa Salad - Vegetarian
    meals[5].meal_tags.append(meal_tags[4])  # Grilled Cheese Sandwich - Nut-Free
    meals[6].meal_tags.append(meal_tags[4])  # Pancakes - Nut-Free
    meals[7].meal_tags.append(meal_tags[1])  # Lentil Soup - Vegan
    meals[8].meal_tags.append(meal_tags[2])  # Fish Tacos - Gluten-Free

    db.session.commit()

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
        create_test_data()
        print("Test data created successfully.")