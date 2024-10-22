import streamlit as st
import pandas as pd
from utils.database import get_connection

# Fetch patient data
def fetch_patients():
    conn = get_connection()
    query = "SELECT * FROM patients;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Add or update patient function
def add_update_patient(first_name, last_name, date_of_birth, gender, address, phone_number, email, emergency_contact, insurance_details, blood_group, patient_id=None):
    conn = get_connection()
    cursor = conn.cursor()
    if patient_id:
        # Update existing patient
        cursor.execute("""
            UPDATE patients 
            SET first_name = %s, last_name = %s, date_of_birth = %s, gender = %s, address = %s, phone_number = %s, email = %s, emergency_contact = %s, insurance_details = %s, blood_group = %s
            WHERE patient_id = %s;
        """, (first_name, last_name, date_of_birth, gender, address, phone_number, email, emergency_contact, insurance_details, blood_group, patient_id))
        st.success("Patient updated successfully!")
    else:
        # Add new patient
        cursor.execute("""
            INSERT INTO patients (first_name, last_name, date_of_birth, gender, address, phone_number, email, emergency_contact, insurance_details, blood_group)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, (first_name, last_name, date_of_birth, gender, address, phone_number, email, emergency_contact, insurance_details, blood_group))
        st.success("Patient added successfully!")
    conn.commit()
    cursor.close()
    conn.close()

# Delete patient function
def delete_patient(patient_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM patients WHERE patient_id = %s;", (patient_id,))
    conn.commit()
    cursor.close()
    conn.close()
    st.success("Patient deleted successfully!")

# Fetch lab tests data
def fetch_lab_tests():
    conn = get_connection()
    query = "SELECT * FROM labtests;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Add or update lab test function
def add_update_lab_test(patient_id, test_name, test_date, results, test_id=None):
    conn = get_connection()
    cursor = conn.cursor()
    if test_id:
        # Update existing lab test
        cursor.execute("""
            UPDATE labtests 
            SET patient_id = %s, test_name = %s, test_date = %s, results = %s
            WHERE test_id = %s;
        """, (patient_id, test_name, test_date, results, test_id))
        st.success("Lab test updated successfully!")
    else:
        # Add new lab test
        cursor.execute("""
            INSERT INTO labtests (patient_id, test_name, test_date, results)
            VALUES (%s, %s, %s, %s);
        """, (patient_id, test_name, test_date, results))
        st.success("Lab test added successfully!")
    conn.commit()
    cursor.close()
    conn.close()

# Delete lab test function
def delete_lab_test(test_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM labtests WHERE test_id = %s;", (test_id,))
    conn.commit()
    cursor.close()
    conn.close()
    st.success("Lab test deleted successfully!")

# Main Dashboard Layout
def head_nurse_dashboard():
    st.title("Head Nurse Dashboard")

    # Sidebar Navigation
    menu = ["Patients", "Lab Tests"]
    choice = st.sidebar.selectbox("Select Action", menu)

    if choice == "Patients":
        st.header("Manage Patients")

        # Display Patients Data
        patients_data = fetch_patients()
        st.subheader("View Patients")
        st.dataframe(patients_data)

        st.subheader("Add or Update Patient")
        with st.form(key='add_patient_form'):
            patient_id = st.text_input("Patient ID (Leave blank to add new)", value="", key='patient_id')
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            date_of_birth = st.date_input("Date of Birth")
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            address = st.text_area("Address")
            phone_number = st.text_input("Phone Number")
            email = st.text_input("Email")
            emergency_contact = st.text_input("Emergency Contact")
            insurance_details = st.text_area("Insurance Details")
            blood_group = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
            submit_button = st.form_submit_button("Submit")

            if submit_button:
                if patient_id:
                    add_update_patient(first_name, last_name, date_of_birth, gender, address, phone_number, email, emergency_contact, insurance_details, blood_group, patient_id)
                else:
                    add_update_patient(first_name, last_name, date_of_birth, gender, address, phone_number, email, emergency_contact, insurance_details, blood_group)

        # Option to delete patient
        st.subheader("Delete Patient")
        del_patient_id = st.text_input("Enter Patient ID to Delete", value="")
        if st.button("Delete Patient"):
            delete_patient(del_patient_id)

    elif choice == "Lab Tests":
        st.header("Manage Lab Tests")

        # Display Lab Tests Data
        lab_tests_data = fetch_lab_tests()
        st.subheader("View Lab Tests")
        st.dataframe(lab_tests_data)

        st.subheader("Add or Update Lab Test")
        with st.form(key='add_lab_test_form'):
            lab_test_id = st.text_input("Lab Test ID (Leave blank to add new)", value="", key='lab_test_id')
            lab_patient_id = st.number_input("Patient ID", min_value=1, key='lab_patient_id')
            test_name = st.text_input("Test Name")
            test_date = st.date_input("Test Date")
            results = st.text_area("Results")            
            submit_lab_test_button = st.form_submit_button("Submit")

            if submit_lab_test_button:
                if lab_test_id:
                    add_update_lab_test(lab_patient_id, test_name, test_date, results,lab_test_id)
                else:
                    add_update_lab_test(lab_patient_id, test_name, test_date, results)

        # Option to delete lab test
        st.subheader("Delete Lab Test")
        del_lab_test_id = st.text_input("Enter Lab Test ID to Delete", value="")
        if st.button("Delete Lab Test"):
            delete_lab_test(del_lab_test_id)

if __name__ == "__main__":
    head_nurse_dashboard()
