import pytest
import streamlit as st
from unittest.mock import MagicMock
from app.app import login_page, signup_page
from time import sleep
from app.db.dao.userDAO import UserDAO
from app.models.user import User
from app.db.couch_client import CouchClient
import os
import dotenv

dotenv.load_dotenv()
RUN_ENV = os.getenv('RUN_ENV')

def get_dao(db_base_name):
    print(RUN_ENV)
    if RUN_ENV == "1":
        db_name=f"{db_base_name}"
        return db_name
    if RUN_ENV == "2":
        db_name=f"test_{db_base_name}"
        return db_name
    if RUN_ENV == "3":
        db_name=f"dev_{db_base_name}"
        return db_name

@pytest.fixture(scope="module")
def couch_client():
    """Fixture for initializing the CouchDB client."""
    client = CouchClient()
    yield client  # Provide the fixture to the test
    # Teardown: Cleanup after tests
    client.delete_db(get_dao("users"))

@pytest.fixture(scope="module")
def user_dao(couch_client):
    """Fixture for initializing the UserDAO with a test database."""
    dao = UserDAO(db_name=get_dao("users"))
    couch_client.create_db(get_dao("users"))
    return dao

# Fixture to mock Streamlit components and session state
@pytest.fixture
def setup_streamlit_mocks(mocker):
    # Mock session state
    st.session_state["logged_in"] = False
    st.session_state["guest"] = False
    st.session_state["admin"] = False
    st.session_state["login_page"] = False
    st.session_state["sign_up"] = False

    # Mock Streamlit components
    mocker.patch("streamlit.text_input", return_value="username")  # Default username for testing
    mocker.patch("streamlit.button", return_value=True)
    mocker.patch("streamlit.success")
    mocker.patch("streamlit.error")
    mocker.patch("streamlit.switch_page")
    mocker.patch("streamlit.rerun")
    return st


def test_signup_page_success(mocker, setup_streamlit_mocks):
    """Test successful signup."""
    # Reset session state
    st.session_state.clear()
    st.session_state["sign_up"] = True
    st.session_state["login_page"] = False

    # Mock Streamlit inputs and methods
    mocker.patch("streamlit.text_input", side_effect=["newuser", "newpassword", "newpassword"])
    mock_success = mocker.patch("streamlit.success")

    # Call the signup_page function
    signup_page()

    # Assert success message is displayed
    mock_success.assert_called_once_with("Account created successfully! Please log in.")

    # Assert the user is redirected to the homepage
    mock_switch_page.assert_called_once_with("pages/Homepage.py")



def test_login_page_invalid_password(mocker, setup_streamlit_mocks, user_dao):
    """Test login with an invalid password."""
    # Set up session state
    st.session_state["logged_in"] = False
    st.session_state["guest"] = False

    # Create a mock user in the database with a valid password
    valid_user = User(name="username", email="test@example.com", password="correctpassword", bio="", profile_picture="db\\profile_pics\\no_pfp.png")
    user_dao.add_user(valid_user)

    # Mock Streamlit inputs for username and incorrect password
    mocker.patch("streamlit.text_input", side_effect=["username", "wrongpassword"])

    # Mock error display
    mock_error = mocker.patch("streamlit.error")

    # Simulate button interaction
    mocker.patch("streamlit.button", side_effect=[True, False, False])  # Simulate "Log In" button click

    # Call the login_page function
    login_page()

    # Verify the error message for incorrect password
    mock_error.assert_called_once_with("Incorrect password. Please try again.")

    # Verify that the user session state was not updated
    assert not st.session_state["logged_in"], "User should not be logged in with incorrect password."
    assert not st.session_state["guest"], "Guest session should not be active."



def test_login_page_username_not_found(mocker, setup_streamlit_mocks):
    """Test login with a username not found."""
    st.session_state["logged_in"] = False
    st.session_state["guest"] = False

    # Mock user input with non-existent username
    mocker.patch("streamlit.text_input", side_effect=["nonexistentuser", "password"])

    # Mock login button click
    login_page()

    # Check that an error message is displayed for the username not found
    st.error.assert_called_once_with("Username not found. Please try again.")


def test_signup_page_success(mocker, setup_streamlit_mocks, user_dao):
    """Test successful signup."""
    # Set session state to show the signup page
    st.session_state["sign_up"] = True
    st.session_state["login_page"] = False

    # Mock Streamlit input fields and button interactions
    mocker.patch("streamlit.text_input", side_effect=["newuser12", "newuser12@example.com", "newpassword", "newpassword"])
    mock_button = mocker.patch("streamlit.button", side_effect=[True, False])  # Simulate clicking "Sign Up"

    # Mock success and error calls
    mock_success = mocker.patch("streamlit.success")
    mock_error = mocker.patch("streamlit.error")

    # Call the signup_page function
    signup_page()

    # Verify the account creation process
    new_user = user_dao.get_user_by_username("newuser12")
    if mock_button.call_count > 0:
        assert new_user is not None, "User should have been added to the database."
        assert new_user.email == "newuser12@example.com", "User email should match input."
        assert new_user.name == "newuser12", "Username should match input."
        assert User.verify_password("newpassword", new_user.password_hash), "Password should be correctly hashed and stored."
        mock_success.assert_called_once_with("Account created successfully! Please log in.")
    else:
        mock_error.assert_not_called()


def test_signup_page_email_taken(mocker, setup_streamlit_mocks, user_dao):
    """Test signup with a email that already exists."""
    # Set up session state
    st.session_state["sign_up"] = True
    st.session_state["login_page"] = False

    # Add a user to the database with the username to simulate a taken username
    existing_user = User(
        name="username", 
        email="existing@example.com", 
        password="password", 
        bio="", 
        profile_picture="db\\profile_pics\\no_pfp.png"
    )
    user_dao.add_user(existing_user)

    # Mock Streamlit text input for a new signup attempt with the same username
    mocker.patch("streamlit.text_input", side_effect=["username", "existing@example.com", "newpassword", "newpassword"])

    # Mock error handling
    mock_error = mocker.patch("streamlit.error")

    # Simulate the signup page interaction
    signup_page()

    # Verify that the error is triggered for the username being taken
    mock_error.assert_called_once_with("This email is already associated with an account. Please log in.")



def test_signup_page_passwords_do_not_match(mocker, setup_streamlit_mocks):
    """Test signup with mismatched passwords."""
    # Initialize session state for the signup page
    st.session_state["login_page"] = False
    st.session_state["sign_up"] = True

    # Mock user inputs for username, email, and mismatched passwords
    mocker.patch("streamlit.text_input", side_effect=["newuser123", "user@example.com", "password1", "password2"])
    mocker.patch("streamlit.button", return_value=True)  # Simulate the "Sign Up" button click

    # Mock error handling
    mock_error = mocker.patch("streamlit.error")

    # Call the signup_page function
    signup_page()

    # Verify that the mismatched passwords trigger an error message
    mock_error.assert_called_once_with("Passwords do not match. Please try again.")



def test_continue_as_guest(mocker, setup_streamlit_mocks):
    """Test login as guest."""
    st.session_state["logged_in"] = False
    st.session_state["guest"] = False

    # Mock guest login
    mocker.patch("streamlit.text_input", return_value="")
    mocker.patch("streamlit.button", return_value=True)

    login_page()

    # Check if the user is logged in as a guest and redirected
    st.success.assert_called_once_with("Logged in as Guest.")
    st.switch_page.assert_called_once_with("pages/Homepage.py")

