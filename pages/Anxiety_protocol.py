import streamlit as st
import datetime
import csv
import os

def save_to_csv(data, filename='anxiety_data.csv'):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

def read_csv(filename='anxiety_data.csv'):
    if os.path.exists(filename):
        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            return list(reader)
    return []

def show():
    st.title("Anxiety Protocol")

def anxiety_protocol():
    # Check if the session state object exists, if not, initialize it
    if 'button_count' not in st.session_state:
        st.session_state.button_count = 0
        st.session_state.times = []
        st.session_state.severities = []
        st.session_state.symptoms = []

    st.write("Anxiety Protocol Page")

    # Question 1: Date
    date_selected = st.date_input("Date", value=datetime.date.today())

    # Question 2: Where are you
    st.subheader("Where are you and what is the environment?")
    location_response = st.text_area("Write your response here", key="location", height=100)
    
    st.subheader("Try to describe your anxiety right now?")
    anxiety_description_response = st.text_area("Write your response here", key="anxiety_description", height=100)

    st.subheader("What do you think could be the cause?")
    cause_response = st.text_area("Write your response here", key="cause", height=100)
    
    st.subheader("Any specific triggers? For example Stress, Caffeine, Lack of Sleep, Social Event, Reminder of traumatic event")
    triggers_response = st.text_area("Write your response here", key="triggers", height=100)

    # Question 3: Symptoms
    st.subheader("Symptoms:")
    col1, col2 = st.columns(2)
    symptoms = []
    with col1:
        if st.checkbox("Chest Pain"):
            symptoms.append("Chest Pain")
        if st.checkbox("Chills"):
            symptoms.append("Chills")
        if st.checkbox("Cold"):
            symptoms.append("Cold")
        if st.checkbox("Cold Hands"):
            symptoms.append("Cold Hands")
        if st.checkbox("Dizziness"):
            symptoms.append("Dizziness")
        if st.checkbox("Feeling of danger"):
            symptoms.append("Feeling of danger")
        if st.checkbox("Heart racing"):
            symptoms.append("Heart racing")
        if st.checkbox("Hot flushes"):
            symptoms.append("Hot flushes")
    with col2:
        if st.checkbox("Nausea"):
            symptoms.append("Nausea")
        if st.checkbox("Nervousness"):
            symptoms.append("Nervousness")
        if st.checkbox("Numb Hands"):
            symptoms.append("Numb Hands")
        if st.checkbox("Numbness"):
            symptoms.append("Numbness")
        if st.checkbox("Shortness of Breath"):
            symptoms.append("Shortness of Breath")
        if st.checkbox("Sweating"):
            symptoms.append("Sweating")
        if st.checkbox("Tense Muscles"):
            symptoms.append("Tense Muscles")
        if st.checkbox("Tingly Hands"):
            symptoms.append("Tingly Hands")
        if st.checkbox("Trembling"):
            symptoms.append("Trembling")
        if st.checkbox("Tremor"):
            symptoms.append("Tremor")
        if st.checkbox("Weakness"):
            symptoms.append("Weakness")
    
    new_symptom = st.text_input("Add new symptom:", key="new_symptom")
    if st.button("Add Symptom") and new_symptom:
        st.session_state.symptoms.append(new_symptom)
        symptoms.append(new_symptom)

    # Question 5: Did something Help against the attack?
    st.subheader("Did something Help against the Anxiety?")
    help_response = st.text_area("Write your response here", key="help_response", height=100)
    
    # Save the data to CSV when the form is submitted
    if st.button("Save Data"):
        data = [
            date_selected,
            location_response,
            anxiety_description_response,
            cause_response,
            triggers_response,
            ", ".join(symptoms),
            help_response
        ]
        save_to_csv(data)
        st.success("Data saved successfully!")

def main_page():
    st.title("FeelNow")
    anxiety_protocol()
    
    # Display saved data
    st.header("Saved Data")
    data = read_csv()
    if data:
        st.write("## Anxiety Protocol Data")
        st.table(data)
    else:
        st.write("No data available")

if __name__ == "__main__":
    main_page()

