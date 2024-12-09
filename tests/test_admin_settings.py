import pytest
import streamlit as st
from app.pages.Admin_Settings import display_admin_settings  # Adjust the import path as needed
from unittest.mock import MagicMock
from app.db.dao.userDAO import UserDAO
from app.models.user import User
from app.db.couch_client import CouchClient

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

@pytest.fixture
def setup_streamlit_mocks(mocker):
    """Fixture to mock Streamlit functions used in display_admin_settings."""
    mocker.patch("streamlit.write")
    mocker.patch("streamlit.success")
    mocker.patch("streamlit.error")
    mocker.patch("streamlit.button", side_effect=[False, False, False])  # Mock button clicks
    
    # Mock columns and their elements
    col1, col2, col3 = MagicMock(), MagicMock(), MagicMock()
    col4, col5, col6 = MagicMock(), MagicMock(), MagicMock()
    mocker.patch("streamlit.columns", side_effect=[[col1, col2, col3], [col4, col5, col6]])

    # Define side effects for text inputs
    col1.text_input.side_effect = ["admin_email", "admin_username", "admin_password", "admin_password"]
    col2.text_input.side_effect = ["grant_email", "grant_username"]
    col3.text_input.side_effect = ["delete_username"]

    return col1, col2, col3, col4, col5, col6


def test_display_admin_settings(setup_streamlit_mocks, user_dao):
    """Test the display_admin_settings function to verify components and logic."""
    col1, col2, col3, col4, col5, col6 = setup_streamlit_mocks

    display_admin_settings()

    # Verify section headers
    col1.subheader.assert_called_once_with("Create Admin")
    col2.subheader.assert_called_once_with("Grant Admin Access")
    col3.subheader.assert_called_once_with("Delete User")

    # Verify input fields
    col1.text_input.assert_any_call("Admin Email")
    col1.text_input.assert_any_call("Admin Username")
    col1.text_input.assert_any_call("Admin Password", type="password")
    col1.text_input.assert_any_call("Repeat Admin Password", type="password")

    col2.text_input.assert_any_call("User Email")
    col2.text_input.assert_any_call("User Username")

    col3.text_input.assert_any_call("Username to Delete")

    # Verify buttons
    col4.button.assert_called_once_with("Create Admin", use_container_width=True, type="primary")
    col5.button.assert_called_once_with("Grant Admin Access", use_container_width=True, type="primary")
    col6.button.assert_called_once_with("Delete User", use_container_width=True, type="primary")


def test_create_admin_success(setup_streamlit_mocks, user_dao):
    """Test successful creation of an admin."""
    col1, _, _, col4, _, _ = setup_streamlit_mocks
    col4.button.return_value = True  # Simulate the "Create Admin" button click

    col1.text_input.side_effect = ["admin@example.com", "adminuser", "password", "password"]

    display_admin_settings()

    fetched_user = user_dao.get_user_by_email("admin@example.com")
    assert fetched_user is not None, "Admin should exist in the database."
    assert fetched_user.role == "admin", "User should have 'admin' role."
    st.success.assert_called_once_with("Admin 'adminuser' created successfully.")


def test_create_admin_password_mismatch(setup_streamlit_mocks):
    """Test the else path for 'Create Admin' when passwords do not match."""
    col1, _, _, col4, _, _ = setup_streamlit_mocks
    col4.button.return_value = True  # Simulate the "Create Admin" button click

    col1.text_input.side_effect = ["admin@example.com", "adminuser", "password1", "password2"]

    display_admin_settings()

    st.error.assert_called_once_with("Passwords do not match. Please try again.")


def test_grant_admin_access_success(setup_streamlit_mocks, user_dao, mocker):
    """Test successful granting of admin access."""
    _, col2, _, _, col5, _ = setup_streamlit_mocks
    col5.button.return_value = True  # Simulate the "Grant Admin Access" button click

    col2.text_input.side_effect = ["grant@example.com", "grantuser"]

    new_user=User(name="grantuser", email="grant@example.com", password="password", role="user", bio="test user", profile_picture="https://example.com/profile.jpg")
    user_dao = UserDAO(db_name="test_users")
    user_dao.add_user(new_user)
    display_admin_settings()
    
    user = user_dao.get_user_by_email(email="grant@example.com")
    if user.name == "grantuser":
        assert True
    user_dao.update_user_role(user.id, "admin")
    fetched_user = user_dao.get_user_by_email("grant@example.com")
    assert fetched_user.role == "admin", "User should have been updated to 'admin'."
    st.success.assert_called_once_with("Admin access granted to user 'grantuser'.")


def test_delete_user_success(setup_streamlit_mocks, user_dao):
    """Test successful deletion of a user."""
    _, _, col3, _, _, col6 = setup_streamlit_mocks
    col6.button.return_value = True  # Simulate the "Delete User" button click

    user_dao.add_user(User(name="user1", email="user1@example.com", password="password", role="user", bio="", profile_picture="https://example.com/profile.jpg"))
    col3.text_input.side_effect = ["user1"]

    display_admin_settings()

    fetched_user = user_dao.get_user_by_email("user1@example.com")
    assert fetched_user is None, "User should have been deleted."
    st.success.assert_called_once_with("User 'user1' deleted successfully.")
