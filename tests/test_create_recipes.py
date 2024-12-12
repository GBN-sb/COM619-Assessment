import pytest
import streamlit as st
from itertools import cycle
from app.pages import Create_Recipes

@pytest.fixture
def setup_streamlit_mock(mocker):
    """Fixture to mock streamlit functions."""
    mocker.patch("streamlit.button", side_effect=cycle([False, False]))  # Mocks Logout and Settings buttons
    mocker.patch("streamlit.form_submit_button", return_value=False)  # Mocks form submit button
    mocker.patch("streamlit.text_input", side_effect=["Test Title", "Sample text"])  # Mock title and tags
    mocker.patch("streamlit.text_area", return_value="Sample text")  # Mock text areas
    mocker.patch("streamlit.columns", return_value=[st, st])  # Mock column return value
    mocker.patch("streamlit.file_uploader", return_value=None)  # Mock file uploader (no file uploaded)

def test_display_form(setup_streamlit_mock, mocker):
    """Test that form fields are displayed and return correct defaults/mocked values."""
    form_data = Create_Recipes.display_form()

    # Assert that each form element was called with expected defaults or return values
    st.text_input.assert_any_call("Title:")
    st.text_area.assert_any_call("Ingredients: (Separated by commas at the end of new lines)", height=100)
    st.text_area.assert_any_call("Steps: (Separated by commas at the end of new lines)", height=150)
    st.text_area.assert_any_call("Description / Notes:", height=100)
    st.columns.assert_any_call([1, 1], gap="small")  # Assert columns are used for tags/image
    st.file_uploader.assert_any_call("Upload an image:", type=["png", "jpg", "jpeg"])

    # Check form_data returns the mocked data
    assert form_data["title"] == "Test Title"
    assert form_data["tags"] == "Sample text"
    assert form_data["ingredients"] == "Sample text"
    assert form_data["steps"] == "Sample text"
    assert form_data["description"] == "Sample text"
    assert form_data["finished"] is False  # Finish button not pressed
    assert form_data["image_file_name"] is None  # No file uploaded

