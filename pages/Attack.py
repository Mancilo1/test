import streamlit as st
from PIL import Image
import time
import navigation  # Importieren Sie die navigation.py-Datei

def show():
    st.image("Logo.jpeg", width=600)
    st.write("---")
    
    st.write("Anxiety Assessment:")
    
    answer = st.radio("Do you feel like you're having an Anxiety Attack right now?", ("Yes", "No"))
    if answer == "Yes":
        navigation.switch_pages("Anxiety_Attack_Protocol")  # Verwenden Sie die switch_pages()-Funktion
    else:
        answer_2 = st.radio("Are you anxious right now?", ("Yes", "No"))
        if answer_2 == "Yes":
            navigation.switch_pages("Anxiety_protocol")  # Verwenden Sie die switch_pages()-Funktion
        else:
            st.write("Reassess your feelings.")

if __name__ == "__main__":
    show()

