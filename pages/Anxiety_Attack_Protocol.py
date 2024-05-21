import streamlit as st
import datetime
import csv
import os

def show():
    st.title("Anxiety Attack Protocol")

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

def anxiety_attack_protocol():
    # Check if the session state object exists, if not, initialize it
    if 'button_count' not in st.session_state:
        st.session_state.button_count = 0
        st.session_state.times = []
        st.session_state.severities = []

    st.write("Anxiety Attack Protocol")

    # Question 1: Date
    date_selected = st.date_input("Date", value=datetime.date.today())

    # Question 2: Time & Severity
    add_time_severity()

    # Question 3: Symptoms
    st.subheader("Symptoms:")
    col1, col2 = st.columns(2)
    with col1:
        symptoms_anxiety = st.checkbox("Anxiety")
        symptoms_chestpain = st.checkbox("Chest Pain")
        symptoms_chills = st.checkbox("Chills")
        symptoms_chocking = st.checkbox("Chocking")
        symptoms_cold = st.checkbox("Cold")
        symptoms_coldhands = st.checkbox("Cold Hands")
        symptoms_dizziness = st.checkbox("Dizziness")
        symptoms_feelingdanger = st.checkbox("Feeling of danger")
        symptoms_feelingdread = st.checkbox("Feeling of dread")
        symptoms_heartracing = st.checkbox("Heart racing")
        symptoms_hotflushes = st.checkbox("Hot flushes")
        symptoms_irrationalthinking = st.checkbox("Irrational thinking")
    with col2:
        symptoms_nausea = st.checkbox("Nausea")
        symptoms_nervous = st.checkbox("Nervousness")
        symptoms_numbhands = st.checkbox("Numb Hands")
        symptoms_numbness = st.checkbox("Numbness")
        symptoms_palpitations = st.checkbox("Palpitations")
        symptoms_shortbreath = st.checkbox("Shortness of Breath")
        symptoms_sweating = st.checkbox("Sweating")
        symptoms_tensemuscles = st.checkbox("Tense Muscles")
        symptoms_tinglyhands = st.checkbox("Tingly Hands")
        symptoms_trembling = st.checkbox("Trembling")
        symptoms_tremor = st.checkbox("Tremor")
        symptoms_weakness = st.checkbox("Weakness")
    if 'symptoms' not in st.session_state:
        st.session_state.symptoms = []

     # Gather selected symptoms
    symptoms = []
    if symptoms_anxiety: symptoms.append("Anxiety")
    if symptoms_chestpain: symptoms.append("Chest Pain")
    if symptoms_chills: symptoms.append("Chills")
    if symptoms_chocking: symptoms.append("Chocking")
    if symptoms_cold: symptoms.append("Cold")
    if symptoms_coldhands: symptoms.append("Cold Hands")
    if symptoms_dizziness: symptoms.append("Dizziness")
    if symptoms_feelingdanger: symptoms.append("Feeling of danger")
    if symptoms_feelingdread: symptoms.append("Feeling of dread")
    if symptoms_heartracing: symptoms.append("Heart racing")
    if symptoms_hotflushes: symptoms.append("Hot flushes")
    if symptoms_irrationalthinking: symptoms.append("Irrational thinking")
    if symptoms_nausea: symptoms.append("Nausea")
    if symptoms_nervous: symptoms.append("Nervousness")
    if symptoms_numbhands: symptoms.append("Numb Hands")
    if symptoms_numbness: symptoms.append("Numbness")
    if symptoms_palpitations: symptoms.append("Palpitations")
    if symptoms_shortbreath: symptoms.append("Shortness of Breath")
    if symptoms_sweating: symptoms.append("Sweating")
    if symptoms_tensemuscles: symptoms.append("Tense Muscles")
    if symptoms_tinglyhands: symptoms.append("Tingly Hands")
    if symptoms_trembling: symptoms.append("Trembling")
    if symptoms_tremor: symptoms.append("Tremor")
    if symptoms_weakness: symptoms.append("Weakness")

    # Display existing symptoms
    for symptom in st.session_state.symptoms:
        st.write(symptom)

    new_symptom = st.text_input("Add new symptom:")
    if st.button("Add Symptom") and new_symptom:
        st.session_state.symptoms.append(new_symptom)

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
    
    # Save the data to CSV when the form is submitted
    if st.button("Save Data"):
        time_severity_pairs = st.session_state.times
        data = [
            date_selected,
            "; ".join([f"{time.strftime('%H:%M')} - {severity}" for time, severity in time_severity_pairs]),
            ", ".join(symptoms),
            ", ".join(triggers),
            help_response
        ]
        save_to_csv(data)
        st.success("Data saved successfully!")


def add_time_severity():
    st.subheader("Time & Severity")
    
    # Initialize times list if not already initialized
    if 'times' not in st.session_state:
        st.session_state.times = []

    for i in range(st.session_state.button_count + 1):
        if i < len(st.session_state.times):
            time_selected, severity = st.session_state.times[i]
        else:
            time_selected = datetime.datetime.now().time()
            severity = 1

        # Convert time_selected to string with minute precision
        time_selected_str = time_selected.strftime('%H:%M')
        
        # Display time input with minute precision
        time_selected_str = st.text_input(f"Time {i+1}", value=time_selected_str)
        
        # Convert the string back to datetime.time object
        time_selected = datetime.datetime.strptime(time_selected_str, '%H:%M').time()
        
        severity = st.slider(f"Severity (1-10) {i+1}", min_value=1, max_value=10, value=severity)
        
        # Update time and severity in session state
        if len(st.session_state.times) <= i:
            st.session_state.times.append((time_selected, severity))
        else:
            st.session_state.times[i] = (time_selected, severity)

    if st.button("Add Time & Severity"):
        st.session_state.button_count += 1

def main_page():
    st.title("FeelNow")
    anxiety_attack_protocol()
    
 # Display saved data
    st.header("Saved Data")
    data = read_csv()
    if data:
        st.write("## Anxiety Attack Protocol Data")
        st.table(data)
    else:
        st.write("No data available")


if __name__ == "__main__":
    main_page()
