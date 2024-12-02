import unittest
from unittest.mock import MagicMock, patch
from db.dao.commentsDAO import CommentsDAO
from models.comment import Comment

class TestCommentsDAO(unittest.TestCase):

    @patch('db.dao.commentsDAO.CouchClient')
    def test_create_comment(self, MockCouchClient):
        mock_client = MockCouchClient.return_value
        mock_client.create_doc.return_value = ("comment123", True, "Created successfully")

        comments_dao = CommentsDAO("comments_db")
        comment = Comment("1", "user123", "post123", "Test comment", "2024-12-02T12:00:00")
        response = comments_dao.create_comment(comment)

        mock_client.create_doc.assert_called_once()
        self.assertEqual(response, ("comment123", True, "Created successfully"))

    @patch('db.dao.commentsDAO.CouchClient')
    def test_get_comment_by_id(self, MockCouchClient):
        mock_client = MockCouchClient.return_value
        mock_client.get_doc.return_value = {
            "comment_id": "comment123",
            "user_id": "user123",
            "post_id": "post123",
            "content": "Test comment",
            "created_at": "2024-12-02T12:00:00"
        }

        comments_dao = CommentsDAO("comments_db")
        comment = comments_dao.get_comment_by_id("comment123")

        if comment is None:
            self.fail("Comment not found.")

        mock_client.get_doc.assert_called_once_with("comments_db", "comment123")
        self.assertEqual(comment.content, "Test comment")

    @patch('db.dao.commentsDAO.CouchClient')
    def test_delete_comment(self, MockCouchClient):
        mock_client = MockCouchClient.return_value
        mock_client.delete_doc.return_value = True

        comments_dao = CommentsDAO("comments_db")
        result = comments_dao.delete_comment("comment123")

        mock_client.delete_doc.assert_called_once_with("comments_db", "comment123")
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
