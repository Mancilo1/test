import streamlit as st
from PIL import Image
from pages import Anxiety_Attack_Protocol, Anxiety_protocol
import os

def switch_pages(page_name):
    """Switches to the specified page."""
    if page_name == "Anxiety_protocol":
        file_path = os.path.join("pages", "Anxiety_protocol.py")
        if os.path.exists(file_path):
            st.success("Redirecting to Anxiety Protocol page...")
            os.system("streamlit run pages/Anxiety_protocol.py")
        else:
            st.error("Anxiety_protocol.py file not found.")
    elif page_name == "Anxiety_Attack_Protocol":
        st.success("Redirecting to Anxiety Attack Protocol page...")
        # Fügen Sie hier die Logik hinzu, um zur Seite Anxiety_Attack_Protocol zu wechseln
    else:
        st.error("Unknown page: {}".format(page_name))

def show():
    st.image("Logo.jpeg", width=600)
    st.write("---")
    
    st.write("Anxiety Assessment:")
    
    answer = st.radio("Do you feel like you're having an Anxiety Attack right now?", ("Yes", "No"))
    if answer == "Yes":
        switch_pages("Anxiety_Attack_Protocol")
    else:
        answer_2 = st.radio("Are you anxious right now?", ("Yes", "No"))
        if answer_2 == "Yes":
            switch_pages("Anxiety_protocol")
        else:
            st.write("Reassess your feelings.")

if __name__ == "__main__":
    show()
