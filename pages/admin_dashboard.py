import streamlit as st
import pandas as pd
from utils.database import get_connection

# Function to fetch doctors data
def fetch_doctors():
    conn = get_connection()
    query = "SELECT * FROM doctors;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Function to add a doctor
def add_doctor(first_name, last_name, specialization, department, phone_number, email, availability, consultation_fees):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO doctors (first_name, last_name, specialization, department, phone_number, email, availability, consultation_fees)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """, (first_name, last_name, specialization, department, phone_number, email, availability, consultation_fees))
    conn.commit()
    cursor.close()
    conn.close()
    st.success("Doctor added successfully!")

# Function to update a doctor
def update_doctor(doctor_id, first_name, last_name, specialization, department, phone_number, email, availability, consultation_fees):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE doctors 
        SET first_name = %s, last_name = %s, specialization = %s, department = %s,
            phone_number = %s, email = %s, availability = %s, consultation_fees = %s 
        WHERE id = %s;
    """, (first_name, last_name, specialization, department, phone_number, email, availability, consultation_fees, doctor_id))
    conn.commit()
    cursor.close()
    conn.close()
    st.success("Doctor updated successfully!")

# Function to delete a doctor
def delete_doctor(doctor_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM doctors WHERE doctor_id = %s;", (doctor_id,))
    conn.commit()
    cursor.close()
    conn.close()
    st.success("Doctor deleted successfully!")

# Function to fetch staff data
def fetch_staff():
    conn = get_connection()
    query = "SELECT * FROM staff;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Function to add staff
def add_staff(first_name, last_name, role, department, phone_number, email, shift_schedule):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO staff (first_name, last_name, role, department, phone_number, email, shift_schedule)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """, (first_name, last_name, role, department, phone_number, email, shift_schedule))
    conn.commit()
    cursor.close()
    conn.close()
    st.success("Staff added successfully!")

# Function to fetch payments
def fetch_payments():
    conn = get_connection()
    query = "SELECT * FROM payments;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Main Admin Dashboard
def admin_dashboard():
    st.title("Admin Dashboard")
    
    # Section to manage doctors
    st.subheader("Manage Doctors")
    doctors_data = fetch_doctors()
    st.dataframe(doctors_data)

    # Add new doctor
    with st.form(key='add_doctor_form'):
        st.subheader("Add New Doctor")
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        specialization = st.text_input("Specialization")
        department = st.text_input("Department")
        phone_number = st.text_input("Phone Number")
        email = st.text_input("Email")
        availability = st.text_input("Availability")
        consultation_fees = st.number_input("Consultation Fees", min_value=0.0, format="%.2f")
        submit_doctor_button = st.form_submit_button("Add Doctor")

        if submit_doctor_button:
            add_doctor(first_name, last_name, specialization, department, phone_number, email, availability, consultation_fees)

    # Update or delete doctor
    st.subheader("Update or Delete Doctor")
    doctor_id = st.number_input("Doctor ID to Update/Delete", min_value=1)
    
    if doctor_id:
        doctor = doctors_data[doctors_data['doctor_id'] == doctor_id]
        
        if not doctor.empty:
            doctor = doctor.iloc[0]

            with st.form(key='update_doctor_form'):
                st.subheader("Update Doctor")
                first_name = st.text_input("First Name", value=doctor['first_name'])
                last_name = st.text_input("Last Name", value=doctor['last_name'])
                specialization = st.text_input("Specialization", value=doctor['specialization'])
                department = st.text_input("Department", value=doctor['department'])
                phone_number = st.text_input("Phone Number", value=doctor['phone_number'])
                email = st.text_input("Email", value=doctor['email'])
                availability = st.text_input("Availability", value=doctor['availability'])
                consultation_fees = st.number_input("Consultation Fees", value=float(doctor['consultation_fees']), min_value=0.0, format="%.2f")

                update_button = st.form_submit_button("Update Doctor")

                if update_button:
                    update_doctor(doctor_id, first_name, last_name, specialization, department, phone_number, email, availability, consultation_fees)

            if st.button("Delete Doctor"):
                delete_doctor(doctor_id)

    # Section to manage staff
    st.subheader("Manage Staff")
    staff_data = fetch_staff()
    st.dataframe(staff_data)

    with st.form(key='add_staff_form'):
        st.subheader("Add New Staff")
        staff_first_name = st.text_input("First Name", key='staff_first_name')
        staff_last_name = st.text_input("Last Name", key='staff_last_name')
        role = st.text_input("Role")
        staff_department = st.text_input("Department")
        staff_phone_number = st.text_input("Phone Number")
        staff_email = st.text_input("Email")
        shift_schedule = st.text_input("Shift Schedule")
        submit_staff_button = st.form_submit_button("Add Staff")

        if submit_staff_button:
            add_staff(staff_first_name, staff_last_name, role, staff_department, staff_phone_number, staff_email, shift_schedule)

    # Section to manage payments
    st.subheader("Manage Payments")
    payments_data = fetch_payments()
    st.dataframe(payments_data)


if __name__ == "__main__":
    admin_dashboard()
