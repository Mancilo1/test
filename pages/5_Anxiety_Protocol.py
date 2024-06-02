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

    anxiety_protocol()

    if st.sidebar.button("Logout"):
        st.session_state['authentication'] = False
        st.session_state.pop('username', None)
        st.experimental_rerun()

def anxiety_protocol():
    username = st.session_state['username']
    data_file = f"{username}_anxiety_protocol_data.csv"
    
    if 'anxiety_data' not in st.session_state:
        if st.session_state.github.file_exists(data_file):
            st.session_state.anxiety_data = st.session_state.github.read_df(data_file)
        else:
            st.session_state.anxiety_data = pd.DataFrame(columns=['Date', 'Location', 'Anxiety Description', 'Cause', 'Triggers', 'Symptoms', 'Help'])

    st.title("Anxiety Protocol")

    # Question 1: Date
    date_selected = st.date_input("Date", value=datetime.date.today())

    # Question 2: Where are you
    st.subheader("Where are you and what is the environment?")
    location = st.text_area("Write your response here", key="location", height=100)
    
    st.subheader("Try to describe your anxiety right now?")
    anxiety_description = st.text_area("Write your response here", key="anxiety_description", height=100)

    st.subheader("What do you think could be the cause?")
    cause = st.text_area("Write your response here", key="cause", height=100)
    
    st.subheader("Any specific triggers?")
    st.write("For example Stress, Caffeine, Lack of Sleep, Social Event, Reminder of traumatic event.")
    triggers = st.text_area("Write your response here", key="triggers", height=100)

    # Question 3: Symptoms
    st.subheader("Symptoms:")
    symptoms_list = []
    col1, col2 = st.columns(2)
    with col1:
        if st.checkbox("Chest Pain"): symptoms_list.append("Chest Pain")
        if st.checkbox("Chills"): symptoms_list.append("Chills")
        if st.checkbox("Cold"): symptoms_list.append("Cold")
        if st.checkbox("Cold Hands"): symptoms_list.append("Cold Hands")
        if st.checkbox("Dizziness"): symptoms_list.append("Dizziness")
        if st.checkbox("Feeling of danger"): symptoms_list.append("Feeling of danger")
        if st.checkbox("Heart racing"): symptoms_list.append("Heart racing")
        if st.checkbox("Hot flushes"): symptoms_list.append("Hot flushes")
        if st.checkbox("Nausea"): symptoms_list.append("Nausea")
        if st.checkbox("Nervousness"): symptoms_list.append("Nervousness")
    with col2:
        if st.checkbox("Numb Hands"): symptoms_list.append("Numb Hands")
        if st.checkbox("Numbness"): symptoms_list.append("Numbness")
        if st.checkbox("Shortness of Breath"): symptoms_list.append("Shortness of Breath")
        if st.checkbox("Sweating"): symptoms_list.append("Sweating")
        if st.checkbox("Tense Muscles"): symptoms_list.append("Tense Muscles")
        if st.checkbox("Tingly Hands"): symptoms_list.append("Tingly Hands")
        if st.checkbox("Trembling"): symptoms_list.append("Trembling")
        if st.checkbox("Tremor"): symptoms_list.append("Tremor")
        if st.checkbox("Weakness"): symptoms_list.append("Weakness")

    # Display existing symptoms
    if 'symptoms' not in st.session_state:
        st.session_state.symptoms = []

    for symptom in st.session_state.symptoms:
        st.write(symptom)

    new_symptom = st.text_input("Add new symptom:", key="new_symptom")
    if st.button("Add Symptom") and new_symptom:
        st.session_state.symptoms.append(new_symptom)

    # Question 5: Did something Help against the attack?
    st.subheader("Did something Help against the Anxiety?")
    help_response = st.text_area("Write your response here", key="help_response", height=100)

    if st.button("Save Entry"):
        new_entry = {
            'Date': date_selected,
            'Location': location,
            'Anxiety Description': anxiety_description,
            'Cause': cause,
            'Triggers': triggers,
            'Symptoms': ", ".join(symptoms_list),
            'Help': help_response
        }
        new_entry_df = pd.DataFrame([new_entry])

        st.session_state.anxiety_data = pd.concat([st.session_state.anxiety_data, new_entry_df], ignore_index=True)
        st.session_state.github.write_df(data_file, st.session_state.anxiety_data, "added new entry")
        st.success("Entry saved successfully!")
        st.experimental_rerun()

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
