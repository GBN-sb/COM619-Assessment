import streamlit as st

usernames = ["User_Username", "Admin_Username"] # TODO - Import these from DB
passwords = ["User_Password", "Admin_Password"]
type = ["User", "Admin"]

def login():
    st.title("Login")
    with st.form("LoginForm"):
        usernameEntered = st.text_input("Username")
        passwordEntered = st.text_input("Password", type="password")

        if st.form_submit_button("Login"):
            if usernameEntered in usernames:
                index = usernames.index(usernameEntered)
                if passwords[index] == passwordEntered:
                    if type[index] == "Admin":
                        st.session_state.admin = True
                    st.success("Login Success")
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Invalid Username or Password")
            else:
                st.error("Invalid Username or Password")

    st.write("Signup:")
    if st.button("Signup"):
        st.session_state.signup = True
        st.rerun()

    st.write("Guest")
    if st.button("Guest"):
        st.session_state.guest = True
        st.session_state.logged_in = True
        st.rerun()

def signup():
    st.title("Signup")
    with st.form("SignupForm"):
        usernameSignup = st.text_input("Username")
        passwordSignup = st.text_input("Password", type="password")
        passwordReEntry = st.text_input("Re-Enter Your Password", type="password")

        if st.form_submit_button("Signup"):
            if passwordSignup != passwordReEntry:
                st.error("Passwords do not match.")
            else:
                if usernameSignup in usernames:
                    st.error("There is already an account with this username.")
                else:
                    usernames.append(usernameSignup)
                    passwords.append(passwordSignup)
                    type.append("User")

                    st.success("Successful Account Creation")
                    st.session_state.signup = False
                    st.session_state.logged_in = True
                    st.rerun()

    st.write("Login")
    if st.button("Login"):
        st.session_state.signup = False
        st.rerun()

    st.write("Guest")
    if st.button("Guest"):
        st.session_state.signup = False
        st.session_state.guest = True
        st.session_state.logged_in = True
        st.rerun()

def Homepage():
    st.title("Homepage")

    if st.session_state.admin:
        st.write("Admin")

    if st.session_state.guest:
        st.write("Guest")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.admin = False
        st.session_state.guest = False
        st.rerun()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "signup" not in st.session_state:
    st.session_state.signup = False

if "guest" not in st.session_state:
    st.session_state.guest = False

if "admin" not in st.session_state:
    st.session_state.admin = False

if st.session_state.logged_in:
    Homepage()
elif st.session_state.signup:
    signup()
else:
    login()