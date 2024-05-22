import streamlit as st
from PIL import Image
import time
import sys
import os

# Adjust the path to include the parent directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importing the pages
import anxiety_attack_protocol as attack_protocol
import anxiety_protocol

def main():
    # Get query parameters to determine the page
    query_params = st.experimental_get_query_params()
    page = query_params.get("page", ["main"])[0]

    if page == "anxiety_attack_protocol":
        attack_protocol.show()
    elif page == "anxiety_protocol":
        anxiety_protocol.show()
    else:
        show_main_page()

def show_main_page():
    st.image("Logo.jpeg", width=600)
    st.write("---")

    st.write("Anxiety Assessment:")

    answer = st.radio("Do you feel like you're having an Anxiety Attack right now?", ("Yes", "No"))
    if answer == "Yes":
        switch_pages("anxiety_attack_protocol")
    else:
        answer_2 = st.radio("Are you anxious right now?", ("Yes", "No"))
        if answer_2 == "Yes":
            switch_pages("anxiety_protocol")
        else:
            st.write("Reassess your feelings.")

def switch_pages(page_name):
    st.success(f"Redirecting to {page
