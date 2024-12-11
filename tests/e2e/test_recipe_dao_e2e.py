import pytest
from app.db.dao.userDAO import UserDAO
from app.models.user import User
from app.db.dao.recipeDAO import RecipeDAO
from app.models.recipe import Recipe
from app.db.couch_client import CouchClient

@pytest.fixture(scope="module")
def couch_client():
    """Fixture for initializing the CouchDB client."""
    client = CouchClient()
    yield client
    client.delete_db("test_recipes")
    client.delete_db("test_users")

@pytest.fixture(scope="module")
def recipe_dao(couch_client):
    """Fixture for initializing the RecipeDAO with a test database."""
    dao = RecipeDAO(db_name="test_recipes")
    couch_client.create_db("test_users")
    couch_client.create_db("test_recipes")
    return dao

def test_end_to_end_recipe_operations(recipe_dao):
    """End-to-end test for RecipeDAO operations."""
    # Create a user
    new_user = User(name="John", email="JohnDoe@example.com", password="password123", role="user", bio="Hello, World!", profile_picture="https://example.com/profile.jpg")
    user_dao = UserDAO(db_name="test_users")
    user_dao.add_user(new_user)
    # Get user id
    user = user_dao.get_user_by_email("JohnDoe@example.com")
    if user is None:
        assert False
    user_id = user.id

    # Add recipe
    new_recipe = Recipe(title="Pancakes", description="Delicious pancakes", ingredients=["flour", "milk", "eggs"], instructions="Some instructions" , picture_location="https://example.com/pancakes.jpg", creator_id=user_id)
    assert recipe_dao.create_recipe(new_recipe) is not None

    # Get recipe by title
    fetched_recipe = recipe_dao.get_recipe_by_name("Pancakes")
    print(fetched_recipe)
    assert fetched_recipe is not None
    assert fetched_recipe.title == "Pancakes"
    assert fetched_recipe.description == "Delicious pancakes"

    # Update recipe
    fetched_recipe.description = "Some new description"
    assert recipe_dao.update_recipe(fetched_recipe) is not None
    updated_recipe = recipe_dao.get_recipe_by_name("Pancakes")
    assert updated_recipe.description == "Some new description"

    # Get all recipes
    all_recipes = recipe_dao.get_recipes()
    assert len(all_recipes) == 1

    # Delete recipe
    assert recipe_dao.delete_recipe(fetched_recipe.id) is True
    all_recipes = recipe_dao.get_recipes()
    assert len(all_recipes) == 0
    # Delete user
    user_dao.delete_user(user_id)
    all_users = user_dao.get_all_users()
    assert len(all_users) == 0
    