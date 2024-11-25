import streamlit as st
from time import sleep

# User data
usernames = ["username", "admin"]
passwords = ["password", "admin"]
user_types = ["user", "admin"]

# Page setup
st.set_page_config(page_title="Login/Signup", page_icon="🔐", layout="centered")
st.title("🍴 Welcome to Recipes")
st.markdown("---")  # Divider for better separation


# Login Page
def login_page():
    st.header("Login")
    st.markdown("### Please log in to continue.")
    with st.expander(
        "Temporary Login Information"
    ):  # TODO Remove this once the database and DAOs have been integrated
        st.write("User: username `username`, password `password`.")  # ^
        st.write("Admin: username `admin`, password `admin`.")  # ^

    # Login form
    username = st.text_input("Username", placeholder="Enter your username")
    password = st.text_input(
        "Password", type="password", placeholder="Enter your password"
    )
    st.write("###")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Log In", use_container_width=True, type="primary"):
            if username in usernames:
                user_index = usernames.index(username)
                if password == passwords[user_index]:
                    st.session_state["logged_in"] = True
                    user_role = user_types[user_index]
                    st.success(f"Logged in successfully as {user_role.capitalize()}!")
                    sleep(1)
                    st.switch_page("pages/Homepage.py")  # Switch to the Homepage
                else:
                    st.error("Incorrect password. Please try again.")
            else:
                st.error("Username not found. Please try again.")
    with col2:
        if st.button("Signup", use_container_width=True, type="primary"):
            st.session_state.sign_up = True
            st.session_state.login_page = False
            st.rerun()

    st.markdown("---")
    if st.button("Continue as Guest", use_container_width=True, type="primary"):
        st.session_state["guest"] = True
        st.success("Logged in as Guest.")
        sleep(1)
        st.switch_page("pages/Homepage.py")


# Signup Page
def signup_page():
    st.header("Sign Up")
    st.markdown("### Create a new account.")

    # Signup form
    username_signup = st.text_input("Username", placeholder="Choose a unique username")
    password_signup = st.text_input(
        "Password", type="password", placeholder="Create a password"
    )
    password_reentry = st.text_input(
        "Confirm Password", type="password", placeholder="Re-enter your password"
    )
    st.write("###")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Sign Up", use_container_width=True, type="primary"):
            if username_signup in usernames:
                st.error(
                    "This username is already taken. Please choose a different one."
                )
            elif password_signup != password_reentry:
                st.error("Passwords do not match. Please try again.")
            else:
                usernames.append(username_signup)
                passwords.append(password_signup)
                user_types.append("user")
                st.success("Account created successfully! Please log in.")
                sleep(1)
                st.switch_page("pages/Homepage.py")  # Switch to the Homepage
    with col2:
        if st.button("Login", use_container_width=True, type="primary"):
            st.session_state.sign_up = False
            st.session_state.login_page = True
            st.switch_page("pages/Homepage.py")  # Switch to the Homepage


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "admin" not in st.session_state:
    st.session_state.admin = False

if "guest" not in st.session_state:
    st.session_state.guest = False

if "login_page" not in st.session_state:
    st.session_state.login_page = False

if "sign_up" not in st.session_state:
    st.session_state.sign_up = False

if st.session_state.sign_up:
    signup_page()
else:
    login_page()
