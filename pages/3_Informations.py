import streamlit as st
import binascii
import bcrypt
import time
import pandas as pd
from github_contents import GithubContents
from PIL import Image

# Constants
DATA_FILE = "MyLoginTable.csv"
DATA_COLUMNS = ['username', 'name', 'birthday', 'password', 'phone_number', 'address', 'occupation', 'emergency_contact_name', 'emergency_contact_number', 'email', 'doctor_email']

def main():
    init_github()
    init_credentials()
    logo_path = "Logo.jpeg"  # Ensure this path is correct relative to your script location
    st.image(logo_path, use_column_width=True)
    st.title("Inform yourselfe about Mental Health")

    if 'username' in st.session_state:
        username = st.session_state['username']
        
        # Load user data
        user_data = st.session_state.df_users.loc[st.session_state.df_users['username'] == username]
        
        if not user_data.empty:
            if 'edit_profile' not in st.session_state:
                st.session_state.edit_profile = False

    # Article 1
    st.write("## Anxiety Disorder")
    st.write("### National Institution of Mental Health")
    st.markdown(""" 
    What is anxiety?
    Occasional anxiety is a normal part of life. Many people worry about things such as health, money, or family problems. But anxiety disorders involve more than temporary worry or fear. For people with an anxiety disorder, the anxiety does not go away and can get worse over time. The symptoms can interfere with daily activities such as job performance, schoolwork, and relationships.
    
    There are several types of anxiety disorders, including generalized anxiety disorder, panic disorder, social anxiety disorder, and various phobia-related disorders. 
    """)
    st.markdown('<a href="https://www.nimh.nih.gov/health/topics/anxiety-disorders" target="_blank"><button>Read more</button></a>', unsafe_allow_html=True)

    # Article 2
    st.write("## Anxiety Disorder")
    st.write("### World Health Organisation")
    st.markdown("""
    Everyone can feel anxious sometimes, but people with anxiety disorders often experience fear and worry that is both intense and excessive. These feelings are typically accompanied by physical tension and other behavioural and cognitive symptoms. They are difficult to control, cause significant distress and can last a long time if untreated. Anxiety disorders interfere with daily activities and can impair a person’s family, social and school or working life.

    An estimated 4% of the global population currently experience an anxiety disorder (1). In 2019, 301 million people in the world had an anxiety disorder, making anxiety disorders the most common of all mental disorders (1).

    Although highly effective treatments for anxiety disorders exist, only about 1 in 4 people in need (27.6%) receive any treatment (2). Barriers to care include lack of awareness that this is a treatable health condition, lack of investment in mental health services, lack of trained health care providers, and social stigma.
    """)
    st.markdown('<a href="https://www.who.int/news-room/fact-sheets/detail/anxiety-disorders" target="_blank"><button>Read more</button></a>', unsafe_allow_html=True)

    # Article 3
    st.write("## 11 tips for coping with an anxiety disorder")
    st.markdown("""
    Keep physically active.
    Develop a routine so that you're physically active most days of the week. Exercise is a powerful stress reducer. It can improve your mood and help you stay healthy. Start out slowly, and gradually increase the amount and intensity of your activities.
    Avoid alcohol and recreational drugs.
    These substances can cause or worsen anxiety. If you can't quit on your own, see your healthcare provider or find a support group to help you.
    Quit smoking, and cut back or quit drinking caffeinated beverages.
    Nicotine and caffeine can worsen anxiety.
    """)
    st.markdown('<a href="https://www.mayoclinichealthsystem.org/hometown-health/speaking-of-health/11-tips-for-coping-with-an-anxiety-disorder" target="_blank"><button>Read more</button></a>', unsafe_allow_html=True)
        
    # Article 4
    st.write("## I Feel Anxious: Tips for Dealing with Anxiety")
    st.write("Feeling tense, restless, or fearful? Anxiety can make you feel trapped in your own head, but these tools can help you ease tension, stay present, and manage anxiety.")
    st.markdown(""" 
    Why am I anxious?
    Anxiety can arise for all sorts of reasons. You may feel restless and have a hard time sleeping the night before an important test, an early flight, or a job interview, for example. Or you may feel nauseous when you think about going to a party and interacting with strangers, or physically tense when comparing your bank balance to the bills that keep mounting up.

    Sometimes it can seem that you feel nervous, panicky, and on-edge for no reason at all. However, there’s usually a trigger to feelings of anxiety and panic, even if it’s not immediately obvious.
    """)
    st.markdown('<a href="https://www.helpguide.org/articles/anxiety/i-feel-anxious-tips-for-dealing-with-anxiety.htm" target="_blank"><button>Read more</button></a>', unsafe_allow_html=True)

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
    """Login an existing user."""
    st.title("Login")
    with st.form(key='login_form'):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            authenticate(username, password)
def login_page():
    """Login an existing user."""
    st.title("Login")
    with st.form(key='login_form'):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            authenticate(username, password)

def register_page():
    """Register a new user."""
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

def switch_page(page_name):
    st.success(f"Redirecting to {page_name.replace('_', ' ')} page...")
    st.experimental_set_query_params(page=page_name)
    time.sleep(3)
    st.experimental_rerun()

if __name__ == "__main__":
    main()
