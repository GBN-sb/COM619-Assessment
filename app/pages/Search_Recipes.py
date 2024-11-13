import streamlit as st

st.set_page_config(page_title="Create Recipes", layout="wide")

# Sidebar buttons
col1, col2 = st.sidebar.columns(2)
button1 = col1.button('Logout')
button2 = col2.button('Settings')

def display_recipe_search(recipes, available_tags):
    st.title("Search Recipes")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input("Search by title:")
    with col2:
        selected_tags = st.multiselect("Filter by tags:", options=available_tags)
    
    def recipe_matches(recipe):
        title_match = search_query.lower() in recipe["title"].lower()
        tag_match = any(tag in recipe["tags"] for tag in selected_tags) if selected_tags else True
        return title_match and tag_match
    
    # Filter the recipes
    filtered_recipes = [recipe for recipe in recipes if recipe_matches(recipe)]
    
    # Display filtered recipes
    st.subheader("Results")
    if filtered_recipes:
        for recipe in filtered_recipes:
            st.markdown(f"### {recipe['title']}")
            st.write(f"Tags: {', '.join(recipe['tags'])}")
            st.write("---")
    else:
        st.write("No recipes found matching your criteria.")

# TODO: Add backend processing and functionality for form_data when finished
available_tags = ["Italian", "Pasta", "Indian", "Spicy", "Mexican", "Snack"]
recipes = [
    {"title": "Spaghetti Bolognese", "tags": ["Italian", "Pasta"]},
    {"title": "Chicken Curry", "tags": ["Indian", "Spicy"]},
    {"title": "Tacos", "tags": ["Mexican", "Snack"]}
]

form_data = display_recipe_search(recipes, available_tags)
