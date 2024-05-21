import streamlit as st
from PIL import Image
import time

def show():
    st.image("Logo.jpeg", width=600)
    st.write("---")
    
    st.write("Anxiety Assessment:")
    
    answer = st.radio("Do you feel like you're having an Anxiety Attack right now?", ("Yes", "No"))
    if answer == "Yes":
        st.write("Redirecting to Anxiety Attack Protocol page...")
        time.sleep(2)  # Optional: kleine Verzögerung, um die Nachricht anzuzeigen
        redirect_to_page("Anxiety_Attack_Protocol")
    else:
        answer_2 = st.radio("Are you anxious right now?", ("Yes", "No"))
        if answer_2 == "Yes":
            st.write("Redirecting to Anxiety Protocol page...")
            time.sleep(2)  # Optional: kleine Verzögerung, um die Nachricht anzuzeigen
            redirect_to_page("Anxiety_protocol")
        else:
            st.write("Reassess your feelings.")

def redirect_to_page(page_name):
    if page_name == "Anxiety_Attack_Protocol":
        st.success("Redirecting to Anxiety Attack Protocol page...")
        # Fügen Sie hier die Logik hinzu, um zur Seite Anxiety_Attack_Protocol zu wechseln
    elif page_name == "Anxiety_protocol":
        st.success("Redirecting to Anxiety Protocol page...")
        # Fügen Sie hier die Logik hinzu, um zur Seite Anxiety_protocol zu wechseln

if __name__ == "__main__":
    show()
