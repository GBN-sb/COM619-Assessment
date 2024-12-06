import pytest
from db.dao.userDAO import UserDAO
from models.user import User
from db.dao.recipeDAO import RecipeDAO
from models.recipe import Recipe
from db.couch_client import CouchClient
from db.dao.commentsDAO import CommentsDAO
from models.comment import Comment
from datetime import datetime

@pytest.fixture(scope="module")
def couch_client():
    """Fixture for initializing the CouchDB client."""
    client = CouchClient()
    yield client
    client.delete_db("test_recipes")
    client.delete_db("test_users")
    client.delete_db("test_comments")

@pytest.fixture(scope="module")
def comment_dao(couch_client):
    """Fixture for initializing the RecipeDAO with a test database."""
    dao = CommentsDAO(db_name="test_comments")
    couch_client.create_db("test_users")
    couch_client.create_db("test_recipes")
    couch_client.create_db("test_comments")
    return dao

def test_end_to_end_comment_operations(comment_dao):
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

    # Add comment
    json_date = datetime.now().isoformat()
    new_comment = Comment(user_id=user_id, post_id=recipe_id, content="Hello, world!", created_at=json_date)
    assert comment_dao.create_comment(new_comment) is not None

    # Get recipe by title
    fetched_recipe = recipe_dao.get_recipe_by_name("Pancakes")
    assert fetched_recipe is not None
    assert fetched_recipe.title == "Pancakes"
    assert fetched_recipe.description == "Delicious pancakes"

    # Get comment by user ID
    fetched_comment = comment_dao.get_comments_by_user_id(user_id)[0]
    assert fetched_comment is not None
    assert fetched_comment.user_id == user_id
    assert fetched_comment.post_id == recipe_id
    assert fetched_comment.content == "Hello, world!"

    # Update recipe
    fetched_recipe.description = "Some new description"
    assert recipe_dao.update_recipe(fetched_recipe) is not None
    updated_recipe = recipe_dao.get_recipe_by_name("Pancakes")
    if updated_recipe is None:
        assert False
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

    # Delete comment
    assert comment_dao.delete_comment(new_comment.id) is True
    all_comments = comment_dao.get_comments()
    assert len(all_comments) == 0

