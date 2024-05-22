import streamlit as st
from PIL import Image
import time

def main():
    query_params = st.experimental_get_query_params()
    page = query_params.get("page", ["main"])[0]

    if page == "anxiety_attack_protocol":
        import pages.anxiety_attack_protocol as attack_protocol
        attack_protocol.show()
    elif page == "anxiety_protocol":
        import pages.anxiety_protocol as anxiety_protocol
        anxiety_protocol.show()
    else:
        show_main_page()

def show_main_page():
    st.image("Logo.jpeg", width=600)
    st.write("---")
    
    st.write("Anxiety Assessment:")
    
    answer = st.radio("Do you feel like you're having an Anxiety Attack right now?", ("Yes", "No"))
    if answer == "Yes":
        st.switch_pages("anxiety_attack_protocol")
    else:
        answer_2 = st.radio("Are you anxious right now?", ("Yes", "No"))
        if answer_2 == "Yes":
            st.switch_pages("anxiety_protocol")
        else:
            st.write("Reassess your feelings.")

def switch_pages(page_name):
    st.success(f"Redirecting to {page_name.replace('_', ' ')} page...")
    time.sleep(2)
    st.experimental_set_query_params(page=page_name)
    st.experimental_rerun()

if __name__ == "__main__":
    main()
