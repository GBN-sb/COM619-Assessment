import streamlit as st
import os
from time import sleep
from db.dao.userDAO import UserDAO
from models.user import User

TEST_MODE = os.getenv('TEST_MODE')

# Initialize UserDAO

# Page setup
st.set_page_config(page_title="Login/Signup", page_icon="🔐", layout="centered")
st.title("🍴 Welcome to Recipes")
st.markdown("---")  # Divider for better separation


# Login Page
def login_page():
    user_dao = UserDAO(db_name="test_users" if TEST_MODE else "users")
    st.header("Login")
    st.markdown("### Please log in to continue.")
    
    # Login form
    username = st.text_input("Username", placeholder="Enter your username")
    password = st.text_input("Password", type="password", placeholder="Enter your password")
    st.write("###")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Log In", use_container_width=True, type="primary"):
            user = user_dao.get_user_by_username(username)
            if user:
                if User.verify_password(password, user.password_hash):
                    if user.role == "admin":
                        st.session_state["admin"] = True
                    else:
                        st.session_state["logged_in"] = True
                    st.success(f"Logged in successfully as {user.role.capitalize()}!")
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
    user_dao = UserDAO(db_name="test_users" if TEST_MODE else "users")
    st.header("Sign Up")
    st.markdown("### Create a new account.")
    
    # Signup form
    username_signup = st.text_input("Username", placeholder="Choose a unique username")
    email_signup = st.text_input("Email", placeholder="Enter your email address")
    password_signup = st.text_input("Password", type="password", placeholder="Create a password")
    password_reentry = st.text_input("Confirm Password", type="password", placeholder="Re-enter your password")
    st.write("###")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Sign Up", use_container_width=True, type="primary"):
            if user_dao.get_user_by_email(email_signup):
                st.error("This email is already associated with an account. Please log in.")
            elif password_signup != password_reentry:
                st.error("Passwords do not match. Please try again.")
            else:
                try:
                    new_user = User(name=username_signup, email=email_signup, password=password_signup, bio="", profile_picture="db\\profile_pics\\no_pfp.png")
                    success = user_dao.add_user(new_user)
                    if success:
                        st.success("Account created successfully! Please log in.")
                        sleep(1)
                        st.session_state.sign_up = False
                        st.session_state.login_page = True
                        st.switch_page("pages/Homepage.py")  # Switch to the Homepage
                    else:
                        st.error("Failed to create account. Please try again.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
    
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
