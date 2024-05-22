import streamlit as st
from PIL import Image
import time

def show():
    st.image("Logo.jpeg", width=600)
    st.write("---")
    
    st.write("Anxiety Assessment:")
    
    answer = st.radio("Do you feel like you're having an Anxiety Attack right now?", ("Yes", "No"))
    if answer == "Yes":
        st.switch_pages("anxiety_attack_protocol.py")
    else:
        answer_2 = st.radio("Are you anxious right now?", ("Yes", "No"))
        if answer_2 == "Yes":
            st.switch_pages("anxiety_protocol.py")
        else:
            st.write("Reassess your feelings.")

def switch_pages(page_name):
    st.success("Redirecting to {} page...".format(page_name))
    time.sleep(2)
    st.experimental_rerun()

if __name__ == "__main__":
    show()
