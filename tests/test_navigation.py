import pytest
import streamlit as st
from unittest.mock import MagicMock
from app.navigation import make_sidebar, get_current_page_name, logout
from time import sleep


# Fixture to mock Streamlit components and session state
@pytest.fixture
def setup_streamlit_mocks(mocker):
    # Mock session state for different conditions
    st.session_state["logged_in"] = False
    st.session_state["guest"] = False
    st.session_state["admin"] = False

    # Mock Streamlit components
    mocker.patch("streamlit.write")
    mocker.patch("streamlit.page_link")
    mocker.patch("streamlit.button", return_value=False)
    mocker.patch("streamlit.switch_page")
    mocker.patch("streamlit.info")

    return st


def test_get_current_page_name_no_ctx(mocker, setup_streamlit_mocks):
    """Test get_current_page_name when the script context is None."""
    
    # Mock get_script_run_ctx to return None
    mocker.patch("streamlit.runtime.scriptrunner.get_script_run_ctx", return_value=None)
    
    # Expecting a RuntimeError
    with pytest.raises(RuntimeError, match="Couldn't get script context"):
        get_current_page_name()


def test_sidebar_logged_in(mocker, setup_streamlit_mocks):
    """Test sidebar when logged in."""
    st.session_state["logged_in"] = True
    make_sidebar()

    # Check if correct links and buttons are rendered
    st.page_link.assert_any_call("pages/Homepage.py", label="Homepage", icon="🏠")
    st.page_link.assert_any_call("pages/My_Recipes.py", label="My Recipes", icon="👨‍🍳")
    st.page_link.assert_any_call("pages/Create_Recipes.py", label="Create Recipes", icon="🍳")
    st.page_link.assert_any_call("pages/Search_Recipes.py", label="Search Recipes", icon="🍽️")
    st.page_link.assert_any_call("pages/Settings.py", label="Settings", icon="⚙️")
    st.button.assert_any_call("Logout")


def test_sidebar_guest(mocker, setup_streamlit_mocks):
    """Test sidebar when in guest mode."""
    st.session_state["guest"] = True
    make_sidebar()

    # Check if correct links and buttons are rendered
    st.page_link.assert_any_call("pages/Homepage.py", label="Homepage", icon="🏠")
    st.page_link.assert_any_call("pages/Search_Recipes.py", label="Search Recipes", icon="🍽️")
    st.button.assert_any_call("Logout")


def test_sidebar_admin(mocker, setup_streamlit_mocks):
    """Test sidebar when logged in as an admin."""
    st.session_state["admin"] = True
    make_sidebar()

    # Check if correct links and buttons are rendered
    st.page_link.assert_any_call("pages/Homepage.py", label="Homepage", icon="🏠")
    st.page_link.assert_any_call("pages/My_Recipes.py", label="My Recipes", icon="👨‍🍳")
    st.page_link.assert_any_call("pages/Create_Recipes.py", label="Create Recipes", icon="🍳")
    st.page_link.assert_any_call("pages/Search_Recipes.py", label="Search Recipes", icon="🍽️")
    st.page_link.assert_any_call("pages/Settings.py", label="Settings", icon="⚙️")
    st.button.assert_any_call("Logout")

def test_logout(mocker, setup_streamlit_mocks):
    """Test the logout function."""
    # Set session state to logged in
    st.session_state["logged_in"] = True

    # Call logout
    logout()

    # Check that session states are reset
    assert not st.session_state.get("logged_in", False)
    assert not st.session_state.get("guest", False)
    assert not st.session_state.get("admin", False)
    st.info.assert_called_once_with("Successfully Logged Out.")
    st.switch_page.assert_called_once_with("app.py")
