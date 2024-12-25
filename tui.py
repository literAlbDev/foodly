from main import clear, sign_in, sign_up, add_allergies, add_meal, plan_meals, get_current_tags, get_current_meals, get_current_plan, update_meal, update_current_plan
from app import create_app


def main():
    while True:
        input("Press Enter to continue...")
        clear()
        print("1. Sign in")
        print("2. Sign up")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            user = sign_in(username, password)
            if user:
                print("Successfully signed in!")
                user_menu(user)
            else:
                print("Invalid username or password.")
        elif choice == "2":
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            if sign_up(username, password):
                print("Successfully signed up!")
            else:
                print("Username already exists.")
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

    print("Done!")


def user_menu(user):
    while True:
        input("Press Enter to continue...")
        clear()
        print("1. See current tags")
        print("2. See current meals")
        print("3. See current plan")
        print("4. Add allergies")
        print("5. Add meals")
        print("6. Plan meals")
        print("7. Update existing meal")
        print("8. Update current plan")
        print("9. Sign out")

        inner_choice = input("Enter your choice: ")

        if inner_choice == "1":
            tags = get_current_tags()
            print("Current tags:")
            for tag in tags:
                print(tag.name)
        elif inner_choice == "2":
            meals = get_current_meals(user)
            print("Current meals:")
            for meal in meals:
                print(
                    f"{meal.name} ({', '.join(tag.name for tag in meal.meal_tags)})")
                print("Ingredients: " + ", ".join(meal.ingredients))
                print("")
        elif inner_choice == "3":
            meal_plans = get_current_plan(user)
            meal_plans.sort(key=lambda x: x.meal_date)
            print("Current plan:")
            for meal_plan in meal_plans:
                print(f"Meal: {meal_plan.meal.name} on {meal_plan.meal_date}")
        elif inner_choice == "4":
            allergies = input(
                "Enter your allergies (comma-separated): ").split(",")
            add_allergies(user, allergies)
            print("Allergies added successfully.")
        elif inner_choice == "5":
            meal_name = input("Enter the meal name: ")
            ingredients = input(
                "Enter the ingredients (comma-separated): ").split(",")
            tags = input("Enter the tags (comma-separated): ").split(",")
            add_meal(user, meal_name, ingredients, tags)
            print("Meal added successfully.")
        elif inner_choice == "6":
            unwanted_tags = input(
                "Enter unwanted tags (comma-separated): ").split(",")
            start_date = input("Enter the start date (YYYY-MM-DD): ")
            end_date = input("Enter the end date (YYYY-MM-DD): ")
            try:
                meal_plans = plan_meals(
                    user, unwanted_tags, start_date, end_date)
                for meal_plan in meal_plans:
                    print(
                        f"Planned meal: {meal_plan.meal.name} on {meal_plan.meal_date}")
            except ValueError as e:
                print(e)
        elif inner_choice == "7":
            meal_name = input("Enter the meal name to update: ")
            new_name = input("Enter the new meal name: ")
            new_ingredients = input(
                "Enter the new ingredients (comma-separated): ").split(",")
            if update_meal(user, meal_name, new_name, new_ingredients):
                print("Meal updated successfully.")
            else:
                print("Meal not found.")
        elif inner_choice == "8":
            meal_plans = get_current_plan(user)
            print("Current plan:")
            for i, meal_plan in enumerate(meal_plans):
                print(f"{i+1}. Meal: {meal_plan.meal.name} on {meal_plan.meal_date}")

            choice = input(
                "Enter the number of the meal plan to edit (or '0' to cancel): ")
            if choice == "0":
                continue

            try:
                index = int(choice) - 1
                new_meal_name = input("Enter the new meal name: ")
                new_meal_date = input("Enter the new meal date (YYYY-MM-DD): ")
                if update_current_plan(user, index, new_meal_name, new_meal_date):
                    print("Meal plan updated successfully.")
                else:
                    print("Invalid choice or meal not found.")
            except ValueError:
                print("Invalid choice. Please enter a number.")
        elif inner_choice == "9":
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        main()
