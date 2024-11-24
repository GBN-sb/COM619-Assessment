import pytest
import streamlit as st
from app.pages.Settings import display_settings  # Adjust the import path as needed
from unittest.mock import MagicMock


@pytest.fixture
def setup_streamlit_mocks(mocker):
    """Fixture to mock streamlit functions used in display_settings."""
    # Mock session state for admin access
    st.session_state["is_admin"] = True

    # Mock Streamlit functions
    mocker.patch("streamlit.write")
    mocker.patch("streamlit.button", side_effect=[False, True])  # First call for "Go to Admin", second for "Save Changes"
    mocker.patch("streamlit.success")
    mocker.patch("streamlit.error")

    # Mock columns and elements
    col1, col2, col3 = MagicMock(), MagicMock(), MagicMock()
    col4, col5 = MagicMock(), MagicMock()

    mocker.patch("streamlit.columns", side_effect=[[col1, col2, col3], [col4, col5]])

    # Define side effects for text input, file uploader, and radio
    col1.text_input.side_effect = ["current_username", "current_username", "new_username"]
    col2.text_input.side_effect = ["current_password", "current_password", "new_password"]
    col3.text_input.side_effect = ["current_email", "current_email", "new_email"]
    col4.file_uploader.return_value = None
    col5.radio.return_value = "Metric"

    return col1, col2, col3, col4, col5


def test_display_settings(setup_streamlit_mocks):
    """Test the display_settings function to verify components and logic."""
    col1, col2, col3, col4, col5 = setup_streamlit_mocks

    # Call the function
    result = display_settings()

    # Verify each section header
    col1.subheader.assert_called_once_with("Change Username")
    col2.subheader.assert_called_once_with("Change Password")
    col3.subheader.assert_called_once_with("Change Email")
    col4.subheader.assert_called_once_with("Change Profile Picture")
    col5.subheader.assert_called_once_with("Preferred Units")

    # Verify text input fields for username, password, and email
    col1.text_input.assert_any_call("Current Username")
    col1.text_input.assert_any_call("Repeat Current Username")
    col1.text_input.assert_any_call("New Username")

    col2.text_input.assert_any_call("Current Password", type="password")
    col2.text_input.assert_any_call("Repeat Current Password", type="password")
    col2.text_input.assert_any_call("New Password", type="password")

    col3.text_input.assert_any_call("Current Email")
    col3.text_input.assert_any_call("Repeat Current Email")
    col3.text_input.assert_any_call("New Email")

    # Verify file uploader and radio button
    col4.file_uploader.assert_called_once_with("Upload New Profile Picture", type=["jpg", "jpeg", "png"])
    col5.radio.assert_called_once_with("Select Units", options=["Metric", "Imperial"])

    # Verify the "Go to Admin Dashboard" button (admin session state is True)
    st.button.assert_any_call("Go to Admin Dashboard")
    
    # Check that "Save Changes" button triggered the validation logic
    st.button.assert_any_call("Save Changes")

    # Check for success message display
    st.success.assert_called_once_with("Your settings have been updated.")

    # Verify that the function returns the expected values
    if result:
        new_username, new_email, new_password, new_profile_picture, units_option = result
        assert new_username == "new_username"
        assert new_email == "new_email"
        assert new_password == "new_password"
        assert new_profile_picture is None
        assert units_option == "Metric"
        