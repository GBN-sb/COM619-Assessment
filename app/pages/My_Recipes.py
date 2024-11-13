import streamlit as st
from Settings import display_settings

# Page layout setup
st.set_page_config(page_title="My Recipes", layout="wide")

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

def display_recipes(recipes):
    for recipe in recipes:
        with st.container():
            st.write(f"**{recipe['title']}**")
            col1, col2 = st.columns([1, 1], gap="small")
            with col1:
                if st.button("Edit", key=f"edit_{recipe['title']}"):
                    st.write(f"Editing {recipe['title']}...")
                    # TODO add functionality for buttons
            with col2:
                if st.button("Remove", key=f"remove_{recipe['title']}"):
                    st.write(f"Removing {recipe['title']}...")
                    # TODO add functionality for buttons
            st.write("---")

# Initialize recipes
recipes = [{"title": "Title 1"}, {"title": "Title 2"}, {"title": "Title 3"}]

# Main content area
if st.session_state.show_settings:
    display_settings()  # Display settings in the main content area
else:
    st.title("My Recipes")
    display_recipes(recipes)