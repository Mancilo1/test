import streamlit as st
from PIL import Image
import time

def show():
    st.image("Logo.jpeg", width=600)
    st.write("---")
    
    st.write("Anxiety Assessment:")
    
    answer = st.radio("Do you feel like you're having an Anxiety Attack right now?", ("Yes", "No"))
    if answer == "Yes":
        switch_pages("Anxiety_Attack_Protocol.py")  # Hier wird der Dateiname als Zeichenkette übergeben
    else:
        answer_2 = st.radio("Are you anxious right now?", ("Yes", "No"))
        if answer_2 == "Yes":
            switch_pages("Anxiety_protocol.py")  # Hier wird der Dateiname als Zeichenkette übergeben
        else:
            st.write("Reassess your feelings.")

def switch_pages(page_name):
    st.success("Redirecting to {} page...".format(page_name))  # Hier können Sie eine Erfolgsmeldung oder eine andere Benachrichtigung anzeigen
    time.sleep(2)  # Optional: Kleine Verzögerung, um die Nachricht anzuzeigen
    st.experimental_rerun()

if __name__ == "__main__":
    show()
