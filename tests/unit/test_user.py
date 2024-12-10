import pytest
from app.models.user import User
import bcrypt

def test_user_creation():
    user = User(
        name="John",
        email="john@doe.com",
        password="password123",
        role="admin",
        bio="Hello, world!"
    )
    assert user.name == "John"
    assert user.email == "john@doe.com"
    assert user.role == "admin"
    assert user.bio == "Hello, world!"
    assert user.profile_picture is None
    assert bcrypt.checkpw("password123".encode('utf-8'), user.password_hash.encode('utf-8'))

def test_password_hashing():
    password = "password123"
    hashed_password = User.hash_password(password)
    assert bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def test_password_verification():
    password = "password123"
    hashed_password = User.hash_password(password)
    assert User.verify_password(password, hashed_password)
    assert not User.verify_password("wrongpassword", hashed_password)

def test_user_validation():
    with pytest.raises(ValueError):
        User(name="", email="john@doe.com", password="password123")
    with pytest.raises(ValueError):
        User(name="John", email="invalidemail", password="password123")
    with pytest.raises(ValueError):
        User(name="John", email="john@doe.com", password="")
    with pytest.raises(ValueError):
        User(name="John", email="john@doe.com", password="password123", role="invalidrole")

def test_user_to_dict():
    user = User(
        name="John",
        email="john@doe.com",
        password="password123",
        role="admin",
        bio="Hello, world!"
    )
    user_dict = user.to_dict()
    assert user_dict["name"] == "John"
    assert user_dict["email"] == "john@doe.com"
    assert user_dict["role"] == "admin"
    assert user_dict["bio"] == "Hello, world!"
    assert user_dict["profilePicture"] is None

def test_user_from_dict():
    user_data = {
        "id": 1,
        "name": "John",
        "email": "john@doe.com",
        "passwordHash": User.hash_password("password123"),
        "profilePicture": None,
        "role": "admin",
        "bio": "Hello, world!"
    }
    user = User.from_dict(user_data)
    assert user.id == 1
    assert user.name == "John"
    assert user.email == "john@doe.com"
    assert user.role == "admin"
    assert user.bio == "Hello, world!"
    assert user.profile_picture is None
    assert bcrypt.checkpw("password123".encode('utf-8'), user.password_hash.encode('utf-8'))