import binascii
import streamlit as st
import pandas as pd
import bcrypt
from github_contents import GithubContents
import datetime
from PIL import Image

# Constants
DATA_FILE = "MyLoginTable.csv"
DATA_COLUMNS = ['username', 'name', 'password']

def show():
    st.title("Profile")

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
        
    st.subheader("Profile Picture")
        profile_picture = st.session_state.profile_picture
        if profile_picture is None:
            st.warning("No profile picture uploaded yet.")
            uploaded_file = st.file_uploader("Upload Profile Picture", type=["jpg", "jpeg", "png"])
            if uploaded_file is not None:
                st.session_state.profile_picture = Image.open(uploaded_file)
        else:
            st.image(profile_picture, caption="Your Profile Picture", use_column_width=True)
    else:
        st.error("User data not found.")

# Deine anderen Funktionen bleiben unverändert

def main():
    init_github()
    init_credentials()

    # Add the logo to the sidebar
    st.sidebar.image("Logo.jpeg", use_column_width=True)
    
    if 'authentication' not in st.session_state:
        st.session_state['authentication'] = False

    if not st.session_state['authentication']:
        options = st.sidebar.selectbox("Select a page", ["Login", "Register"])
        if options == "Login":
            login_page()
        elif options == "Register":
            register_page()
    else:
        logout_button = st.sidebar.button("Logout")
        if logout_button:
            st.session_state['authentication'] = False
            st.experimental_rerun()
        else:
            profile_page()

def login_page():
    """ Login an existing user. """
    st.title("Login")
    with st.form(key='login_form'):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            authenticate(username, password)

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

if __name__ == "__main__":
    main_page()
