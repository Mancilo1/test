import streamlit as st
from github_contents import GithubContents

# Initialize GithubContents
github = GithubContents(
    st.secrets["github"]["owner"],
    st.secrets["github"]["repo"],
    st.secrets["github"]["token"])

def main_page():
    # Sidebar configuration
    try:
        st.sidebar.image("Logo.jpeg", use_column_width=True)
        st.sidebar.title("Navigation")
        page_selection = st.sidebar.selectbox("Select a page", ["Main", "Login/Register"])
    except Exception as e:
        st.sidebar.error(f"Error loading sidebar content: {e}")

    # Main page content
    if page_selection == "Main":
        st.image("Logo.jpeg", width=600)  # Adjusted logo size
        st.subheader("Anxiety Tracker Journal")
        st.write("""
            Welcome to FeelNow, your anxiety attack journal.
            This app helps you track and manage your anxiety by providing a platform to journal your thoughts 
            and feelings during anxiety attacks.
            
            ## What is FeelNow
            FeelNow is an app with which you can easily assess and monitor an acute panic attack. It is just like a diary and helps you to keep an eye on your mental health.
            
            ## What can the App do
            The app is supposed to help you write down important parts of a panic attack or even simply for your anxiety. It simplifies taking notes while feeling distressed by having the option to just choose how you're feeling instead of having to write your feelings down yourself.
            
            ## How do I use it
            You can create your own login by registering. You will then have a list of important points to assess during an acute attack, such as symptoms, possible triggers, who helped you at that moment or how strongly you felt them. If you do not feel like you're having a panic attack but you do feel anxious, you can do the same in the simpler version.
        """)

        col1, col2 = st.columns([0.8, 0.2])
        with col2:
            if st.button("Login/Register"):
                st.experimental_set_query_params(page="login")
                st.experimental_rerun()
    
    elif page_selection == "Login/Register":
        st.experimental_set_query_params(page="login")
        st.experimental_rerun()

def switch_page(page_name):
    st.success(f"Redirecting to {page_name} page...")  # Display success message
    st.experimental_set_query_params(page=page_name)
    st.experimental_rerun()

if __name__ == "__main__":
    main_page()
