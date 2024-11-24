import streamlit as st
from navigation import make_sidebar

st.set_page_config(layout="wide")
make_sidebar()

def display_settings():
    """Display the settings options overlay on the current page."""
    st.write("---")
    col1, col2, col3 = st.columns([1, 1, 1], gap="medium")

    # Change Username
    col1.subheader("Change Username")
    current_username = col1.text_input("Current Username")
    repeat_current_username = col1.text_input("Repeat Current Username")
    new_username = col1.text_input("New Username")

    # Change Password
    col2.subheader("Change Password")
    current_password = col2.text_input("Current Password", type="password")
    repeat_current_password = col2.text_input("Repeat Current Password", type="password")
    new_password = col2.text_input("New Password", type="password")

    # Change Email
    col3.subheader("Change Email")
    current_email = col3.text_input("Current Email")
    repeat_current_email = col3.text_input("Repeat Current Email")
    new_email = col3.text_input("New Email")

    col4, col5 = st.columns([1, 1], gap="large")
    
    # Change Profile Picture
    col4.subheader("Change Profile Picture")
    new_profile_picture = col4.file_uploader("Upload New Profile Picture", type=["jpg", "jpeg", "png"])
    
    # Toggle between metric and imperial units
    col5.subheader("Preferred Units")
    units_option = col5.radio("Select Units", options=["Metric", "Imperial"])

    # Admin Dashboard Button (only visible if the user has admin access)
    if st.session_state.get("is_admin", False):
        if st.button("Go to Admin Dashboard"):
            st.write("Transferring to admin dashboard...")
            # TODO Add move to admin dashboard

    # Save Changes Button
    if st.button("Save Changes"):
        # Validation logic
        if (
            current_username == repeat_current_username and
            current_password == repeat_current_password and
            current_email == repeat_current_email
        ):
            st.success("Your settings have been updated.")
            # TODO Perform the save logic, e.g., updating the database
            return new_username, new_email, new_password, new_profile_picture, units_option
        else:
            st.error("Current details do not match. Please try again.")

display_settings()