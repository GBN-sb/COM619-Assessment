import streamlit as st

# Page layout setup
st.set_page_config(page_title="Homepage", layout="wide")

# Sidebar buttons
col1, col2 = st.sidebar.columns(2)
button1 = col1.button('Logout')
button2 = col2.button('Settings')

st.title("Homepage")