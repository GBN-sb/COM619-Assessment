import pytest
import streamlit as st
from app.pages.Settings import display_settings  # Adjust the import path as needed
from unittest.mock import MagicMock
import bcrypt

@pytest.fixture
def setup_streamlit_mocks(mocker):
    """Fixture to mock streamlit functions used in display_settings."""
    # Create a valid bcrypt hash for the password
    hashed_password = bcrypt.hashpw("current_password".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    
    # Mock session state for user details
    st.session_state["user"] = MagicMock(name="TestUser", password_hash=hashed_password, email="test@example.com")
    st.session_state["user"].name = "TestUser"

    # Mock Streamlit functions
    mocker.patch("streamlit.write")
    mocker.patch("streamlit.success")
    mocker.patch("streamlit.error")
    mocker.patch("streamlit.text_input", side_effect=[
        "TestUser", "TestUser", "NewTestUser",  # Username inputs
        "current_password", "current_password", "new_password",  # Password inputs
        "test@example.com", "test@example.com", "new@example.com"  # Email inputs
    ])
    mocker.patch("streamlit.button", side_effect=[False, True, False, True, False, True])  # Buttons for update actions
    mocker.patch("streamlit.columns", return_value=[MagicMock(), MagicMock(), MagicMock()])

    return mocker


    return mocker

def test_display_settings(setup_streamlit_mocks):
    """Test the display_settings function to verify components and logic."""
    mocker = setup_streamlit_mocks
    
    # Call the function
    display_settings()

    # Verify columns creation
    st.columns.assert_called_once_with([1, 1, 1], gap="medium")

    # Verify text input calls for username section
    st.text_input.assert_any_call("Current Username")
    st.text_input.assert_any_call("Repeat Current Username")
    st.text_input.assert_any_call("New Username")

    # Verify text input calls for password section
    st.text_input.assert_any_call("Current Password", type="password")
    st.text_input.assert_any_call("Repeat Current Password", type="password")
    st.text_input.assert_any_call("New Password", type="password")

    # Verify text input calls for email section
    st.text_input.assert_any_call("Current Email")
    st.text_input.assert_any_call("Repeat Current Email")
    st.text_input.assert_any_call("New Email")

    # Verify button calls
    st.button.assert_any_call("Update Username")
    st.button.assert_any_call("Update Password")
    st.button.assert_any_call("Update Email")
