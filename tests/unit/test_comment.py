import pytest
from datetime import datetime
from app.models.comment import Comment
from unittest.mock import patch

def test_comment_creation():
    comment = Comment(
        user_id=123,
        post_id=456,
        content="Hello, world!",
        created_at=datetime.now()
    )
    assert comment.user_id == 123
    assert comment.post_id == 456
    assert comment.content == "Hello, world!"
    assert comment.created_at is not None
    assert isinstance(comment.created_at, datetime)

def test_comment_to_dict():
    comment = Comment(
        user_id=123,
        post_id=456,
        content="Hello, world!",
        created_at=datetime.now()
    )
    comment_dict = comment.to_dict()
    assert comment_dict["user_id"] == 123
    assert comment_dict["post_id"] == 456
    assert comment_dict["content"] == "Hello, world!"
    assert comment_dict["created_at"] == comment.created_at

def test_comment_from_dict():
    # Reset the ID counter
    data = {
        "id": 1,
        "user_id": 123,
        "post_id": 456,
        "content": "Hello, world!",
        "created_at": datetime.now()
    }
    comment = Comment.from_dict(data)
    assert comment.id == 1
    assert comment.user_id == 123
    assert comment.post_id == 456
    assert comment.content == "Hello, world!"
    assert comment.created_at == data["created_at"]

def test_comment_from_dict_missing_fields():
    data = {
        "id": 1,
        "user_id": 123,
        "content": "Hello, world!",
        "created_at": datetime.now()
    }
    with pytest.raises(ValueError, match="Missing required fields"):
        Comment.from_dict(data)

@patch('db.dao.userDAO.UserDAO.get_user_by_id')
def test_check_user_id_is_valid(mock_get_user_by_id):
    mock_get_user_by_id.return_value = True
    comment = Comment(
        user_id=123,
        post_id=456,
        content="Hello, world!",
        created_at=datetime.now()
    )
    comment._check_user_id_is_valid(123)
    mock_get_user_by_id.assert_called_once_with(123)

@patch('db.dao.userDAO.UserDAO.get_user_by_id')
def test_check_user_id_is_invalid(mock_get_user_by_id):
    mock_get_user_by_id.return_value = None
    comment = Comment(
        user_id=123,
        post_id=456,
        content="Hello, world!",
        created_at=datetime.now()
    )
    with pytest.raises(ValueError, match="User not found."):
        comment._check_user_id_is_valid(123)

@patch('db.dao.recipeDAO.RecipeDAO.get_recipe_by_id')
def test_check_recipe_id_is_valid(mock_get_recipe_by_id):
    mock_get_recipe_by_id.return_value = True
    comment = Comment(
        user_id=123,
        post_id=456,
        content="Hello, world!",
        created_at=datetime.now()
    )
    comment._check_recipe_id_is_valid(456)
    mock_get_recipe_by_id.assert_called_once_with(456)

@patch('db.dao.recipeDAO.RecipeDAO.get_recipe_by_id')
def test_check_recipe_id_is_invalid(mock_get_recipe_by_id):
    mock_get_recipe_by_id.return_value = None
    comment = Comment(
        user_id=123,
        post_id=456,
        content="Hello, world!",
        created_at=datetime.now()
    )
    with pytest.raises(ValueError, match="Recipe not found."):
        comment._check_recipe_id_is_valid(456)
