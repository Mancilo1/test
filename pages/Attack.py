import streamlit as st
from PIL import Image
from pages import Anxiety_Attack_Protocol, Anxiety_protocol
import os

def show():
    st.image("Logo.jpeg", width=600)
    st.write("---")
    
    st.write("Anxiety Assessment:")
    
    st.write("Do you feel like you're having an Anxiety Attack right now?")
    if st.button("Yes"):
        anxiety_attack_protocol()
    elif st.button("No"):
        redirect_question_2()
        if st.button("Yes "):
            anxiety_protocol()
        elif st.button("No "):
            No_2_question()

def switch_page(page_name):
    if page_name == "Anxiety_protocol":
        file_path = os.path.join("pages", "Anxiety_protocol.py")
        if os.path.exists(file_path):
            os.system("streamlit run pages/Anxiety_protocol.py")
        else:
            st.error("Anxiety_protocol.py file not found.")
    elif page_name == "anxiety_attack_protocol":
        # Logik für die Dashboard-Seite
        st.title("pages", "Anxiety_Attack_protocol")
        st.write("Switched to Dashboard page.")


def anxiety_attack_protocol():
    st.write("Redirecting to Anxiety Attack Protocol page...")

def redirect_question_2():
    st.write("Are you anxious right now?")

def anxiety_protocol():
    st.write("Redirecting to Anxiety Protocol page...")

def No_2_question():
    st.experimental_rerun()

if __name__ == "__main__":
    show()
