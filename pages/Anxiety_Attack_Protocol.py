import streamlit as st
import datetime

def show():
    st.title("Anxiety Attack Protocol")

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

if __name__ == "__main__":
    main_page()
