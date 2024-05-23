import streamlit as st

def profile_page():
    st.title("Profile")
    
    # Lade die Benutzerdaten aus dem DataFrame
    username = st.session_state['username']
    user_data = st.session_state.df_users.loc[st.session_state.df_users['username'] == username]
    
    if not user_data.empty:
        st.write("Username:", username)
        st.write("Name:", user_data['name'].iloc[0])
        st.write("Birthday:", user_data['birthday'].iloc[0])
    else:
        st.error("User data not found.")

# Deine anderen Funktionen bleiben unverändert

def main():
    init_github()
    init_credentials()

    # Add the logo to the sidebar
    st.sidebar.image("Logo.jpeg", use_column_width=True)
    
    if 'authentication' not in st.session_state:
        st.session_state['authentication'] = False

    if not st.session_state['authentication']:
        options = st.sidebar.selectbox("Select a page", ["Login", "Register"])
        if options == "Login":
            login_page()
        elif options == "Register":
            register_page()
    else:
        logout_button = st.sidebar.button("Logout")
        if logout_button:
            st.session_state['authentication'] = False
            st.experimental_rerun()
        else:
            profile_page()  # Füge diese Zeile hinzu, um das Profil anzuzeigen, wenn der Benutzer eingeloggt ist

# Deine anderen Funktionen bleiben unverändert

if __name__ == "__main__":
    main()
