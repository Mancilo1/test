import streamlit as st
from PIL import Image
import time

def switch_pages(page_name):
    if page_name == "Anxiety_Attack_Protocol":
        st.success("Redirecting to Anxiety Attack Protocol page...")
        time.sleep(2)
        st.switch_page("Anxiety_Attack_Protocol.py")
    elif page_name == "Anxiety_protocol":
        st.success("Redirecting to Anxiety Protocol page...")
        time.sleep(2)
        st.switch_page("Anxiety_Protocol.py")

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
