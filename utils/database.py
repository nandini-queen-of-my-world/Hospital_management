import psycopg2
import streamlit as st

def get_connection():
    return psycopg2.connect(
        host=st.secrets['database']['DB_HOST'],
        database=st.secrets['database']['DB_NAME'],
        user=st.secrets['database']['DB_USER'],
        password=st.secrets['database']['DB_PASSWORD']
    )
