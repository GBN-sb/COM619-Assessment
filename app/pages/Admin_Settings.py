import streamlit as st
from navigation import make_sidebar

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
            st.success(f"Admin '{admin_username}, {admin_email}' created successfully.")
            # TODO Perform database operation to create admin
        else:
            st.error("Passwords do not match. Please try again.")

    # Grant Admin Access Button
    if col5.button("Grant Admin Access", use_container_width=True, type="primary"):
        if grant_email and grant_username:
            st.success(f"Admin access granted to user '{grant_username}'.")
            # TODO Perform database operation to grant admin access
        else:
            st.error("Please provide both email and username.")

    # Delete User Button
    if col6.button("Delete User", use_container_width=True, type="primary"):
        if delete_username:
            st.success(f"User '{delete_username}' deleted successfully.")
            # TODO Perform database operation to delete user
        else:
            st.error("Please provide a username to delete.")


def main():  # pragma: no cover
    st.set_page_config(layout="wide")
    make_sidebar()

    # Display admin settings
    display_admin_settings()


if __name__ == "__main__":  # pragma: no cover
    main()
