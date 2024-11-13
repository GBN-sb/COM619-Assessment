import pytest
import streamlit as st
from itertools import cycle
from app.pages import Create_Recipes
from app.Settings import display_settings

@pytest.fixture
def setup_streamlit_mock(mocker):
    """Fixture to mock streamlit functions."""
    mocker.patch("streamlit.button", side_effect=cycle([False, False]))  # Mocks Logout and Settings buttons
    mocker.patch("streamlit.form_submit_button", return_value=False)  # Mocks form submit button
    mocker.patch("streamlit.text_input", side_effect=["Test Title", "Sample text"])  # Mock title and tags
    mocker.patch("streamlit.slider", return_value=3)
    mocker.patch("streamlit.text_area", return_value="Sample text")
    mocker.patch("streamlit.file_uploader", return_value=None)

def test_display_form(setup_streamlit_mock, mocker):
    """Test that form fields are displayed and return correct defaults/mocked values."""
    form_data = Create_Recipes.display_form()

    # Assert that each form element was called with expected defaults or return values
    st.text_input.assert_any_call("Title:")
    st.slider.assert_any_call("Difficulty (1-5):", min_value=1, max_value=5, step=1)
    st.text_area.assert_any_call("Ingredients:", height=100)
    st.text_area.assert_any_call("Steps:", height=150)
    st.text_area.assert_any_call("Description / Notes:", height=100)
    st.file_uploader.assert_any_call("Image:", type=["jpg", "jpeg", "png"])

    # Check form_data returns the mocked data
    assert form_data["title"] == "Test Title"
    assert form_data["difficulty"] == 3
    assert form_data["tags"] == "Sample text"
    assert form_data["ingredients"] == "Sample text"
    assert form_data["steps"] == "Sample text"
    assert form_data["description"] == "Sample text"
    assert form_data["image"] is None
    assert form_data["finished"] is False  # Finish button not pressed
