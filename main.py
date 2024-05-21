import streamlit as st
from pages import Mainpage
from pages import Login
from pages import Attack 
from pages import Anxiety_Attack_Protocol
from pages import Anxiety_protocol
from github_contents import GithubContents

github = GithubContents(
    st.secrets["github"]["owner"],
    st.secrets["github"]["repo"],
    st.secrets["github"]["token"])

PAGE_TITLE_MAP = {
    "Main Page": Mainpage,
    "Login Page": Login,
    "Register Page": Attack,
    "Anxiety Attack Protocol Page": Anxiety_Attack_Protocol,
    "Anxiety Protocol Page": Anxiety_protocol
}

import streamlit as st
from PIL import Image
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

if __name__ == "__main__":
    Mainpage()

