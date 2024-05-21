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

if __name__ == "__main__":
    Mainpage()

