import unittest
from models.recipe import Recipe

class TestRecipeModel(unittest.TestCase):

    def test_to_dict(self):
        recipe = Recipe(
            title="Test Recipe",
            description="Description here",
            ingredients=["ing1", "ing2"],
            instructions="Steps",
            picture_location="image.jpg",
            creator_id="creator123"
        )
        recipe_dict = recipe.to_dict()
        self.assertEqual(recipe_dict["title"], "Test Recipe")
        self.assertEqual(recipe_dict["description"], "Description here")
        self.assertEqual(recipe_dict["ingredients"], ["ing1", "ing2"])

    def test_from_dict(self):
        data = {
            "id": 1,
            "title": "Test Recipe",
            "description": "Description here",
            "ingredients": ["ing1", "ing2"],
            "instructions": "Steps",
            "pictureLocation": "image.jpg",
            "creatorId": "creator123",
            "createdAt": "2024-12-02T12:00:00"
        }
        recipe = Recipe.from_dict(data)
        self.assertEqual(recipe.title, "Test Recipe")
        self.assertEqual(recipe.creator_id, "creator123")
        self.assertEqual(recipe.created_at.isoformat(), "2024-12-02T12:00:00")

if __name__ == '__main__':
    unittest.main()
