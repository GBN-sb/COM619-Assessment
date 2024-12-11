import pytest
from app.db.dao.userDAO import UserDAO
from app.models.user import User
from app.db.dao.recipeDAO import RecipeDAO
from app.models.recipe import Recipe
from app.db.couch_client import CouchClient
from app.models.like import Like
from app.db.dao.likesDAO import LikesDAO

@pytest.fixture(scope="module")
def couch_client():
    """Fixture for initializing the CouchDB client."""
    client = CouchClient()
    yield client
    client.delete_db("test_recipes")
    client.delete_db("test_users")
    client.delete_db("test_likes")

@pytest.fixture(scope="module")
def likes_dao(couch_client):
    """Fixture for initializing the RecipeDAO with a test database."""
    dao = LikesDAO(db_name="test_likes")
    couch_client.create_db("test_users")
    couch_client.create_db("test_recipes")
    couch_client.create_db("test_likes")
    return dao

def test_end_to_end_comment_operations(likes_dao):
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
    recipe_dao = RecipeDAO(db_name="test_recipes")
    recipe_dao.create_recipe(new_recipe)
    # Get recipe ID
    recipe = recipe_dao.get_recipe_by_name("Pancakes")
    if recipe is None:
        assert False
    recipe_id = recipe.id

    # Add like
    new_like = Like(user_id=user_id, recipe_id=recipe_id)
    assert likes_dao.create_like(new_like) is not None

    # Get like by ID
    like = likes_dao.get_like_by_id(new_like.id)
    assert like is not None
    assert like.user_id == user_id
    assert like.recipe_id == recipe_id
    assert like.id == new_like.id

    # Get like count
    like_count = likes_dao.get_like_count(recipe_id)
    assert like_count == 1

    # Get likes by user
    likes = likes_dao.get_likes_by_user(user_id)
    assert len(likes) == 1
    assert likes[0].user_id == user_id
    assert likes[0].recipe_id == recipe_id
    assert likes[0].id == new_like.id

    # Delete like
    assert likes_dao.delete_like(new_like.id) is True
    like_count = likes_dao.get_like_count(recipe_id)
    assert like_count == 0
