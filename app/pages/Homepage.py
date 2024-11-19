import streamlit as st
from navigation import make_sidebar

make_sidebar()

st.write("---")
st.write("Page content goes here")

if st.session_state.logged_in:
    st.write("User")
elif st.session_state.admin:
    st.write("Admin")
elif st.session_state.guest:
    st.write("Guest")
