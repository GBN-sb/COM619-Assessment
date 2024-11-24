import streamlit as st
from navigation import make_sidebar

st.set_page_config(layout="wide")
make_sidebar()

user_type=""
if st.session_state.logged_in:
    user_type="User"
elif st.session_state.admin:
    user_type="Admin"
elif st.session_state.guest:
    user_type="Guest"


st.title(f"Welcome to the Homepage, {user_type}")
st.write("---")
st.write("Page content goes here")
