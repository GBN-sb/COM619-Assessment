import pytest
from db.dao.userDAO import UserDAO
from models.user import User
from db.couch_client import CouchClient

@pytest.fixture(scope="module")
def couch_client():
    """Fixture for initializing the CouchDB client."""
    client = CouchClient()
    yield client  # Provide the fixture to the test
    # Teardown: Cleanup after tests
    client.delete_db("test_users")

@pytest.fixture(scope="module")
def user_dao(couch_client):
    """Fixture for initializing the UserDAO with a test database."""
    dao = UserDAO(db_name="test_users")
    couch_client.create_db("test_users")
    return dao

def test_end_to_end_user_operations(user_dao):
    """End-to-end test for UserDAO operations."""
    # Add user
    new_user = User(name="John", email="JohnDoe@example.com", password="password123", role="user", bio="Hello, World!", profile_picture="https://example.com/profile.jpg")
    assert user_dao.add_user(new_user) is True

    # Get user by email
    fetched_user = user_dao.get_user_by_email("JohnDoe@example.com")
    print(fetched_user.email)
    print(fetched_user.id)
    
    assert fetched_user is not None
    assert fetched_user.name == "John"
    assert fetched_user.email == "JohnDoe@example.com"

    # Update user role
    assert user_dao.update_user_role(fetched_user.id, "admin") is True
    updated_user = user_dao.get_user_by_email("JohnDoe@example.com")
    assert updated_user.role == "admin"

    # Get all users
    all_users = user_dao.get_all_users()

    assert len(all_users) == 1

    # Delete user
    assert user_dao.delete_user(fetched_user.id) is True
    all_users = user_dao.get_all_users()
    assert len(all_users) == 0
