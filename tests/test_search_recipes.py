import pytest
import streamlit as st
from app.pages import Search_Recipes  # Adjust import as needed
from db.dao.userDAO import UserDAO
from app.models.recipe import Recipe  # Assuming the Recipe model is imported from the correct path

@pytest.fixture
def setup_streamlit_mock(mocker):
    """Fixture to mock streamlit functions."""
    mocker.patch("streamlit.text_input", return_value="Spaghetti")  # Mock search input
    mocker.patch("streamlit.multiselect", return_value=["Italian"])  # Mock selected tags
    mocker.patch("streamlit.markdown")  # Mock markdown for displaying recipe titles
    mocker.patch("streamlit.write")  # Mock write for displaying recipe tags
    mocker.patch("streamlit.image")  # Mock image display

    # Mock the st.columns to return mock column objects that support context manager protocol
    mock_column = mocker.MagicMock()
    mock_column.__enter__.return_value = mock_column  # Allow context manager use
    mock_column.__exit__.return_value = False  # No exception handling, as expected by context manager

    # Return a list of two mock columns (as the original code uses two columns)
    mocker.patch("streamlit.columns", return_value=[mock_column, mock_column])

def test_display_recipe_search(setup_streamlit_mock, mocker):
    """Test that the search and filter functionality in `display_recipe_search` works as expected."""
    # Sample recipe data using the Recipe model
    recipes = [
        Recipe(
            title="Spaghetti Bolognese", 
            description="A classic Italian dish", 
            tags=["Italian", "Pasta"], 
            ingredients="Pasta, Meat", 
            instructions="Cook", 
            picture_location_id="spaghetti.jpg", 
            creator_id="user123"
        ),
        Recipe(
            title="Chicken Curry", 
            description="A spicy curry", 
            tags=["Indian", "Spicy"], 
            ingredients="Chicken, Spices", 
            instructions="Cook", 
            picture_location_id=None, 
            creator_id="user456"
        ),
        Recipe(
            title="Tacos", 
            description="A delicious Mexican snack", 
            tags=["Mexican", "Snack"], 
            ingredients="Tortillas, Meat", 
            instructions="Cook", 
            picture_location_id=None, 
            creator_id="user789"
        ),
    ]
    available_tags = ["Italian", "Pasta", "Indian", "Spicy", "Mexican", "Snack"]
    
    # Sort the expected list to match the actual order
    expected_tags = sorted(available_tags)
    
    # Mock the get_recipes method to return our sample recipes
    mocker.patch.object(Search_Recipes.recipe_dao, "get_recipes", return_value=recipes)
    
    # Call the display_recipe_search function
    Search_Recipes.display_recipe_search()

    # Check that st.text_input was called for the search bar
    st.text_input.assert_called_once_with("Search by title:")
    
    # Check that st.markdown and st.write were called to display "Spaghetti Bolognese"
    st.markdown.assert_any_call("### Spaghetti Bolognese")
    st.write.assert_any_call("---")
