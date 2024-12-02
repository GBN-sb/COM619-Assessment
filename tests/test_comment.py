import unittest
from unittest.mock import patch, MagicMock
from models.comment import Comment
from db.dao.userDAO import UserDAO
from db.dao.recipeDAO import RecipeDAO

class TestCommentModel(unittest.TestCase):

    @patch('db.dao.userDAO.UserDAO.get_user_by_id')
    def test_check_user_id_is_valid(self, mock_get_user_by_id):
        # Mock a valid user
        mock_get_user_by_id.return_value = {"id": "123", "name": "Test User"}
        
        comment = Comment("1", "123", "456", "Test Content", "2024-12-02T12:00:00")
        try:
            comment._check_user_id_is_valid("123")
        except ValueError:
            self.fail("_check_user_id_is_valid raised ValueError unexpectedly!")
        
        # Mock an invalid user
        mock_get_user_by_id.return_value = None
        with self.assertRaises(ValueError):
            comment._check_user_id_is_valid("999")

    @patch('db.dao.recipeDAO.RecipeDAO.get_recipe_by_id')
    def test_check_recipe_id_is_valid(self, mock_get_recipe_by_id):
        # Mock a valid recipe
        mock_get_recipe_by_id.return_value = {"id": "456", "title": "Test Recipe"}
        
        comment = Comment("1", "123", "456", "Test Content", "2024-12-02T12:00:00")
        try:
            comment._check_recipe_id_is_valid("456")
        except ValueError:
            self.fail("_check_recipe_id_is_valid raised ValueError unexpectedly!")
        
        # Mock an invalid recipe
        mock_get_recipe_by_id.return_value = None
        with self.assertRaises(ValueError):
            comment._check_recipe_id_is_valid("999")

    def test_to_dict(self):
        comment = Comment("1", "123", "456", "Test Content", "2024-12-02T12:00:00")
        expected_dict = {
            'comment_id': "1",
            'user_id': "123",
            'post_id': "456",
            'content': "Test Content",
            'created_at': "2024-12-02T12:00:00"
        }
        self.assertEqual(comment.to_dict(), expected_dict)

    def test_from_dict(self):
        data = {
            'comment_id': "1",
            'user_id': "123",
            'post_id': "456",
            'content': "Test Content",
            'created_at': "2024-12-02T12:00:00"
        }
        comment = Comment.from_dict(data)
        self.assertEqual(comment.comment_id, "1")
        self.assertEqual(comment.user_id, "123")
        self.assertEqual(comment.post_id, "456")
        self.assertEqual(comment.content, "Test Content")
        self.assertEqual(comment.created_at, "2024-12-02T12:00:00")

        with self.assertRaises(ValueError):
            Comment.from_dict({})

if __name__ == '__main__':
    unittest.main()
