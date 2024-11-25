import pytest
import streamlit as st
from unittest.mock import MagicMock
from app.app import login_page, signup_page
from time import sleep

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



def test_login_page_invalid_password(mocker, setup_streamlit_mocks):
    """Test login with an invalid password."""
    st.session_state["logged_in"] = False
    st.session_state["guest"] = False

    # Mock user input with incorrect password
    mocker.patch("streamlit.text_input", side_effect=["username", "wrongpassword"])

    # Mock login button click
    login_page()

    # Check that an error message is displayed for the wrong password
    st.error.assert_called_once_with("Incorrect password. Please try again.")


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


def test_signup_page_success(mocker, setup_streamlit_mocks):
    """Test successful signup."""
    st.session_state["sign_up"] = True
    st.session_state["login_page"] = False

    # Mock signup form inputs
    mocker.patch("streamlit.text_input", side_effect=["newuser12", "newpassword", "newpassword"])

    # Mock signup button click
    signup_page()

    # Check that the account is created and the user is directed to the homepage
    st.success.assert_called_once_with("Account created successfully! Please log in.")


def test_signup_page_username_taken(mocker, setup_streamlit_mocks):
    """Test signup with a username that already exists."""
    st.session_state["sign_up"] = True
    st.session_state["login_page"] = False

    # Mock signup form inputs
    mocker.patch("streamlit.text_input", side_effect=["username", "newpassword", "newpassword"])

    # Mock signup button click
    signup_page()

    # Check that an error message is displayed for the taken username
    st.error.assert_called_once_with("This username is already taken. Please choose a different one.")


def test_signup_page_passwords_do_not_match(mocker, setup_streamlit_mocks):
    """Test signup with mismatched passwords."""
    st.session_state["sign_up"] = True
    st.session_state["login_page"] = False

    # Mock signup form inputs with mismatched passwords
    mocker.patch("streamlit.text_input", side_effect=["newuser123", "password1", "password2"])
    mocker.patch("streamlit.button", return_value=True)  # Simulate button click

    # Call the signup_page function
    signup_page()

    # Check that an error message is displayed for the mismatched passwords
    st.error.assert_called_once_with("Passwords do not match. Please try again.")



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

