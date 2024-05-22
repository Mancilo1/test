import streamlit as st
import datetime
import csv
import os

def save_to_csv(data, filename='anxiety_protocol_data.csv'):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

def read_csv(filename='anxiety_protocol_data.csv'):
    if os.path.exists(filename):
        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            return list(reader)
    return []

def anxiety_protocol():
    # Check if the session state object exists, if not, initialize it
    if 'symptoms' not in st.session_state:
        st.session_state.symptoms = []

    st.write("Anxiety Protocol Page")

    # Question 1: Date
    date_selected = st.date_input("Date", value=datetime.date.today())

    # Question 2: Where are you
    st.subheader("Where are you and what is the environment?")
    location_response = st.text_area("Write your response here", key="location", height=100)
    
    st.subheader("Try to describe your anxiety right now")
    anxiety_description = st.text_area("Write your response here", key="anxiety_description", height=100)

    st.subheader("What do you think could be the cause?")
    cause_response = st.text_area("Write your response here", key="cause", height=100)
    
    st.subheader("Any specific triggers? For example Stress, Caffeine, Lack of Sleep, Social Event, Reminder of traumatic event")
    triggers_response = st.text_area("Write your response here", key="triggers", height=100)

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
    
    # Gather selected symptoms
    symptoms = []
    if symptoms_chestpain: symptoms.append("Chest Pain")
    if symptoms_chills: symptoms.append("Chills")
    if symptoms_cold: symptoms.append("Cold")
    if symptoms_coldhands: symptoms.append("Cold Hands")
    if symptoms_dizziness: symptoms.append("Dizziness")
    if symptoms_feelingdanger: symptoms.append("Feeling of danger")
    if symptoms_heartracing: symptoms.append("Heart racing")
    if symptoms_hotflushes: symptoms.append("Hot flushes")
    if symptoms_nausea: symptoms.append("Nausea")
    if symptoms_nervous: symptoms.append("Nervousness")
    if symptoms_numbhands: symptoms.append("Numb Hands")
    if symptoms_numbness: symptoms.append("Numbness")
    if symptoms_shortbreath: symptoms.append("Shortness of Breath")
    if symptoms_sweating: symptoms.append("Sweating")
    if symptoms_tensemuscles: symptoms.append("Tense Muscles")
    if symptoms_tinglyhands: symptoms.append("Tingly Hands")
    if symptoms_trembling: symptoms.append("Trembling")
    if symptoms_tremor: symptoms.append("Tremor")
    if symptoms_weakness: symptoms.append("Weakness")
    
    new_symptom = st.text_input("Add new symptom:", key="new_symptom")
    if st.button("Add Symptom") and new_symptom:
        st.session_state.symptoms.append(new_symptom)

    # Question 5: Did something Help against the Anxiety?
    st.subheader("Did something help against the anxiety?")
    help_response = st.text_area("Write your response here", key="help_response", height=100)
    
    # Save the data to CSV when the form is submitted
    if st.button("Save Data"):
        data = [
            date_selected,
            location_response,
            anxiety_description,
            cause_response,
            triggers_response,
            ", ".join(symptoms + st.session_state.symptoms),
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
    show()


