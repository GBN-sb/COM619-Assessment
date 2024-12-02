import unittest
from unittest.mock import MagicMock, patch
from db.dao.userDAO import UserDAO
from models.user import User

class TestUserDAO(unittest.TestCase):

    @patch('db.dao.userDAO.CouchClient')
    def test_create_user(self, MockCouchClient):
        # Mock the CouchClient instance
        mock_client = MockCouchClient.return_value
        
        # Scenario 1: Successful creation
        mock_client.create_doc.return_value = ("user123", True, "Created successfully")
        mock_client.query_documents.return_value = []  # No existing user with the same email

        user_dao = UserDAO()
        user = User(
            name="John Doe",
            email="john.doe@example.com",
            password="password123",
            profile_picture="profile.jpg",
            role="user",
            bio="This is John's bio."
        )
        response = user_dao.create_user(user)

        mock_client.create_doc.assert_called_once_with("users", user.to_dict())
        self.assertEqual(response, ("user123", True, "Created successfully"))

        # Scenario 2: User with the same email already exists
        mock_client.create_doc.reset_mock()
        mock_client.query_documents.return_value = [
            {
                "id": "user123",
                "name": "John Doe",
                "email": "john.doe@example.com",
                "passwordHash": "hashed_password",
                "profilePicture": "profile.jpg",
                "role": "user",
                "bio": "This is John's bio."
            }
        ]
        
        with self.assertRaises(ValueError) as context:
            user_dao.create_user(user)

        self.assertEqual(str(context.exception), "A user with this email already exists.")
        mock_client.create_doc.assert_not_called()
        mock_client.query_documents.assert_called_with(
            "users", {"selector": {"email": "john.doe@example.com"}}
        )


    @patch('db.dao.userDAO.CouchClient')
    def test_get_user_by_id(self, MockCouchClient):
        mock_client = MockCouchClient.return_value
        mock_client.get_doc.return_value = {
            "id": 1,
            "name": "John Doe",
            "email": "john.doe@example.com",
            "passwordHash": "hashed_password",
            "profilePicture": "profile.jpg",
            "role": "user",
            "bio": "This is John's bio."
        }

        user_dao = UserDAO()
        user = user_dao.get_user_by_id(1)

        if user is None:
            self.fail("User not found.")

        mock_client.get_doc.assert_called_once_with("users", 1)
        self.assertEqual(user.name, "John Doe")
        self.assertEqual(user.email, "john.doe@example.com")
        self.assertEqual(user.role, "user")
        self.assertEqual(user.bio, "This is John's bio.")

    @patch('db.dao.userDAO.CouchClient')
    def test_get_user_by_email(self, MockCouchClient):
        mock_client = MockCouchClient.return_value
        mock_client.query_documents.return_value = [
            {
                "id": 1,
                "name": "John Doe",
                "email": "john.doe@example.com",
                "passwordHash": "hashed_password",
                "profilePicture": "profile.jpg",
                "role": "user",
                "bio": "This is John's bio."
            }
        ]

        user_dao = UserDAO()
        user = user_dao.get_user_by_email("john.doe@example.com")

        if user is None:
            self.fail("User not found.")

        mock_client.query_documents.assert_called_once_with(
            "users", {"selector": {"email": "john.doe@example.com"}}
        )
        self.assertEqual(user.name, "John Doe")
        self.assertEqual(user.email, "john.doe@example.com")
        self.assertEqual(user.role, "user")
        self.assertEqual(user.bio, "This is John's bio.")


    @patch('db.dao.userDAO.CouchClient')
    def test_update_user(self, MockCouchClient):
        mock_client = MockCouchClient.return_value
        mock_client.update_doc.return_value = True

        user_dao = UserDAO()
        updated_data = {"bio": "Updated bio"}
        result = user_dao.update_user(1, updated_data)

        mock_client.update_doc.assert_called_once_with("users", 1, updated_data)
        self.assertTrue(result)

    @patch('db.dao.userDAO.CouchClient')
    def test_delete_user(self, MockCouchClient):
        mock_client = MockCouchClient.return_value
        mock_client.delete_doc.return_value = True

        user_dao = UserDAO()
        result = user_dao.delete_user(1)

        mock_client.delete_doc.assert_called_once_with("users", 1)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
