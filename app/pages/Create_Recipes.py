import streamlit as st
from navigation import make_sidebar
from db.dao.recipeDAO import RecipeDAO
from db.dao.userDAO import UserDAO
from models.recipe import Recipe
import os
import dotenv

dotenv.load_dotenv()
RUN_ENV = os.getenv('RUN_ENV')

def get_dao(db_base_name):
    if RUN_ENV == "1":
        db_name=f"{db_base_name}"
        return db_name
    if RUN_ENV == "2":
        db_name=f"test_{db_base_name}"
        return db_name
    if RUN_ENV == "3":
        db_name=f"dev_{db_base_name}"
        return db_name

recipe_dao = RecipeDAO(db_name=get_dao("recipes"))
user_dao = UserDAO(db_name="users")

def display_form():
    """Displays the recipe creation form and returns form inputs."""
    st.title("🍳 Create Recipes")
    with st.form("recipe_form"):
        # Title
        title = st.text_input("Title:")

        # Tags and Image fields
        tags = st.text_input("Tags:")

        # Ingredients and Steps fields
        ingredients = st.text_area("Ingredients:", height=100)
        steps = st.text_area("Steps:", height=150)

        # Description / Notes field
        description = st.text_area("Description / Notes:", height=100)

        # Finish button
        finished = st.form_submit_button("Finish")

    return {
        "title": title,
        "description": description,
        "tags": tags,
        "ingredients": ingredients,
        "steps": steps,
        "finished": finished,
    }


def main():  # pragma: no cover
    make_sidebar()
    # Display the form and get user input
    form_data = display_form()

    creator_id = st.session_state.user.id

    if form_data["finished"]:
        # Create a Recipe instance
        recipe = Recipe(
            title=form_data["title"],
            description=form_data["description"],
            tags=form_data["tags"],
            ingredients=form_data["ingredients"],
            instructions=form_data["steps"],
            picture_location="db\\profile_pics\\no_pfp.png",
            creator_id=creator_id
        )

        # Add the recipe to the database
        result = recipe_dao.create_recipe(recipe)

        # Provide feedback to the user
        if result:
            st.success("Recipe added successfully!")
        else:
            st.error("An error occurred while adding the recipe. Please try again.")


if __name__ == "__main__":  # pragma: no cover
    main()
