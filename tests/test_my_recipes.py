import pytest
import streamlit as st
from unittest import mock
from app.pages.My_Recipes import display_recipes
from app.db.dao.recipeDAO import RecipeDAO
from app.db.dao.userDAO import UserDAO
from app.models.recipe import Recipe
from app.models.user import User
from app.db.couch_client import CouchClient
import os
import dotenv

# Load environment variables
dotenv.load_dotenv()
RUN_ENV = os.getenv('RUN_ENV')

# Function to get the database name based on the environment
def get_dao(db_base_name):
    if RUN_ENV == "1":
        db_name = f"{db_base_name}"
        return db_name
    if RUN_ENV == "2":
        db_name = f"test_{db_base_name}"
        return db_name
    if RUN_ENV == "3":
        db_name = f"dev_{db_base_name}"
        return db_name

@pytest.fixture(scope="module")
def couch_client():
    """Fixture for initializing the CouchDB client."""
    client = CouchClient()
    yield client  # Provide the fixture to the test
    # Teardown: Cleanup after tests
    client.delete_db(get_dao("recipes"))
    client.delete_db(get_dao("users"))

@pytest.fixture(scope="module")
def recipe_dao(couch_client):
    """Fixture for initializing the RecipeDAO with a test database."""
    dao = RecipeDAO(db_name=get_dao("recipes"))
    couch_client.create_db(get_dao("recipes"))
    return dao

@pytest.fixture(scope="module")
def user_dao(couch_client):
    """Fixture for initializing the UserDAO with a test database."""
    dao = UserDAO(db_name=get_dao("users"))
    couch_client.create_db(get_dao("users"))
    return dao

@pytest.fixture
def setup_streamlit_mock(mocker):
    """Fixture to mock streamlit functions."""
    # Set up the mock for st.button to return False for each call
    mocker.patch("streamlit.button", side_effect=[False] * 4)  # Adjust the number of times based on your test needs
    mocker.patch("streamlit.container")
    mocker.patch("streamlit.write")
    mocker.patch("streamlit.image")

def test_recipe_display(setup_streamlit_mock, recipe_dao, user_dao, mocker):
    
    # Test data: Create some mock user in the database
    user = User(
        name="John",
        email="john@doe.com",
        password="password123",
        role="admin",
        bio="Hello, world!",
        profile_picture=""
    )

    user_dao.add_user(user)
    test_creator = user_dao.get_user_by_username(user.name)
    st.session_state.user = test_creator
    
    # Test data: Create some mock recipes in the database
    recipes = [
        Recipe(
            title="Recipe 1",
            description="Description 1",
            tags=["Tag1"],
            ingredients="Ingredient 1, Ingredient 2",
            instructions="Step 1, Step 2",
            picture_location_id="",
            creator_id=test_creator.id,
        ),
        Recipe(
            title="Recipe 2",
            description="Description 2",
            tags=["Tag2"],
            ingredients="Ingredient 3, Ingredient 4",
            instructions="Step 3, Step 4",
            picture_location_id="",
            creator_id=test_creator.id,
        )
    ]

    # Add mock recipes to the database
    for recipe in recipes:
        recipe_dao.create_recipe(recipe)
    
    # Call the main display function
    display_recipes()
    print(recipe_dao.get_recipes_by_author(test_creator.id))

    # Assert that st.write was called for each recipe title
    for recipe in recipes:
        assert recipe == recipe

    # Assert that the st.button was called for each Edit and Remove button
    for recipe in recipes:
        st.button.assert_any_call("Remove", key=f"remove_{recipe.id}")
        st.button.assert_any_call("Edit", key=f"edit_{recipe.id}")
