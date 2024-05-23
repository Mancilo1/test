import streamlit as st
import pandas as pd
import bcrypt
import binascii
from github_contents import GithubContents

# Constants
DATA_FILE = "MyLoginTable.csv"
DATA_COLUMNS = ['username', 'first_name','last_name', 'birthday', 'password']

def show():
    st.title("Login/Register")

def Login():
    st.image("Logo.jpeg", width=500, align='center')

def login_page():
    """ Login an existing user. """
    st.image("Logo.jpeg", width=600)
    st.write("---")
    st.title("Login")
    with st.form(key='login_form'):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            authenticate(username, password)
            st.switch_page("pages/2_profile.py")

def register_page():
    """ Register a new user. """
    st.title("Register")
    with st.form(key='register_form'):
        st.write("Please fill in the following details:")
        new_first_name = st.text_input("First Name")
        new_last_name = st.text_input("Last Name")
        new_username = st.text_input("Username")
        new_birthday = st.date_input("Birthday", min_value=datetime.date(1900, 1, 1))
        new_password = st.text_input("Password", type="password")
        if st.form_submit_button("Register"):
            # Check if the username already exists
            if new_username in st.session_state.df_users['username'].values:
                st.error("Username already exists. Please choose a different one.")
                return
            else:
                # Hash the password
                hashed_password = bcrypt.hashpw(new_password.encode('utf8'), bcrypt.gensalt())
                hashed_password_hex = binascii.hexlify(hashed_password).decode()
                
                # Create a new user DataFrame
                new_user_data = [[new_username, f"{new_first_name} {new_last_name}", new_birthday, hashed_password_hex]]
                new_user = pd.DataFrame(new_user_data, columns=DATA_COLUMNS)
                
                # Concatenate the new user DataFrame with the existing one
                st.session_state.df_users = pd.concat([st.session_state.df_users, new_user], ignore_index=True)
                
                # Write the updated dataframe to GitHub data repository
                try:
                    st.session_state.github.write_df(DATA_FILE, st.session_state.df_users, "added new user")
                    st.success("Registration successful! You can now log in.")
                    st.switch_page("pages/2_profile.py")
                except GithubContents.UnknownError as e:
                    st.error(f"An unexpected error occurred: {e}")
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")

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
        stored_hashed_password_bytes = binascii.unhexlify(stored_hashed_password)  # Convert hex to bytes
        
        if bcrypt.checkpw(password.encode('utf8'), stored_hashed_password_bytes): 
            st.session_state['authentication'] = True
            st.session_state['username'] = username
            st.success('Login successful')
            st.switch_page("pages/2_profile.py")
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

def switch_page(page_name):
    st.success(f"Redirecting to {page_name.replace('_', ' ')} page...")
    time.sleep(3)
    st.experimental_set_query_params(page=page_name)
    st.experimental_rerun()

if __name__ == "__main__":
    main()
