import streamlit as st

# Page layout setup
st.set_page_config(page_title="My Recipes", layout="wide")

# Sidebar buttons
col1, col2 = st.sidebar.columns(2)
button1 = col1.button('Logout')
button2 = col2.button('Settings')

st.title("My Recipes")

# TODO Load recipe data dynamically
recipes = [
    {"title": "Title 1"},
    {"title": "Title 2"},
    {"title": "Title 3"}
]

# Loop through each recipe and create a layout with Edit and Remove buttons
for recipe in recipes:
    with st.container():
        # Display recipe title
        st.write(f"**{recipe['title']}**")

        # Edit and Remove buttons in a horizontal layout
        col1, col2 = st.columns([1, 1], gap="small")
        with col1:
            if st.button("Edit", key=f"edit_{recipe['title']}"):
                st.write(f"Editing {recipe['title']}...")
                # TODO add button functionality
        with col2:
            if st.button("Remove", key=f"remove_{recipe['title']}"):
                st.write(f"Removing {recipe['title']}...")
                # TODO add button functionality

        # Spacing between recipe entries
        st.write("---")
