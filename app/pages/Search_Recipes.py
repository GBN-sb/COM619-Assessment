import streamlit as st
from navigation import make_sidebar


def display_recipe_search(recipes, available_tags):
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input("Search by title:")
    with col2:
        selected_tags = st.multiselect("Filter by tags:", options=available_tags)

    def recipe_matches(recipe):
        title_match = search_query.lower() in recipe["title"].lower()
        tag_match = (
            any(tag in recipe["tags"] for tag in selected_tags)
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
            st.markdown(f"### {recipe['title']}")
            st.write(f"Tags: {', '.join(recipe['tags'])}")
            st.write("---")
    else:
        st.write("No recipes found matching your criteria.")


def main():  # pragma: no cover
    st.set_page_config(layout="wide")
    make_sidebar()

    # Define available tags and recipes
    available_tags = ["Italian", "Pasta", "Indian", "Spicy", "Mexican", "Snack"]
    recipes = [
        {"title": "Spaghetti Bolognese", "tags": ["Italian", "Pasta"]},
        {"title": "Chicken Curry", "tags": ["Indian", "Spicy"]},
        {"title": "Tacos", "tags": ["Mexican", "Snack"]},
    ]

    # Call the display function
    display_recipe_search(recipes, available_tags)


if __name__ == "__main__":  # pragma: no cover
    main()
