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
