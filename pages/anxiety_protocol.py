import binascii
import streamlit as st
import pandas as pd
import bcrypt
from github_contents import GithubContents
import datetime

# Constants
DATA_FILE = "MyLoginTable.csv"
DATA_COLUMNS = ['username', 'name', 'password']

def show():
    st.title("Login/Register")

def Login():
    st.image("Logo.jpeg", width=600)

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
            hashed_password = bcrypt.hashpw(new_password.encode('utf8'), bcrypt.gensalt())  # Hash the password
            hashed_password_hex = binascii.hexlify(hashed_password).decode()  # Convert hash to hexadecimal string
            
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
        stored_hashed_password_bytes = binascii.unhexlify(stored_hashed_password)  # Convert hex to bytes
        
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
        anxiety_protocol()

        logout_button = st.button("Logout")
        if logout_button:
            st.session_state['authentication'] = False
            st.session_state.pop('username', None)
            st.experimental_rerun()

def anxiety_protocol():
    username = st.session_state['username']
    data_file = f"{username}_data.csv"
    
    if 'data' not in st.session_state:
        if st.session_state.github.file_exists(data_file):
            st.session_state.data = st.session_state.github.read_df(data_file)
        else:
            st.session_state.data = pd.DataFrame(columns=['Date', 'Time', 'Severity', 'Symptoms', 'Triggers', 'Help'])

st.title("Anxiety Protocol")

    # Question 1: Date
date_selected = st.date_input("Date", value=datetime.date.today())

    # Question 2: Where are you
st.subheader("Where are you and what is the environment?")
help_response = st.text_area("Write your response here", key="location", height=100)
    
st.subheader("Try to describe your anxiety right now?")
help_response = st.text_area("Write your response here", key="anxiety_description", height=100)

st.subheader("What do you think could be the cause?")
help_response = st.text_area("Write your response here", key="cause", height=100)
    
st.subheader("Any specific triggers? For example Stress, Caffeine, Lack of Sleep, Social Event, Reminder of traumatic event")
help_response = st.text_area("Write your response here", key="triggers", height=100)

    # Question 3: Symptoms
st.subheader("Symptoms:")
col1, col2 = st.columns(2)
with col1:
        symptoms_chestpain = st.checkbox("Chest Pain")
        symptoms_chills = st.checkbox("Chills")
        symptoms_cold = st.checkbox("Cold")
        symptoms_coldhands = st.checkbox("Cold Hands")
        symptoms_dizziness = st.checkbox("Dizziness")
        symptoms_feelingdanger = st.checkbox("Feeling of danger")
        symptoms_heartracing = st.checkbox("Heart racing")
        symptoms_hotflushes = st.checkbox("Hot flushes")
with col2:
        symptoms_nausea = st.checkbox("Nausea")
        symptoms_nervous = st.checkbox("Nervousness")
        symptoms_numbhands = st.checkbox("Numb Hands")
        symptoms_numbness = st.checkbox("Numbness")
        symptoms_shortbreath = st.checkbox("Shortness of Breath")
        symptoms_sweating = st.checkbox("Sweating")
        symptoms_tensemuscles = st.checkbox("Tense Muscles")
        symptoms_tinglyhands = st.checkbox("Tingly Hands")
        symptoms_trembling = st.checkbox("Trembling")
        symptoms_tremor = st.checkbox("Tremor")
        symptoms_weakness = st.checkbox("Weakness")
if 'symptoms' not in st.session_state:
        st.session_state.symptoms = []

    # Display existing symptoms
for symptom in st.session_state.symptoms:
        st.write(symptom)

new_symptom = st.text_input("Add new symptom:", key="new_symptom")
if st.button("Add Symptom") and new_symptom:
    st.session_state.symptoms.append(new_symptom)

    # Question 5: Did something Help against the attack?
st.subheader("Did something Help against the Anxiety?")
help_response = st.text_area("Write your response here", key="help_response", height=100)

        # Create a DataFrame from the new entry
new_entry_df = pd.DataFrame([new_entry])
        
        # Append the new entry to the existing data DataFrame
st.session_state.data = pd.concat([st.session_state.data, new_entry_df], ignore_index=True)
        
        # Save the updated DataFrame to the user's specific CSV file on GitHub
st.session_state.github.write_df(data_file, st.session_state.data, "added new entry")
st.success("Entry saved successfully!")

    # Display saved entries
st.subheader("Saved Entries")
st.write(st.session_state.data)

if __name__ == "__main__":
    main()


