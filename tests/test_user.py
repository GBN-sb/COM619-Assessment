import unittest
from models.user import User

class TestUserModel(unittest.TestCase):

    def test_password_hashing(self):
        user = User(name="Test", email="test@test.com", password="password123")
        self.assertTrue(User.verify_password("password123", user.password_hash))
        self.assertFalse(User.verify_password("wrongpassword", user.password_hash))

    def test_to_dict(self):
        user = User(name="Test", email="test@test.com", password="password123", bio="A test bio")
        user_dict = user.to_dict()
        self.assertEqual(user_dict["name"], "Test")
        self.assertEqual(user_dict["email"], "test@test.com")
        self.assertEqual(user_dict["bio"], "A test bio")

    def test_from_dict(self):
        data = {
            "id": 1,
            "name": "Test",
            "email": "test@test.com",
            "passwordHash": "hash",
            "profilePicture": "profile.jpg",
            "role": "user",
            "bio": "A test bio"
        }
        user = User.from_dict(data)
        self.assertEqual(user.name, "Test")
        self.assertEqual(user.email, "test@test.com")

if __name__ == '__main__':
    unittest.main()
