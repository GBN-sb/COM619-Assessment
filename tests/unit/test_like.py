import pytest
from unittest.mock import patch, MagicMock
from app.models.like import Like

def test_like_initialization():
    like = Like(id=1, user_id=2, recipe_id=3)
    assert like.id == 1
    assert like.user_id == 2
    assert like.recipe_id == 3

def test_to_dict():
    like = Like(id=1, user_id=2, recipe_id=3)
    like_dict = like.to_dict()
    assert like_dict == {'id': 1, 'user_id': 2, 'recipe_id': 3}

def test_from_dict():
    data = {'id': 1, 'user_id': 2, 'recipe_id': 3}
    like = Like.from_dict(data)
    assert like.id == 1
    assert like.user_id == 2
    assert like.recipe_id == 3

def test_from_dict_missing_fields():
    data = {'id': 1, 'user_id': 2}
    with pytest.raises(ValueError) as excinfo:
        Like.from_dict(data)
    assert "Missing required fields" in str(excinfo.value)

@patch('models.like.UserDAO')
def test_check_user_id_is_valid(mock_user_dao):
    mock_user_dao().get_user_by_id.return_value = MagicMock()
    like = Like(id=1, user_id=2, recipe_id=3)
    like._check_user_id_is_valid(2)
    mock_user_dao().get_user_by_id.assert_called_once_with(2)

@patch('models.like.UserDAO')
def test_check_user_id_is_valid_user_not_found(mock_user_dao):
    mock_user_dao().get_user_by_id.return_value = None
    like = Like(id=1, user_id=2, recipe_id=3)
    with pytest.raises(ValueError) as excinfo:
        like._check_user_id_is_valid(2)
    assert "User not found." in str(excinfo.value)

@patch('models.like.RecipeDAO')
def test_check_recipe_id_is_valid(mock_recipe_dao):
    mock_recipe_dao().get_recipe_by_id.return_value = MagicMock()
    like = Like(id=1, user_id=2, recipe_id=3)
    like._check_recipe_id_is_valid(3)
    mock_recipe_dao().get_recipe_by_id.assert_called_once_with(3)

@patch('models.like.RecipeDAO')
def test_check_recipe_id_is_valid_recipe_not_found(mock_recipe_dao):
    mock_recipe_dao().get_recipe_by_id.return_value = None
    like = Like(id=1, user_id=2, recipe_id=3)
    with pytest.raises(ValueError) as excinfo:
        like._check_recipe_id_is_valid(3)
    assert "Recipe not found." in str(excinfo.value)