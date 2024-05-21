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
    st.title("Anxiety Attack Protocol")

def anxiety_attack_protocol():
    # Check if the session state object exists, if not, initialize it
    if 'button_count' not in st.session_state:
        st.session_state.button_count = 0
        st.session_state.times = []
        st.session_state.severities = []
        st.session_state.symptoms = []
        st.session_state.triggers = []

    st.write("Anxiety Attack Protocol")

    # Question 1: Date
    date_selected = st.date_input("Date", value=datetime.date.today())

    # Question 2: Time & Severity
    add_time_severity()

    # Question 3: Symptoms
    st.subheader("Symptoms:")
    col1, col2 = st.columns(2)
    symptoms = []
    with col1:
        if st.checkbox("Anxiety"):
            symptoms.append("Anxiety")
        if st.checkbox("Chest Pain"):
            symptoms.append("Chest Pain")
        if st.checkbox("Chills"):
            symptoms.append("Chills")
        if st.checkbox("Chocking"):
            symptoms.append("Chocking")
        if st.checkbox("Cold"):
            symptoms.append("Cold")
        if st.checkbox("Cold Hands"):
            symptoms.append("Cold Hands")
        if st.checkbox("Dizziness"):
            symptoms.append("Dizziness")
        if st.checkbox("Feeling of danger"):
            symptoms.append("Feeling of danger")
        if st.checkbox("Feeling of dread"):
            symptoms.append("Feeling of dread")
        if st.checkbox("Heart racing"):
            symptoms.append("Heart racing")
        if st.checkbox("Hot flushes"):
            symptoms.append("Hot flushes")
        if st.checkbox("Irrational thinking"):
            symptoms.append("Irrational thinking")
    with col2:
        if st.checkbox("Nausea"):
            symptoms.append("Nausea")
        if st.checkbox("Nervousness"):
            symptoms.append("Nervousness")
        if st.checkbox("Numb Hands"):
            symptoms.append("Numb Hands")
        if st.checkbox("Numbness"):
            symptoms.append("Numbness")
        if st.checkbox("Palpitations"):
            symptoms.append("Palpitations")
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
    
    new_symptom = st.text_input("Add new symptom:")
    if st.button("Add Symptom") and new_symptom:
        st.session_state.symptoms.append(new_symptom)
        symptoms.append(new_symptom)

    # Question 4: Triggers
    st.subheader("Triggers:")
    selected_triggers = st.multiselect("Select Triggers", ["Stress", "Caffeine", "Lack of Sleep", "Social Event", "Reminder of traumatic event", "Alcohol", "Conflict", "Family problems"])
    if selected_triggers:
        st.session_state.triggers.extend(selected_triggers)

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
            ", ".join(st.session_state.triggers),
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

