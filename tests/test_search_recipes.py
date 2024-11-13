import pytest
import streamlit as st
from itertools import cycle
from app.pages import Search_Recipes  # Adjust import as needed

@pytest.fixture
def setup_streamlit_mock(mocker):
    """Fixture to mock streamlit functions."""
    mocker.patch("streamlit.text_input", return_value="Spaghetti")  # Mock search input
    mocker.patch("streamlit.multiselect", return_value=["Italian"])  # Mock selected tags
    mocker.patch("streamlit.markdown")  # Mock markdown for displaying recipe titles
    mocker.patch("streamlit.write")  # Mock write for displaying recipe tags

def test_display_recipe_search(setup_streamlit_mock, mocker):
    """Test that the search and filter functionality in `display_recipe_search` works as expected."""
    # Sample recipe data
    recipes = [

        {"title": "Spaghetti Bolognese", "tags": ["Italian", "Pasta"]},
        {"title": "Chicken Curry", "tags": ["Indian", "Spicy"]},
        {"title": "Tacos", "tags": ["Mexican", "Snack"]},
    ]
    available_tags = ["Italian", "Pasta", "Indian", "Spicy", "Mexican", "Snack"]

    # Call the display_recipe_search function
    Search_Recipes.display_recipe_search(recipes, available_tags)

    # Check that st.text_input was called for the search bar
    st.text_input.assert_called_once_with("Search by title:")

    # Check that st.multiselect was called with the correct tag options
    st.multiselect.assert_called_once_with("Filter by tags:", options=available_tags)

    # Check that st.markdown and st.write were called to display "Spaghetti Bolognese"
    st.markdown.assert_any_call("### Spaghetti Bolognese")
    st.write.assert_any_call("Tags: Italian, Pasta")
    st.write.assert_any_call("---")

    # Ensure that only the matching recipe is displayed
    st.markdown.assert_called_once()
    # The 2 things in the call count for this case are the display tags and the seperator line
    assert st.write.call_count == 2
