import streamlit as st

def authenticate_user(role, password):
    credentials = {
        'Admin': st.secrets['general']['ADMIN_PASSWORD'],
        'Receptionist': st.secrets['general']['RECEPTIONIST_PASSWORD'],
        'Head Nurse': st.secrets['general']['HEAD_NURSE_PASSWORD'],
        'Accountant': st.secrets['general']['ACCOUNTANT_PASSWORD'],
        'Services Coordinator': st.secrets['general']['SERVICE_COORDINATOR_PASSWORD']
    }
    
    if role in credentials and credentials[role] == password:
        return True
    return False
