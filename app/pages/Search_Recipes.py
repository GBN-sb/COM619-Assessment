import streamlit as st
from navigation import make_sidebar
from db.dao.recipeDAO import RecipeDAO
import os
import dotenv

dotenv.load_dotenv()
RUN_ENV = os.getenv('RUN_ENV')

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

# Directory for recipe images
IMAGE_FOLDER = "db/dao/recipe_pics"
os.makedirs(IMAGE_FOLDER, exist_ok=True)

def format_multiline_text(text):
    """
    Converts multi-line text into a Markdown-formatted unordered list.
    Each line becomes a list item.
    """
    lines = text.strip().split("\n")
    formatted = "\n".join(f"- {line}" for line in lines if line.strip())
    return formatted

def display_recipe_search():
    st.title("🍽️ Search Recipes")

    # Fetch all recipes from the database
    recipes = recipe_dao.get_recipes()

    # Extract available tags from recipes dynamically
    available_tags = list(
        set(
            tag.strip() 
            for recipe in recipes 
            for tag in (recipe.tags if isinstance(recipe.tags, list) else recipe.tags.split(','))
        )
    )

    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input("Search by title:")
    with col2:
        selected_tags = st.multiselect("Filter by tags:", options=available_tags)

    def recipe_matches(recipe):
        recipe_tags = recipe.tags if isinstance(recipe.tags, list) else recipe.tags.split(',')
        title_match = search_query.lower() in recipe.title.lower()
        tag_match = (
            any(tag in recipe_tags for tag in selected_tags)
            if selected_tags
            else True
        )
        return title_match and tag_match

    # Filter the recipes
    filtered_recipes = [recipe for recipe in recipes if recipe_matches(recipe)]

    # Display filtered recipes
    st.subheader("Results")
    if filtered_recipes:
        for recipe in filtered_recipes:
            st.markdown(f"### {recipe.title}")
            col1, col2 = st.columns([1, 1], gap="large")
            col1.write(f"Tags: {', '.join(recipe.tags if isinstance(recipe.tags, list) else recipe.tags.split(','))}")
            col1.write(f"Ingredients: \n{format_multiline_text(recipe.ingredients)}")
            col1.write(f"Steps: \n{format_multiline_text(recipe.instructions)}")
            col1.write(f"Description: {recipe.description}")
            with col2:
                # Check if the recipe has an associated image
                if recipe.picture_location_id:
                    image_path = os.path.join(IMAGE_FOLDER, recipe.picture_location_id)
                    if os.path.exists(image_path):
                        st.image(image_path, caption=recipe.title, width=400)
                    else:
                        st.write("No image available.")
                else:
                    st.write("No image available.")
            st.write("---")
    else:
        st.write("No recipes found matching your criteria.")

def main():  # pragma: no cover
    st.set_page_config(layout="wide")
    make_sidebar()

    # Call the display function
    display_recipe_search()

if __name__ == "__main__":  # pragma: no cover
    main()
