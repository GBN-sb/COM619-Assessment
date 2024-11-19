import streamlit as st
from time import sleep

usernames = ["username", "admin"]
passwords = ["password", "admin"]
user_type = ["user", "admin"]


st.title("Welcome to Recipes")

def login_page():

    st.write("Please log in to continue.")
    st.write("User: username `username`, password `password`.")
    st.write("Admin: username `admin`, password `admin`.")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Log in", type="primary"):
            if username in usernames:
                location = usernames.index(username)
                if password == passwords[location]:
                    if user_type[location] == "user":
                        st.session_state.logged_in = True
                    elif user_type[location] == "admin":
                        st.session_state.admin = True
                st.success("Logged in successfully!")
                sleep(0.5)
                st.switch_page("pages/Homepage.py")

            else:
                st.error("Incorrect username or password")

    with col2:
        if st.button("Guest", type="primary"):
            st.session_state.guest = True
            st.success("Logging in as Guest.")
            sleep(0.5)
            st.switch_page("pages/Homepage.py")

    with col3:
        if st.button("Signup", type="primary"):
            st.session_state.sign_up = True
            st.session_state.login_page = False
            st.rerun()

def signup_page():

    st.write("Please sign up to continue.")
    usernameSignup = st.text_input("Username")
    passwordSignup = st.text_input("Password", type="password")
    passwordReEntry = st.text_input("Re-Enter Your Password", type="password")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Sign up", type="primary"):
            if usernameSignup in usernames:
                    st.error("There is already an account with this username.")
            else:
                    if passwordSignup != passwordReEntry:
                        st.error("Passwords do not match.")
                    else:
                        usernames.append(usernameSignup)
                        passwords.append(passwordSignup)
                        user_type.append("User")

                        st.success("Successful Account Creation. Please login.")
                        sleep(0.5)
                        st.session_state.logged_in = True
                        st.session_state.sign_up = False
                        st.switch_page("pages/Homepage.py")

    with col2:
        if st.button("Guest", type="primary"):
            st.session_state.guest = True
            st.success("Logging in as Guest.")
            sleep(0.5)
            st.switch_page("pages/Homepage.py")

    with col3:
        if st.button("Login", type="primary"):
            st.session_state.login_page = True
            st.session_state.sign_up = False
            st.rerun()

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
