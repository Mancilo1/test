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

def main():
    init_github()
    init_credentials()

    if 'authentication' not in st.session_state or not st.session_state['authentication']:
        st.error("You must log in first.")
        return

    user_data = st.session_state.df_users.loc[st.session_state.df_users['username'] == st.session_state['username']]
    if not user_data.empty:
        st.session_state['emergency_contact_name'] = user_data['emergency_contact_name'].iloc[0] if 'emergency_contact_name' in user_data.columns else ''
        st.session_state['emergency_contact_number'] = user_data['emergency_contact_number'].iloc[0] if 'emergency_contact_number' in user_data.columns else ''

    anxiety_attack_protocol()

    if st.sidebar.button("Logout"):
        st.session_state['authentication'] = False
        st.session_state.pop('username', None)
        st.experimental_rerun()

def anxiety_attack_protocol():
    username = st.session_state['username']
    data_file = f"{username}_anxiety_attack_data.csv"
    
    if 'anxiety_attack_data' not in st.session_state:
        if st.session_state.github.file_exists(data_file):
            st.session_state.anxiety_attack_data = st.session_state.github.read_df(data_file)
        else:
            st.session_state.anxiety_attack_data = pd.DataFrame(columns=['Date', 'Time', 'Severity', 'Symptoms', 'Triggers', 'Help'])

    st.title("Anxiety Attack Protocol")

    # Question 1: Date
    date_selected = st.date_input("Date", value=datetime.date.today())

    # Question 2: Time & Severity
    add_time_severity()

    # Question 3: Symptoms
    st.subheader("Symptoms:")
    symptoms = []
    col1, col2 = st.columns(2)
    with col1:
        symptoms.extend([
            "Anxiety" if st.checkbox("Anxiety") else "",
            "Chest Pain" if st.checkbox("Chest Pain") else "",
            "Chills" if st.checkbox("Chills") else "",
            "Chocking" if st.checkbox("Chocking") else "",
            "Cold" if st.checkbox("Cold") else "",
            "Cold Hands" if st.checkbox("Cold Hands") else "",
            "Dizziness" if st.checkbox("Dizziness") else "",
            "Feeling of danger" if st.checkbox("Feeling of danger") else "",
            "Feeling of dread" if st.checkbox("Feeling of dread") else "",
            "Heart racing" if st.checkbox("Heart racing") else "",
            "Hot flushes" if st.checkbox("Hot flushes") else "",
            "Irrational thinking" if st.checkbox("Irrational thinking") else ""
        ])
    with col2:
        symptoms.extend([
            "Nausea" if st.checkbox("Nausea") else "",
            "Nervousness" if st.checkbox("Nervousness") else "",
            "Numb Hands" if st.checkbox("Numb Hands") else "",
            "Numbness" if st.checkbox("Numbness") else "",
            "Palpitations" if st.checkbox("Palpitations") else "",
            "Shortness of Breath" if st.checkbox("Shortness of Breath") else "",
            "Sweating" if st.checkbox("Sweating") else "",
            "Tense Muscles" if st.checkbox("Tense Muscles") else "",
            "Tingly Hands" if st.checkbox("Tingly Hands") else "",
            "Trembling" if st.checkbox("Trembling") else "",
            "Tremor" if st.checkbox("Tremor") else "",
            "Weakness" if st.checkbox("Weakness") else ""
        ])
    symptoms = [symptom for symptom in symptoms if symptom]

    # Question 4: Triggers
    st.subheader("Triggers:")
    triggers = st.multiselect("Select Triggers", ["Stress", "Caffeine", "Lack of Sleep", "Social Event", "Reminder of traumatic event", "Alcohol", "Conflict", "Family problems"])
    
    if 'triggers' not in st.session_state:
        st.session_state.triggers = []

    new_trigger = st.text_input("Add new trigger:")
    if st.button("Add Trigger") and new_trigger:
        st.session_state.triggers.append(new_trigger)

    for trigger in st.session_state.triggers:
        st.write(trigger)

    # Question 5: Did something Help against the attack?
    st.subheader("Did something Help against the attack?")
    help_response = st.text_area("Write your response here", height=100)

    if st.button("Save Entry"):
        new_entry = {
            'Date': date_selected,
            'Time': [entry['time'] for entry in st.session_state.time_severity_entries],
            'Severity': [entry['severity'] for entry in st.session_state.time_severity_entries],
            'Symptoms': ", ".join(symptoms),
            'Triggers': ", ".join(triggers),
            'Help': help_response
        }
        new_entry_df = pd.DataFrame([new_entry])

        st.session_state.anxiety_attack_data = pd.concat([st.session_state.anxiety_attack_data, new_entry_df], ignore_index=True)
        st.session_state.github.write_df(data_file, st.session_state.anxiety_attack_data, "added new entry")
        st.success("Entry saved successfully!")
        st.experimental_rerun()

def add_time_severity():
    if 'time_severity_entries' not in st.session_state:
        st.session_state.time_severity_entries = []

    st.subheader("Time & Severity")

    # Display the current time
    current_time = datetime.datetime.now(pytz.timezone('Europe/Zurich')).strftime('%H:%M')
    st.write(f"Current Time: {current_time}")

    # Add severity form
    with st.form(key='severity_form'):
        severity = st.slider("Severity (1-10)", min_value=1, max_value=10, key="severity_slider")
        if st.form_submit_button("Add Severity"):
            new_entry = {
                'time': current_time,
                'severity': severity
            }
            st.session_state.time_severity_entries.append(new_entry)
            st.success(f"Added entry: Time: {current_time}, Severity: {severity}")

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
        emergency_contact_name = st.session_state.emergency_contact_name
        emergency_contact_number = st.session_state.emergency_contact_number

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
    st.experimental_set_query_params(page=page_name)
    st.experimental_rerun()

if __name__ == "__main__":
    main()
    display_emergency_contact()
