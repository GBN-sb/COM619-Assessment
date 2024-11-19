import streamlit as st

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

display_form()

# TODO: Add backend processing and functionality for form_data when finished
