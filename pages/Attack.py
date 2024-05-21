import streamlit as st
from PIL import Image
from pages import Anxiety_Attack_Protocol, Anxiety_protocol

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
