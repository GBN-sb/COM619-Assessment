import streamlit as st
from navigation import make_sidebar
from db.dao.recipeDAO import RecipeDAO
from db.dao.userDAO import UserDAO
from models.recipe import Recipe
import uuid
import os
import dotenv

dotenv.load_dotenv()
RUN_ENV = os.getenv('RUN_ENV')

# Define the folder for storing uploaded images
UPLOAD_FOLDER = "db/dao/recipe_pics"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_dao(db_base_name):
    if RUN_ENV == "1":
        db_name = f"{db_base_name}"
        return db_name
    if RUN_ENV == "2":
        db_name = f"test_{db_base_name}"
        return db_name
    if RUN_ENV == "3":
        db_name = f"dev_{db_base_name}"
        return db_name

recipe_dao = RecipeDAO(db_name=get_dao("recipes"))
user_dao = UserDAO(db_name="users")

def display_form():
    """Displays the recipe creation form and returns form inputs."""
    st.title("🍳 Create Recipes")
    with st.form("recipe_form"):
        # Title
        title = st.text_input("Title:")

        col1, col2 = st.columns([1, 1], gap="small")
        # Tags and Image fields
        tags = col1.text_input("Tags: (Separated by commas)")

        # Image upload
        uploaded_file = col2.file_uploader("Upload an image:", type=["png", "jpg", "jpeg"])
        image_file_name = None

        if uploaded_file is not None:
            # Generate a unique file name
            unique_filename = f"{uuid.uuid4().int}.jpg"
            image_path = os.path.join(UPLOAD_FOLDER, unique_filename)

            # Save the uploaded file
            with open(image_path, "wb") as f:
                f.write(uploaded_file.read())

            image_file_name = unique_filename

        # Ingredients and Steps fields
        ingredients = st.text_area("Ingredients: (Separated by commas at the end of new lines)", height=100)
        steps = st.text_area("Steps: (Separated by commas at the end of new lines)", height=150)

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
        "image_file_name": image_file_name,
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
            picture_location_id=form_data["image_file_name"],
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