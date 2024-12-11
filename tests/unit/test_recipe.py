import pytest
from datetime import datetime
from app.models.recipe import Recipe

def test_recipe_creation():
    recipe = Recipe(
        title="Pancakes",
        description="A delicious breakfast treat.",
        ingredients=["flour", "milk", "eggs"],
        instructions="Mix ingredients and cook on griddle.",
        picture_location="pancakes.jpg",
        creator_id="123"
    )
    assert recipe.title == "Pancakes"
    assert recipe.description == "A delicious breakfast treat."
    assert recipe.ingredients == ["flour", "milk", "eggs"]
    assert recipe.instructions == "Mix ingredients and cook on griddle."
    assert recipe.picture_location == "pancakes.jpg"
    assert recipe.creator_id == "123"
    assert isinstance(recipe.created_at, datetime)

def test_to_dict():
    recipe = Recipe(
        title="Pancakes",
        description="A delicious breakfast treat.",
        ingredients=["flour", "milk", "eggs"],
        instructions="Mix ingredients and cook on griddle.",
        picture_location="pancakes.jpg",
        creator_id="123"
    )
    recipe_dict = recipe.to_dict()
    assert recipe_dict["title"] == "Pancakes"
    assert recipe_dict["description"] == "A delicious breakfast treat."
    assert recipe_dict["ingredients"] == ["flour", "milk", "eggs"]
    assert recipe_dict["instructions"] == "Mix ingredients and cook on griddle."
    assert recipe_dict["pictureLocation"] == "pancakes.jpg"
    assert recipe_dict["creatorId"] == "123"
    assert "createdAt" in recipe_dict

def test_from_dict():
    data = {
        "id": 1,
        "title": "Pancakes",
        "description": "A delicious breakfast treat.",
        "ingredients": ["flour", "milk", "eggs"],
        "instructions": "Mix ingredients and cook on griddle.",
        "pictureLocation": "pancakes.jpg",
        "creatorId": "123",
        "createdAt": datetime.now().isoformat()
    }
    recipe = Recipe.from_dict(data)
    assert recipe.id == 1
    assert recipe.title == "Pancakes"
    assert recipe.description == "A delicious breakfast treat."
    assert recipe.ingredients == ["flour", "milk", "eggs"]
    assert recipe.instructions == "Mix ingredients and cook on griddle."
    assert recipe.picture_location == "pancakes.jpg"
    assert recipe.creator_id == "123"
    assert isinstance(recipe.created_at, datetime)

def test_from_dict_missing_fields():
    data = {
        "id": 1,
        "title": "Pancakes",
        "description": "A delicious breakfast treat.",
        "ingredients": ["flour", "milk", "eggs"],
        "instructions": "Mix ingredients and cook on griddle.",
        "pictureLocation": "pancakes.jpg",
        "creatorId": "123"
    }
    with pytest.raises(ValueError):
        Recipe.from_dict(data)

def test_verify_creator():
    recipe_data = {
        "id": 1,
        "title": "Pancakes",
        "description": "A delicious breakfast treat.",
        "ingredients": ["flour", "milk", "eggs"],
        "instructions": "Mix ingredients and cook on griddle.",
        "pictureLocation": "pancakes.jpg",
        "creatorId": "123",
        "createdAt": datetime.now().isoformat()
    }
    assert Recipe.verify_creator("123", recipe_data) == True
    assert Recipe.verify_creator("124", recipe_data) == False