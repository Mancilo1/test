
import binascii
import streamlit as st
import pandas as pd
from github_contents import GithubContents
import bcrypt

def show():
    st.title("Login/Register")

def Login():
    st.image("Logo.jpeg", width=600)

    # Hier könnten die Optionen für Login oder Registrieren angezeigt werden
    option = st.sidebar.selectbox('Choose an option:', ['Login', 'Register'])

    if option == 'Login':
        login()
    elif option == 'Register':
        register()

def login():
    st.subheader('Login')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')

    if st.button('Login'):
        # Hier könntest du den Login-Prozess implementieren
        st.success('Logged in successfully!')

def register():
    st.subheader('Register')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')

    if st.button('Register'):
        # Hier könntest du den Registrierungsprozess implementieren
        st.success('Registered successfully!')

if __name__ == "__main__":
    Login()
