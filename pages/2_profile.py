import streamlit as st
import pandas as pd
from io import BytesIO
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def main_page():
    st.image("Logo.jpeg", width=600)
    st.title("Your Anxiety Tracker Journal")
    
    if 'username' not in st.session_state:
        st.error("User not logged in.")
        if st.button("Login/Register"):
            st.switch_page("pages/1_login.py")
        return

    anxiety_assessment()  # Call assessment first
    
    username = st.session_state['username']
    
    # Display user profile information
    st.subheader("Profile")
    user_data = st.session_state.df_users.loc[st.session_state.df_users['username'] == username]
    if not user_data.empty:
        st.write("Username:", username)
        st.write("Name:", user_data['name'].iloc[0])
        st.write("Birthday:", user_data['birthday'].iloc[0])
    else:
        st.error("User data not found.")
    
    # Display saved entries
    st.subheader("Anxiety Attack Protocol Entries")
    display_saved_entries(f"{username}_anxiety_attack_protocol.csv")
    
    st.subheader("Anxiety Protocol Entries")
    display_saved_entries(f"{username}_anxiety_protocol.csv")

def display_saved_entries(data_file):
    if 'github' not in st.session_state:
        init_github()
        
    st.write(f"Checking for data file: {data_file}")
    if st.session_state.github.file_exists(data_file):
        st.write(f"Loading data from {data_file}")
        data = st.session_state.github.read_df(data_file)
        if data.empty:
            st.write("No entries found.")
        else:
            st.write("Entries loaded successfully!")
            st.dataframe(data)

            # Download entries as CSV
            buffer = BytesIO()
            data.to_csv(buffer, index=False)
            buffer.seek(0)
            st.download_button(
                label="Download Entries as CSV",
                data=buffer,
                file_name=data_file,
                mime="text/csv",
            )

            # Send entries via email
            email = st.text_input(f"Email to send {data_file}", key=f"email_{data_file}")
            if st.button(f"Send {data_file} via Email"):
                if not email:
                    st.error("Please enter an email address.")
                else:
                    send_email(email, data, data_file)
                    st.success(f"Entries sent to {email}")
    else:
        st.write("No entries found.")

def send_email(to_email, dataframe, filename):
    from_email = st.secrets["email"]["username"]
    from_password = st.secrets["email"]["password"]
    subject = "Your Saved Entries"

    # Create email message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    body = "Please find attached your saved entries."
    msg.attach(MIMEText(body, 'plain'))

    # Attach CSV file
    attachment = BytesIO()
    dataframe.to_csv(attachment, index=False)
    attachment.seek(0)
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f"attachment; filename={filename}")
    msg.attach(part)

    # Send email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, from_password)
    server.sendmail(from_email, to_email, msg.as_string())
    server.quit()

def anxiety_assessment():
    st.subheader("Anxiety Assessment:")
    
    if "step" not in st.session_state:
        st.session_state.step = 1

    if st.session_state.step == 1:
        st.write("Do you feel like you're having an Anxiety Attack right now?")
        if st.button("Yes"):
            st.switch_page("pages/4_anxiety_attack_protocol.py")
        if st.button("No"):
            st.session_state.step = 2
            st.experimental_rerun()

    if st.session_state.step == 2:
        st.write("Are you anxious right now?")
        if st.button("Yes "):
            st.switch_page("pages/5_anxiety_protocol.py")
        if st.button("No "):
            st.session_state.step = 3
            st.experimental_rerun()

    if st.session_state.step == 3:
        show_gif()
        if st.button("Reasses your feelings"):
            st.session_state.step = 1
            st.experimental_rerun()

def show_gif():
    gif_url = "https://64.media.tumblr.com/28fad0005f6861c08f2c07697ff74aa4/tumblr_n4y0patw7Q1rn953bo1_500.gif"
    gif_html = f'<img src="{gif_url}" width="400" height="300">'
    st.markdown(gif_html, unsafe_allow_html=True)

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
            
            if new_username in st.session_state.df_users['username'].values:
                st.error("Username already exists. Please choose a different one.")
            else:
                new_user = pd.DataFrame([[new_username, new_name, hashed_password_hex]], columns=DATA_COLUMNS)
                st.session_state.df_users = pd.concat([st.session_state.df_users, new_user], ignore_index=True)
                
                st.session_state.github.write_df(DATA_FILE, st.session_state.df_users, "added new user")
                st.success("Registration successful! You can now log in.")

def authenticate(username, password):
    """ Authenticate the user. """
    login_df = st.session_state.df_users
    login_df['username'] = login_df['username'].astype(str)

    if username in login_df['username'].values:
        stored_hashed_password = login_df.loc[login_df['username'] == username, 'password'].values[0]
        stored_hashed_password_bytes = binascii.unhexlify(stored_hashed_password)
        
        if bcrypt.checkpw(password.encode('utf8'), stored_hashed_password_bytes): 
            st.session_state['authentication'] = True
            st.session_state['username'] = username
            st.success('Login successful')
            st.experimental_rerun()
        else:
            st.error('Incorrect password')
    else:
        st.error('Username not found')

# Page switching function
def switch_page(page_name):
    st.success(f"Redirecting to {page_name.replace('_', ' ')} page...")
    st.experimental_set_query_params(page=page_name)
    time.sleep(3)
    st.experimental_rerun()

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
        if st.sidebar.button("Logout"):
            st.session_state['authentication'] = False
            st.session_state.pop('username', None)
            st.switch_page("main.py")

if __name__ == "__main__":
    main()
