import streamlit as st
import streamlit_lottie as sl
from utils.authentication import authenticate_user
from utils.database import get_connection
from streamlit_extras.switch_page_button import switch_page
import json

# Load animations
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

def login_page():
    st.markdown("<h2 style='text-align: center;'>Hospital Management System</h2>", unsafe_allow_html=True)
    login_animation = load_lottiefile("assets/login_animation.json")
    sl.st_lottie(login_animation, height=250)

    role = st.selectbox("Select Role", ['Admin', 'Receptionist', 'Head Nurse', 'Accountant', 'Services Coordinator'])
    password = st.text_input("Enter Password", type="password")
    
    if st.button("Login"):
        if authenticate_user(role, password):
            # Map role to the corresponding page name
            role_to_page = {
                'Admin': 'admin dashboard',
                'Receptionist': 'receptionist dashboard',
                'Head Nurse': 'head nurse dashboard',
                'Accountant': 'accountant dashboard',
                'Services Coordinator': 'service coordinator'  # No "dashboard" here
            }
            page_name = role_to_page.get(role)
            if page_name:
                st.session_state.page = page_name
                switch_page(page_name)
            else:
                st.error("Invalid role or page name.")
        else:
            st.error("Invalid role or password.")


# Main function to set up the app
def main():
    if 'page' not in st.session_state:
        st.session_state.page = 'login'

    # Render the appropriate page based on session state
    if st.session_state.page == 'login':
        login_page()
    else:
        # Render the appropriate dashboard based on the session state
        switch_page(st.session_state.page)  # Automatically switch to the stored page

if __name__ == "__main__":
    st.set_page_config(page_title="Hospital Management System", layout="wide", page_icon="🏥")
    main()
