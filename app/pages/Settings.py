import streamlit as st
from navigation import make_sidebar
from db.dao.userDAO import UserDAO
from models.user import User
import os
import dotenv

dotenv.load_dotenv()
RUN_ENV = os.getenv('RUN_ENV')

def get_dao(db_base_name):
    if RUN_ENV == "1":
        db_name = f"{db_base_name}"
    elif RUN_ENV == "2":
        db_name = f"test_{db_base_name}"
    elif RUN_ENV == "3":
        db_name = f"dev_{db_base_name}"
    else:
        db_name = db_base_name
    return db_name

user_dao = UserDAO(db_name=get_dao("users"))

def display_settings():
    """Display the settings options overlay on the current page."""
    st.title("⚙️ Settings")
    st.write("---")
    col1, col2, col3 = st.columns([1, 1, 1], gap="medium")

    current_user = st.session_state.user
    starting_username = st.session_state.user.name

    # Column 1: Change Username
    with col1:
        st.subheader("Change Username")
        current_username = st.text_input("Current Username")
        repeat_current_username = st.text_input("Repeat Current Username")
        new_username = st.text_input("New Username")

        if st.button("Update Username"):
            if current_username == repeat_current_username:
                try:
                    updated_user = current_user
                    updated_user.name = new_username or current_user.name
                    if user_dao.add_user(updated_user):
                        st.success("Username updated successfully!")
                        user_dao.delete_user_by_username(starting_username)
                        st.session_state.user = updated_user
                    else:
                        st.error("Failed to update username.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
            else:
                st.error("Current username entries do not match.")

    # Column 2: Change Password
    with col2:
        st.subheader("Change Password")
        current_password = st.text_input("Current Password", type="password")
        repeat_current_password = st.text_input("Repeat Current Password", type="password")
        new_password = st.text_input("New Password", type="password")

        if st.button("Update Password"):
            if current_password == repeat_current_password:
                if User.verify_password(current_password, current_user.password_hash):
                    try:
                        # Use the new update_user_password method
                        if user_dao.update_user_password(current_user.id, User.hash_password(new_password)):
                            st.success("Password updated successfully!")
                            # Update session state with the new password hash
                            updated_user = current_user
                            updated_user.password_hash = User.hash_password(new_password)  # Hash the new password
                            st.session_state.user = updated_user
                        else:
                            st.error("Failed to update password.")
                    except Exception as e:
                        st.error(f"An error occurred: {e}")
                else:
                    st.error("Incorrect current password.")
            else:
                st.error("Current password entries do not match.")

    # Column 3: Change Email
    with col3:
        st.subheader("Change Email")
        current_email = st.text_input("Current Email")
        repeat_current_email = st.text_input("Repeat Current Email")
        new_email = st.text_input("New Email")

        if st.button("Update Email"):
            if current_email == repeat_current_email:
                try:
                    updated_user = current_user
                    updated_user.email = new_email or current_user.email
                    if user_dao.add_user(updated_user):
                        st.success("Email updated successfully!")
                        user_dao.delete_user_by_username(starting_username)
                        st.session_state.user = updated_user
                    else:
                        st.error("Failed to update email.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
            else:
                st.error("Current email entries do not match.")

def main():  # pragma: no cover
    st.set_page_config(layout="wide")
    make_sidebar()

    # Display settings
    display_settings()


if __name__ == "__main__":  # pragma: no cover
    main()
