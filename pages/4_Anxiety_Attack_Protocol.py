import streamlit as st
import bcrypt
import binascii
import pytz
import datetime
import phonenumbers
import pandas as pd
from github_contents import GithubContents

# Constants
DATA_FILE = "MyLoginTable.csv"
DATA_COLUMNS = ['username', 'name', 'birthday', 'password', 'phone_number', 'address', 'occupation', 'emergency_contact_name', 'emergency_contact_number', 'email', 'doctor_email']
ANXIETY_ATTACK_DATA_FILE = "AnxietyAttackEntries.csv"

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
        # Ensure phone number columns are treated as strings
        st.session_state.df_users['phone_number'] = st.session_state.df_users['phone_number'].astype(str)
        st.session_state.df_users['emergency_contact_number'] = st.session_state.df_users['emergency_contact_number'].astype(str)

def login_page():
    """Login an existing user."""
    logo_path = "Logo.jpeg"
    st.image(logo_path, use_column_width=True)
    st.write("---")
    st.title("Login")
    with st.form(key='login_form'):
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        if st.form_submit_button("Login", key="login_submit"):
            authenticate(username, password)

def register_page():
    """ Register a new user. """
    st.title("Register")
    with st.form(key='register_form'):
        st.write("Please fill in the following details:")
        new_first_name = st.text_input("First Name", key="register_first_name")
        new_last_name = st.text_input("Last Name", key="register_last_name")
        new_username = st.text_input("Username", key="register_username")
        new_birthday = st.date_input("Birthday", min_value=datetime.date(1900, 1, 1), key="register_birthday")
        new_password = st.text_input("Password", type="password", key="register_password")

        if st.form_submit_button("Register", key="register_submit"):
            hashed_password = bcrypt.hashpw(new_password.encode('utf8'), bcrypt.gensalt())  # Hash the password
            hashed_password_hex = binascii.hexlify(hashed_password).decode()  # Convert hash to hexadecimal string
            new_name = f"{new_first_name} {new_last_name}"

            # Check if the username already exists
            if new_username in st.session_state.df_users['username'].values:
                st.error("Username already exists. Please choose a different one.")
                return
            else:
                new_user = pd.DataFrame([[new_username, new_name, new_birthday, hashed_password_hex, "", "", "", "", "", "", ""]], columns=DATA_COLUMNS)
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

def main():
    init_github()
    init_credentials()

    if 'authentication' not in st.session_state:
        st.session_state['authentication'] = False

    if not st.session_state['authentication']:
        options = st.sidebar.selectbox("Select a page", ["Login", "Register"], key="select_page")
        if options == "Login":
            login_page()
        elif options == "Register":
            register_page()
    else:
        st.sidebar.write(f"Logged in as {st.session_state['username']}")
        user_data = st.session_state.df_users.loc[st.session_state.df_users['username'] == st.session_state['username']]
        if not user_data.empty:
            st.session_state['emergency_contact_name'] = user_data['emergency_contact_name'].iloc[0] if 'emergency_contact_name' in user_data.columns else ''
            st.session_state['emergency_contact_number'] = user_data['emergency_contact_number'].iloc[0] if 'emergency_contact_number' in user_data.columns else ''

        anxiety_attack_protocol()

        logout_button = st.sidebar.button("Logout", key="logout_button")
        if logout_button:
            st.session_state['authentication'] = False
            st.session_state.pop('username', None)
            st.switch_page("Main.py")
            st.experimental_rerun()

def anxiety_attack_protocol():
    username = st.session_state['username']
    data_file = f"{username}_anxiety_attack_data.csv"

    if 'data' not in st.session_state:
        if st.session_state.github.file_exists(data_file):
            st.session_state.data = st.session_state.github.read_df(data_file)
        else:
            st.session_state.data = pd.DataFrame(columns=['Date', 'Time', 'Severity', 'Symptoms', 'Triggers', 'Help'])

    st.title("Anxiety Attack Protocol")

    # Question 1: Date
    date_selected = st.date_input("Date", value=datetime.date.today(), key="protocol_date")

    # Question 2: Time & Severity
    add_time_severity()

    # Question 3: Symptoms
    st.subheader("Symptoms:")
    col1, col2 = st.columns(2)
    with col1:
        symptoms_anxiety = st.checkbox("Anxiety", key="symptom_anxiety")
        symptoms_chestpain = st.checkbox("Chest Pain", key="symptom_chestpain")
        symptoms_chills = st.checkbox("Chills", key="symptom_chills")
        symptoms_chocking = st.checkbox("Chocking", key="symptom_chocking")
        symptoms_cold = st.checkbox("Cold", key="symptom_cold")
        symptoms_coldhands = st.checkbox("Cold Hands", key="symptom_coldhands")
        symptoms_dizziness = st.checkbox("Dizziness", key="symptom_dizziness")
        symptoms_feelingdanger = st.checkbox("Feeling of danger", key="symptom_feelingdanger")
        symptoms_feelingdread = st.checkbox("Feeling of dread", key="symptom_feelingdread")
        symptoms_heartracing = st.checkbox("Heart racing", key="symptom_heartracing")
        symptoms_hotflushes = st.checkbox("Hot flushes", key="symptom_hotflushes")
        symptoms_irrationalthinking = st.checkbox("Irrational thinking", key="symptom_irrationalthinking")
    with col2:
        symptoms_nausea = st.checkbox("Nausea", key="symptom_nausea")
        symptoms_nervous = st.checkbox("Nervousness", key="symptom_nervous")
        symptoms_numbhands = st.checkbox("Numb Hands", key="symptom_numbhands")
        symptoms_numbness = st.checkbox("Numbness", key="symptom_numbness")
        symptoms_palpitations = st.checkbox("Palpitations", key="symptom_palpitations")
        symptoms_shortbreath = st.checkbox("Shortness of Breath", key="symptom_shortbreath")
        symptoms_sweating = st.checkbox("Sweating", key="symptom_sweating")
        symptoms_tensemuscles = st.checkbox("Tense Muscles", key="symptom_tensemuscles")
        symptoms_tinglyhands = st.checkbox("Tingly Hands", key="symptom_tinglyhands")
        symptoms_trembling = st.checkbox("Trembling", key="symptom_trembling")
        symptoms_tremor = st.checkbox("Tremor", key="symptom_tremor")
        symptoms_weakness = st.checkbox("Weakness", key="symptom_weakness")

    # Display existing symptoms
    if 'symptoms' not in st.session_state:
        st.session_state.symptoms = []

    for symptom in st.session_state.symptoms:
        st.write(symptom)

    new_symptom = st.text_input("Add new symptom:", key="new_symptom")
    if st.button("Add Symptom", key="add_symptom_button") and new_symptom:
        st.session_state.symptoms.append(new_symptom)

    # Question 4: Triggers
    st.subheader("Triggers:")
    triggers = st.multiselect("Select Triggers", ["Stress", "Caffeine", "Lack of Sleep", "Social Event", "Reminder of traumatic event", "Alcohol", "Conflict", "Family problems"], key="triggers")

    if 'triggers' not in st.session_state:
        st.session_state.triggers = []

    new_trigger = st.text_input("Add new trigger:", key="new_trigger")
    if st.button("Add Trigger", key="add_trigger_button") and new_trigger:
        st.session_state.triggers.append(new_trigger)

    for trigger in st.session_state.triggers:
        st.write(trigger)

    # Question 5: Did something Help against the attack?
    st.subheader("Did something Help against the attack?")
    help_response = st.text_area("Write your response here", height=100, key="help_response")

    if st.button("Save Entry", key="save_entry_button"):
        new_entry = {
            'Date': date_selected,
            'Time': [entry['time'] for entry in st.session_state.time_severity_entries],
            'Severity': [entry['severity'] for entry in st.session_state.time_severity_entries],
            'Symptoms': st.session_state.symptoms,
            'Triggers': triggers,
            'Help': help_response
        }
        st.switch_page("pages/3_Profile.py")
        new_entry_df = pd.DataFrame([new_entry])

        # Append the new entry to the existing data DataFrame
        st.session_state.data = pd.concat([st.session_state.data, new_entry_df], ignore_index=True)

        # Save the updated DataFrame to the user's specific CSV file on GitHub
        st.session_state.github.write_df(data_file, st.session_state.data, "added new entry")
        st.success("Entry saved successfully!")

        # Clear the severity entries after saving
        st.session_state.time_severity_entries = []

def add_time_severity():
    if 'time_severity_entries' not in st.session_state:
        st.session_state.time_severity_entries = []

    st.subheader("Time & Severity")

    # Display the current time
    current_time = datetime.datetime.now(pytz.timezone('Europe/Zurich')).strftime('%H:%M')
    st.write(f"Current Time: {current_time}")

    # Button to add a new time-severity entry
    with st.form(key='severity_form'):
        severity = st.slider("Severity (1-10)", min_value=1, max_value=10, key="severity_slider")
        if st.form_submit_button("Add Severity", key="add_severity_button"):
            new_entry = {
                'time': current_time,
                'severity': severity
            }
            st.session_state.time_severity_entries.append(new_entry)
            st.success(f"Added entry: Time: {current_time}, Severity: {severity}")

    # Display all time-severity entries
    for entry in st.session_state.time_severity_entries:
        st.write(f"Time: {entry['time']}, Severity: {entry['severity']}")

def format_phone_number(number):
    """Format phone number using phonenumbers library."""
    if not number or pd.isna(number) or number == 'nan':
        return None
    number_str = str(number).strip()
    if number_str.endswith('.0'):
        number_str = number_str[:-2]  # Remove trailing '.0'
    try:
        phone_number = phonenumbers.parse(number_str, "CH")  # "CH" is for Switzerland
        if phonenumbers.is_valid_number(phone_number):
            return phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.E164)
        else:
            return number_str  # Return the original number if invalid
    except phonenumbers.NumberParseException:
        return number_str  # Return the original number if parsing fails

def display_emergency_contact():
    """Display the emergency contact in the sidebar if it exists."""
    if 'emergency_contact_name' in st.session_state and 'emergency_contact_number' in st.session_state:
        emergency_contact_name = st.session_state['emergency_contact_name']
        emergency_contact_number = st.session_state['emergency_contact_number']

        if emergency_contact_number:
            formatted_emergency_contact_number = format_phone_number(emergency_contact_number)
            st.sidebar.write(f"Emergency Contact: {emergency_contact_name}")
            if formatted_emergency_contact_number:
                st.sidebar.markdown(f"[{formatted_emergency_contact_number}](tel:{formatted_emergency_contact_number})")
            else:
                st.sidebar.write("No valid emergency contact number available.")
        else:
            st.sidebar.write("No emergency contact number available.")
    else:
        st.sidebar.write("No emergency contact information available.")

def switch_page(page_name):
    st.success(f"Redirecting to {page_name.replace('_', ' ')} page...")
    time.sleep(3)
    st.experimental_set_query_params(page=page_name)
    st.experimental_rerun()

if __name__ == "__main__":
    main()
    display_emergency_contact()
