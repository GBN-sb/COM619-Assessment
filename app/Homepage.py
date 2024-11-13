import streamlit as st
from Settings import display_settings

# Page layout setup
st.set_page_config(page_title="Homepage", layout="wide")

# Initialize session state for settings display toggle
if "show_settings" not in st.session_state:
    st.session_state.show_settings = False

# Sidebar setup with buttons for Logout and Settings
with st.sidebar:
    col1, col2 = st.columns(2)
    if col1.button("Logout"):
        # Implement logout logic here
        st.write("You have been logged out.")  # Placeholder
    if col2.button("Settings"):
        st.session_state.show_settings = not st.session_state.show_settings

# Main content area
if st.session_state.show_settings:
    display_settings()  # Display settings in the main content area
else:
    st.title("Homepage")
    st.write("Main application content goes here.")
