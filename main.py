import streamlit as st
from github_contents import GithubContents

github = GithubContents(
    st.secrets["github"]["owner"],
    st.secrets["github"]["repo"],
    st.secrets["github"]["token"])

def main_sidebar():
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page", ["Profile", "Anxiety Attack", "Anxiety", "Mainpage"])
    if page == "Profile":
        st.sidebar.switch_page("pages/2_profile.py")
    elif page == "Anxiety Attack":
        st.sidebar.switch_page("pages/4_anxiety_attack_protocol.py")
    elif page == "Anxiety":
        st.sidebar.switch_page("pages/5_anxiety_protocol.py")
    elif page == "Mainpage":
        st.sidebar.switch_page("main.py")

def main_page():
    st.image("Logo.jpeg", width=600)
    st.subheader("Anxiety Tracker Journal")
    st.write("""
        Welcome to FeelNow, your anxiety attack journal.
        This app helps you track and manage your anxiety by providing a platform to journal your thoughts 
        and feelings during anxiety attacks.
        
        ## What is FeelNow
        FeelNow is an app with which you can easily assess and monitor an acute panic attack. It is just like a diary and helps you to keep an eye on your mental health.
        
        ## What can the App do
        The app is supposed to help you write down important parts of a panic attack or even simply for your anxiety. It simplifies takeing notes while feeling distressed by having the option to just choose how you're feeling instead of having to write your feelings down yourself.
        
        ## How do I use it
        You can create your own login by registering. You will then have a list of important points to assess during an acute attack, such as symptoms, possible triggers, who helped you at that moment or how strongly you felt them. If you do not feel like you're having a panic attack but you do feel anxious, you can do the same in the simpler version.
        """)

    col1, col2 = st.columns([0.8, 0.2])
    with col2:
        if st.button("Login/Register"):
            st.switch_page("pages/1_login.py")

def switch_page(page_name):
    st.success("Redirecting to {} page...".format(page_name))
    # Hier können Sie die Logik hinzufügen, um zur angegebenen Seite zu navigieren

if __name__ == "__main__":
    main_page()
