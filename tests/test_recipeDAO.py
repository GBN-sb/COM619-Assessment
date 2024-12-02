import unittest
from unittest.mock import MagicMock, patch
from db.dao.recipeDAO import RecipeDAO
from models.recipe import Recipe

class TestRecipeDAO(unittest.TestCase):

    @patch('db.dao.recipeDAO.CouchClient')
    def test_create_recipe(self, MockCouchClient):
        mock_client = MockCouchClient.return_value
        mock_client.create_doc.return_value = ("recipe123", True, "Created successfully")

        recipe_dao = RecipeDAO()
        recipe = Recipe(
            title="Test Recipe",
            description="Description here",
            ingredients=["ing1", "ing2"],
            instructions="Steps",
            picture_location="image.jpg",
            creator_id="creator123"
        )
        response = recipe_dao.create_recipe(recipe)

        mock_client.create_doc.assert_called_once()
        self.assertEqual(response, ("recipe123", True, "Created successfully"))

    @patch('db.dao.recipeDAO.CouchClient')
    def test_get_recipe_by_id(self, MockCouchClient):
        mock_client = MockCouchClient.return_value
        mock_client.get_doc.return_value = {
            "id": "recipe123",
            "title": "Test Recipe",
            "description": "Description here",
            "ingredients": ["ing1", "ing2"],
            "instructions": "Steps",
            "pictureLocation": "image.jpg",
            "creatorId": "creator123",
            "createdAt": "2024-12-02T12:00:00"
        }

        recipe_dao = RecipeDAO()
        recipe = recipe_dao.get_recipe_by_id("recipe123")

        if recipe is None:
            self.fail("Recipe not found.")

        mock_client.get_doc.assert_called_once_with("recipes", "recipe123")
        self.assertEqual(recipe.title, "Test Recipe")
        self.assertEqual(recipe.creator_id, "creator123")

    @patch('db.dao.recipeDAO.CouchClient')
    def test_get_recipes(self, MockCouchClient):
        mock_client = MockCouchClient.return_value
        mock_client.query_documents.return_value = [{
            "id": "recipe123",
            "title": "Test Recipe",
            "description": "Description here",
            "ingredients": ["ing1", "ing2"],
            "instructions": "Steps",
            "pictureLocation": "image.jpg",
            "creatorId": "creator123",
            "createdAt": "2024-12-02T12:00:00"
        }]

        recipe_dao = RecipeDAO()
        recipes = recipe_dao.get_recipes()

        mock_client.query_documents.assert_called_once_with("recipes", {"selector": {}})
        self.assertEqual(len(recipes), 1)
        self.assertEqual(recipes[0].title, "Test Recipe")

    @patch('db.dao.recipeDAO.CouchClient')
    def test_delete_recipe(self, MockCouchClient):
        mock_client = MockCouchClient.return_value
        mock_client.delete_doc.return_value = True

        recipe_dao = RecipeDAO()
        result = recipe_dao.delete_recipe("recipe123")

        mock_client.delete_doc.assert_called_once_with("recipes", "recipe123")
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
