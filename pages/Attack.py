import streamlit as st
from PIL import Image
import time

def show():
    st.image("Logo.jpeg", width=600)
    st.write("---")
    
    st.write("Anxiety Assessment:")
    
    answer = st.radio("Do you feel like you're having an Anxiety Attack right now?", ("Yes", "No"))
    if answer == "Yes":
        switch_pages("Anxiety_Attack_Protocol.py")
    else:
        answer_2 = st.radio("Are you anxious right now?", ("Yes", "No"))
        if answer_2 == "Yes":
            switch_pages("Anxiety_protocol.py")
        else:
            st.write("Reassess your feelings.")

if __name__ == "__main__":
    show()
