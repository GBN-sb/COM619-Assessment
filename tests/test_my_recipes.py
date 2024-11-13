import pytest
import streamlit as st
from itertools import cycle
from app.pages import My_Recipes
from app.Settings import display_settings

@pytest.fixture
def setup_streamlit_mock(mocker):
    """Fixture to mock streamlit functions."""
    mocker.patch("streamlit.button")
    mocker.patch("streamlit.container")
    mocker.patch("streamlit.write")

def test_recipe_display(setup_streamlit_mock, mocker):
    # Mock button clicks
    mocker.patch("streamlit.button", side_effect=cycle([False]))

    # Test data
    recipes = [
        {"title": "Title 1"},
        {"title": "Title 2"},
        {"title": "Title 3"}
    ]

    # Call the page file's main display function
    My_Recipes.display_recipes(recipes)

    # Assert that st.write was called for each recipe title
    for recipe in recipes:
        st.write.assert_any_call(f"**{recipe['title']}**")

    # Assert that the st.button was called for each Edit and Remove button
    for recipe in recipes:
        st.button.assert_any_call("Edit", key=f"edit_{recipe['title']}")
        st.button.assert_any_call("Remove", key=f"remove_{recipe['title']}")
