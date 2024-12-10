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
        db_name=f"{db_base_name}"
        return db_name
    if RUN_ENV == "2":
        db_name=f"test_{db_base_name}"
        return db_name
    if RUN_ENV == "3":
        db_name=f"dev_{db_base_name}"
        return db_name

user_dao = UserDAO(db_name=get_dao("users"))

def display_admin_settings():
    """Display the admin settings options overlay on the current page."""
    st.title("🛠️ Admin Settings")
    st.write("---")
    col1, col2, col3 = st.columns([1, 1, 1], gap="medium")

    # Create Admin
    col1.subheader("Create Admin")
    admin_email = col1.text_input("Admin Email")
    admin_username = col1.text_input("Admin Username")
    admin_password = col1.text_input("Admin Password", type="password")
    repeat_admin_password = col1.text_input("Repeat Admin Password", type="password")

    # Grant Admin Access
    col2.subheader("Grant Admin Access")
    grant_email = col2.text_input("User Email")
    grant_username = col2.text_input("User Username")

    # Delete User
    col3.subheader("Delete User")
    delete_username = col3.text_input("Username to Delete")

    # Action Buttons
    col4, col5, col6 = st.columns([1, 1, 1], gap="medium")

    # Create Admin Button
    if col4.button("Create Admin", use_container_width=True, type="primary"):
        if admin_password == repeat_admin_password:
            try:
                new_user = User(
                    name=admin_username,
                    email=admin_email,
                    password=admin_password,
                    role="admin",
                    bio="New Admin",
                    profile_picture="db\\profile_pics\\no_pfp.png"
                )
                success = user_dao.add_user(new_user)
                if success:
                    st.success(f"Admin '{admin_username}' created successfully.")
                else:
                    st.error("Failed to create admin. Please try again.")
            except Exception as e:
                st.error(f"Error creating admin: {e}")
        else:
            st.error("Passwords do not match. Please try again.")

    # Grant Admin Access Button
    if col5.button("Grant Admin Access", use_container_width=True, type="primary"):
        if grant_email and grant_username:
            try:
                # Get the user by email
                user = user_dao.get_user_by_email(grant_email)
                if user:
                    success = user_dao.update_user_role(user.id, "admin")
                    print(success)
                    if success:
                        st.success(f"Admin access granted to user '{grant_username}'.")
                    else:
                        print("failed")
                        st.error("Failed to grant admin access. Please try again.")
                else:
                    st.error(f"No user found with email '{grant_email}'.")
            except Exception as e:
                print("Exception st.success doesnt work")
                st.error(f"Error granting admin access: {e}")
        else:
            st.error("Please provide both email and username.")

    # Delete User Button
    if col6.button("Delete User", use_container_width=True, type="primary"):
        if delete_username:
            try:
                # Fetch user by username
                users = user_dao.get_all_users()
                user_to_delete = next((u for u in users if u.name == delete_username), None)
                if user_to_delete:
                    success = user_dao.delete_user(user_to_delete.id)
                    if success:
                        st.success(f"User '{delete_username}' deleted successfully.")
                    else:
                        st.error("Failed to delete user. Please try again.")
                else:
                    st.error(f"No user found with username '{delete_username}'.")
            except Exception as e:
                st.error(f"Error deleting user: {e}")
        else:
            st.error("Please provide a username to delete.")


def main():  # pragma: no cover
    st.set_page_config(layout="wide")
    make_sidebar()

    # Display admin settings
    display_admin_settings()


if __name__ == "__main__":  # pragma: no cover
    main()
