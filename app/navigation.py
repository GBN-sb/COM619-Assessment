import streamlit as st
from time import sleep
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import get_pages


def get_current_page_name():
    ctx = get_script_run_ctx()
    if ctx is None:
        raise RuntimeError("Couldn't get script context")

    pages = get_pages("")

    return pages[ctx.page_script_hash]["page_name"]


def make_sidebar():
    with st.sidebar:
        st.write("")
        st.write("")

        if st.session_state.get("logged_in", False):
            st.page_link("pages/Homepage.py", label="Homepage", icon="🏠")
            st.write("User Actions 🎈️")
            st.page_link("pages/My_Recipes.py", label="My Recipes", icon="👨‍🍳")
            st.page_link("pages/Create_Recipes.py", label="Create Recipes", icon="🍳")
            st.page_link("pages/Search_Recipes.py", label="Search Recipes", icon="🍽️")
            st.write("Options ❓")
            st.page_link("pages/Settings.py", label="Settings", icon="⚙️")

            st.write("")
            st.write("")

            if st.button("Logout"):
                logout()
        

        elif st.session_state.get("guest", False):
            st.page_link("pages/Homepage.py", label="Homepage", icon="🏠")
            st.write("User Actions 🎈️")
            st.page_link("pages/Search_Recipes.py", label="Search Recipes", icon="🍽️")

            st.write("")
            st.write("")

            if st.button("Logout"):
                logout()

        
        elif st.session_state.get("admin", False):
            st.page_link("pages/Homepage.py", label="Homepage", icon="🏠")
            st.write("User Actions 🎈️")
            st.page_link("pages/My_Recipes.py", label="My Recipes", icon="👨‍🍳")
            st.page_link("pages/Create_Recipes.py", label="Create Recipes", icon="🍳")
            st.page_link("pages/Search_Recipes.py", label="Search Recipes", icon="🍽️")
            st.write("Options ❓")
            st.page_link("pages/Settings.py", label="Settings", icon="⚙️")
            st.page_link("pages/Admin_Settings.py", label="Admin Settings", icon="🛠️")

            st.write("")
            st.write("")

            if st.button("Logout"):
                logout()

        elif get_current_page_name() != "app":
            st.switch_page("app.py")

def logout():
    st.session_state.guest = False
    st.session_state.logged_in = False
    st.session_state.admin = False
    st.info("Successfully Logged Out.")
    sleep(0.5)
    st.switch_page("app.py")
