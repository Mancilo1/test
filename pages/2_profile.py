import streamlit as st
import binascii
import bcrypt
import time
import datetime
import sys
import os
import pandas as pd
from github_contents import GithubContents
from PIL import Image

# Constants
DATA_FILE = "MyLoginTable.csv"
DATA_COLUMNS = ['username', 'name', 'password']

def main_page():
    st.image("Logo.jpeg", width=600)
    st.title("Your Anxiety Tracker Journal")
    st.subheader("Profile")
    
    # Überprüfe, ob der Benutzer eingeloggt ist
    if 'username' in st.session_state:
        username = st.session_state['username']
        
        # Lade die Benutzerdaten aus dem DataFrame
        user_data = st.session_state.df_users.loc[st.session_state.df_users['username'] == username]
        
        if not user_data.empty:
            st.write("Username:", username)
            st.write("Name:", user_data['name'].iloc[0])
            st.write("Birthday:", user_data['birthday'].iloc[0])
        else:
            st.error("User data not found.")
    else:
        st.error("User not logged in.")
        if st.button("Login/Register"):
            st.switch_page("pages/1_login.py")

def main():
    init_github()
    init_credentials()

    if 'authentication' not in st.session_state:
        st.session_state['authentication'] = False

    if not st.session_state['authentication']:
        options = st.sidebar.selectbox("Select a page", ["Login", "Register"])
        if options == "Login":
            login_page()
        elif options == "Register":
            register_page()
    else:
        st.sidebar.write(f"Logged in as {st.session_state['username']}")
        main_page()
        anxiety_assessment()
        logout_button = st.sidebar.button("Logout")
        if logout_button:
            st.session_state['authentication'] = False
            st.session_state.pop('username', None)
            st.switch_page("main.py")
            st.experimental_rerun()

def anxiety_assessment():
    st.subheader("Anxiety Assessment:")
    
    st.write("Do you feel like you're having an Anxiety Attack right now?")
    if st.button("Yes"):
        st.switch_page("pages/4_anxiety_attack_protocol.py")
    elif st.button("No"):
        st.write("Are you anxious right now?")
        if st.button("Yes "):
            st.switch_page("pages/5_anxiety_protocol.py")
        elif st.button("No "):
            st.write("Reassess your feelings")

def init_github():
    """Initialize the GithubContents object."""
    if 'github' not in st.session_state:
        st.session_state.github = GithubContents(
            st.secrets["github"]["owner"],
            st.secrets["github"]["repo"],
            st.secrets["github"]["token"])
        print("github initialized")
    
def init_credentials():
    """Initialize or load the dataframe."""
    if 'df_users' not in st.session_state:
        if st.session_state.github.file_exists(DATA_FILE):
            st.session_state.df_users = st.session_state.github.read_df(DATA_FILE)
        else:
            st.session_state.df_users = pd.DataFrame(columns=DATA_COLUMNS)

def login_page():
    """ Login an existing user. """
    st.title("Login")
    with st.form(key='login_form'):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            authenticate(username, password)
            # Wenn die Anmeldeinformationen korrekt sind, wird auf die Hauptseite umgeschaltet
            if st.session_state['authentication']:
                st.switch_page("pages/2_profile.py")

def register_page():
    """ Register a new user. """
    st.title("Register")
    with st.form(key='register_form'):
        new_username = st.text_input("New Username")
        new_name = st.text_input("Name")
        new_password = st.text_input("New Password", type="password")
        if st.form_submit_button("Register"):
            hashed_password = bcrypt.hashpw(new_password.encode('utf8'), bcrypt.gensalt())
            hashed_password_hex = binascii.hexlify(hashed_password).decode()
            
            # Check if the username already exists
            if new_username in st.session_state.df_users['username'].values:
                st.error("Username already exists. Please choose a different one.")
                return
            else:
                new_user = pd.DataFrame([[new_username, new_name, hashed_password_hex]], columns=DATA_COLUMNS)
                st.session_state.df_users = pd.concat([st.session_state.df_users, new_user], ignore_index=True)
                
                # Writes the updated dataframe to GitHub data repository
                st.session_state.github.write_df(DATA_FILE, st.session_state.df_users, "added new user")
                st.success("Registration successful! You can now log in.")

def authenticate(username, password):
    """
    Authenticate the user.

    Parameters:
    username (str): The username to authenticate.
    password (str): The password to authenticate.
    """
    login_df = st.session_state.df_users
    login_df['username'] = login_df['username'].astype(str)

    if username in login_df['username'].values:
        stored_hashed_password = login_df.loc[login_df['username'] == username, 'password'].values[0]
        stored_hashed_password_bytes = binascii.unhexlify(stored_hashed_password)
        
        # Check the input password
        if bcrypt.checkpw(password.encode('utf8'), stored_hashed_password_bytes): 
            st.session_state['authentication'] = True
            st.session_state['username'] = username
            st.success('Login successful')
            st.experimental_rerun()
        else:
            st.error('Incorrect password')
    else:
        st.error('Username not found')

# Funktion zur Seitenumschaltung
def switch_page(page_name):
    st.success(f"Redirecting to {page_name.replace('_', ' ')} page...")
    time.sleep(3)
    st.experimental_set_query_params(page=page_name)
    st.experimental_rerun()

if __name__ == "__main__":
    main()
