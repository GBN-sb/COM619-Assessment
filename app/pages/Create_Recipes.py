import streamlit as st
from Settings import display_settings, hide_settings

# Page layout setup
st.set_page_config(page_title="Create Recipes", layout="wide")

# Initialize session state for settings display toggle
if "show_settings" not in st.session_state:
    st.session_state.show_settings = False

# Sidebar setup with buttons for Logout and Settings
with st.sidebar:
    col1, col2 = st.columns(2)
    if col1.button("Logout"):
        # Implement logout logic here
        st.write("You have been logged out.")  # Placeholder
    if col2.button("Settings"):
        st.session_state.show_settings = not st.session_state.show_settings

def display_form():
    """Displays the recipe creation form and returns form inputs."""
    with st.form("recipe_form"):
        # Title and Difficulty fields
        col1, col2 = st.columns([2, 1], gap="small")
        with col1:
            title = st.text_input("Title:")
        with col2:
            difficulty = st.slider("Difficulty (1-5):", min_value=1, max_value=5, step=1)

        # Tags and Image fields
        tags = st.text_input("Tags:")
        image = st.file_uploader("Image:", type=["jpg", "jpeg", "png"])

        # Ingredients and Steps fields
        ingredients = st.text_area("Ingredients:", height=100)
        steps = st.text_area("Steps:", height=150)

        # Description / Notes field
        description = st.text_area("Description / Notes:", height=100)

        # Finish button
        finished = st.form_submit_button("Finish")

    return {
        "title": title,
        "difficulty": difficulty,
        "tags": tags,
        "image": image,
        "ingredients": ingredients,
        "steps": steps,
        "description": description,
        "finished": finished
    }

# Main content area
if st.session_state.show_settings:
    display_settings()  # Display settings in the main content area
else:
    st.title("Create Recipes")
    hide_settings()
    display_form()

# TODO: Add backend processing and functionality for form_data when finished
