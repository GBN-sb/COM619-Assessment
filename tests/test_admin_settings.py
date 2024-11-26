import pytest
import streamlit as st
from app.pages.Admin_Settings import display_admin_settings  # Adjust the import path as needed
from unittest.mock import MagicMock


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


def test_display_admin_settings(setup_streamlit_mocks):
    """Test the display_admin_settings function to verify components and logic."""
    col1, col2, col3, col4, col5, col6 = setup_streamlit_mocks

    display_admin_settings()

    # Verify each section header
    col1.subheader.assert_called_once_with("Create Admin")
    col2.subheader.assert_called_once_with("Grant Admin Access")
    col3.subheader.assert_called_once_with("Delete User")

    # Verify text input fields for "Create Admin"
    col1.text_input.assert_any_call("Admin Email")
    col1.text_input.assert_any_call("Admin Username")
    col1.text_input.assert_any_call("Admin Password", type="password")
    col1.text_input.assert_any_call("Repeat Admin Password", type="password")

    # Verify text input fields for "Grant Admin Access"
    col2.text_input.assert_any_call("User Email")
    col2.text_input.assert_any_call("User Username")

    # Verify text input fields for "Delete User"
    col3.text_input.assert_any_call("Username to Delete")

    # Verify buttons
    col4.button.assert_called_once_with("Create Admin", use_container_width=True, type="primary")
    col5.button.assert_called_once_with("Grant Admin Access", use_container_width=True, type="primary")
    col6.button.assert_called_once_with("Delete User", use_container_width=True, type="primary")

    # Verify success is called three times because there should be 3 successes
    assert st.success.call_count == 3

def test_create_admin_else_path(setup_streamlit_mocks):
    """Test the else path for 'Create Admin' when passwords do not match."""
    col1, _, _, col4, _, _ = setup_streamlit_mocks
    col4.button.return_value = True  # Simulate the "Create Admin" button being clicked

    # Simulate mismatched passwords
    col1.text_input.side_effect = ["admin_email", "admin_username", "password1", "password2"]

    display_admin_settings()

    # Verify error message is shown
    st.error.assert_called_once_with("Passwords do not match. Please try again.")


def test_grant_admin_access_else_path(setup_streamlit_mocks):
    """Test the else path for 'Grant Admin Access' when email or username is missing."""
    _, col2, _, _, col5, _ = setup_streamlit_mocks
    col5.button.return_value = True  # Simulate the "Grant Admin Access" button being clicked

    # Simulate missing email or username
    col2.text_input.side_effect = ["", ""]  # Empty email and username fields

    display_admin_settings()

    # Verify error message is shown
    st.error.assert_called_once_with("Please provide both email and username.")


def test_delete_user_else_path(setup_streamlit_mocks):
    """Test the else path for 'Delete User' when username is missing."""
    _, _, col3, _, _, col6 = setup_streamlit_mocks
    col6.button.return_value = True  # Simulate the "Delete User" button being clicked

    # Simulate missing username
    col3.text_input.side_effect = [""]  # Empty username field

    display_admin_settings()

    # Verify error message is shown
    st.error.assert_called_once_with("Please provide a username to delete.")

