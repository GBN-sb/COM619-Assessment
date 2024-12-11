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

def display_recipes():
    st.title("My Recipes")

    # Fetch recipes for the logged-in user
    recipes = recipe_dao.get_recipes_by_author(st.session_state.user.id)

    if not recipes:
        st.write("You have no recipes yet.")
        return

    for recipe in recipes:
        with st.container():
            st.write(f"{recipe.title}")
            col1, col2 ,col3 = st.columns([1, 1, 1], gap="small")
            
            with col1:
                st.markdown("**Ingredients:**")
                st.markdown(format_multiline_text(recipe.ingredients), unsafe_allow_html=True)
            
            with col2:
                st.markdown("**Instructions:**")
                st.markdown(format_multiline_text(recipe.instructions), unsafe_allow_html=True)

            with col3:
                # Check if the recipe has an associated image
                if recipe.picture_location_id:
                    image_path = os.path.join(IMAGE_FOLDER, recipe.picture_location_id)
                    if os.path.exists(image_path):
                        st.image(image_path, caption=recipe.title, use_column_width=True)
                    else:
                        st.write("No image available.")
                else:
                    st.write("No image available.")
            
            st.write(f"**Description:** {recipe.description}")
            
            col5, col6 = st.columns([1, 1], gap="small")
            with col5:
                if st.button("Edit", key=f"edit_{recipe.id}"):
                    st.write(f"Editing {recipe.title}...")
                    # TODO: Implement recipe editing functionality
            with col6:
                if st.button("Remove", key=f"remove_{recipe.id}"):
                    if recipe_dao.delete_recipe(recipe.id):
                        st.success(f"Removed {recipe.title}.")
                        st.experimental_rerun()  # Refresh the page to update the list
                    else:
                        st.error(f"Failed to remove {recipe.title}.")

def main():  # pragma: no cover
    st.set_page_config(layout="wide")
    make_sidebar()
    display_recipes()

# Run the main function
if __name__ == "__main__":  # pragma: no cover
    main()
