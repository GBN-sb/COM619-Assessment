import streamlit as st
from navigation import make_sidebar


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


def main():  # pragma: no cover
    st.set_page_config(layout="wide")
    make_sidebar()

    # Initialize recipes
    recipes = [{"title": "Title 1"}, {"title": "Title 2"}, {"title": "Title 3"}]

    display_recipes(recipes)


# Run the main function
if __name__ == "__main__":  # pragma: no cover
    main()
