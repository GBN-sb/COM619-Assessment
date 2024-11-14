import pytest
import streamlit as st
from app.pages.Settings import display_settings  # Adjust the import path as needed
from itertools import cycle

@pytest.fixture
def setup_streamlit_mock(mocker):
    """Fixture to mock streamlit functions for the settings page."""
    # Mock the first call to st.columns([1, 1, 1]) to return three mock columns
    col1, col2, col3 = mocker.MagicMock(), mocker.MagicMock(), mocker.MagicMock()
    mocker.patch("streamlit.columns", side_effect=[[col1, col2, col3], [mocker.MagicMock(), mocker.MagicMock()]])

    # Mocking text inputs for username, password, and email in their respective columns
    col1.text_input.side_effect = cycle(["current_username", "current_username", "new_username"])
    col2.text_input.side_effect = cycle(["current_password", "current_password", "new_password"])
    col3.text_input.side_effect = cycle(["current_email", "current_email", "new_email"])

    # Mock other Streamlit elements
    col4, col5 = st.columns.return_value[1]  # Grab mock columns for the second st.columns call
    col4.file_uploader = mocker.Mock(return_value=None)
    col5.radio = mocker.Mock(return_value="Metric")
    mocker.patch("streamlit.button", side_effect=cycle([False, False, True]))  # "Go to Admin" then "Save Changes"
    mocker.patch("streamlit.success")
    mocker.patch("streamlit.error")
    
    # Initialize session state for admin access
    st.session_state["is_admin"] = True

def test_display_settings(setup_streamlit_mock):
    """Test that settings elements are displayed and handle input as expected."""
    # Call the function
    result = display_settings()

    # Verify the calls on each column mock
    st.columns.assert_any_call([1, 1, 1], gap="medium")
    st.columns.assert_any_call([1, 1], gap="large")
    
    # Check username input fields
    st.columns.return_value[0].text_input.assert_any_call("Current Username")
    st.columns.return_value[0].text_input.assert_any_call("Repeat Current Username")
    st.columns.return_value[0].text_input.assert_any_call("New Username")

    # Check password input fields
    st.columns.return_value[1].text_input.assert_any_call("Current Password", type="password")
    st.columns.return_value[1].text_input.assert_any_call("Repeat Current Password", type="password")
    st.columns.return_value[1].text_input.assert_any_call("New Password", type="password")

    # Check email input fields
    st.columns.return_value[2].text_input.assert_any_call("Current Email")
    st.columns.return_value[2].text_input.assert_any_call("Repeat Current Email")
    st.columns.return_value[2].text_input.assert_any_call("New Email")

    # Check profile picture file uploader and preferred units radio button
    st.columns.return_value[1][0].file_uploader.assert_called_once_with("Upload New Profile Picture", type=["jpg", "jpeg", "png"])
    st.columns.return_value[1][1].radio.assert_called_once_with("Select Units", options=["Metric", "Imperial"])

    # Verify button actions for admin and saving changes
    st.button.assert_any_call("Go to Admin Dashboard")
    st.button.assert_any_call("Save Changes")
    
    # Assert result data
    if result:
        new_username, new_email, new_password, new_profile_picture, units_option = result
        assert new_username == "new_username"
        assert new_email == "new_email"
        assert new_password == "new_password"
        assert new_profile_picture is None
        assert units_option == "Metric"
    
    # Check for success or error message display
    st.success.assert_called_once_with("Your settings have been updated.")
    st.error.assert_not_called()
