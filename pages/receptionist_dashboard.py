import streamlit as st
import pandas as pd
from utils.database import get_connection

# Fetch appointment data
def fetch_appointments():
    conn = get_connection()
    query = "SELECT * FROM appointments;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Add new appointment function
def add_appointment(patient_id, doctor_id, appointment_date, appointment_time, status, remarks):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, status, remarks)
        VALUES (%s, %s, %s, %s, %s, %s);
    """, (patient_id, doctor_id, appointment_date, appointment_time, status, remarks))
    conn.commit()
    cursor.close()
    conn.close()
    st.success("Appointment added successfully!")

# Update appointment function
def update_appointment(appointment_id, status, remarks):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE appointments 
        SET status = %s, remarks = %s
        WHERE appointment_id = %s;
    """, (status, remarks, appointment_id))
    conn.commit()
    cursor.close()
    conn.close()
    st.success("Appointment updated successfully!")

# Delete appointment function
def delete_appointment(appointment_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM appointments WHERE appointment_id = %s;", (appointment_id,))
    conn.commit()
    cursor.close()
    conn.close()
    st.success("Appointment deleted successfully!")

def receptionist_dashboard():
    st.title("Receptionist Dashboard")

    # Tabs for managing appointments
    tab1, tab2, tab3 = st.tabs(["View Appointments", "Add Appointment", "Update/Delete Appointment"])

    with tab1:
        st.subheader("View Appointments")
        appointments_data = fetch_appointments()
        st.dataframe(appointments_data)

    with tab2:
        st.subheader("Add New Appointment")
        with st.form(key='add_appointment_form'):
            patient_id = st.number_input("Patient ID", min_value=1)
            doctor_id = st.number_input("Doctor ID", min_value=1)
            appointment_date = st.date_input("Appointment Date")
            appointment_time = st.time_input("Appointment Time")
            status = st.selectbox("Status", ["Scheduled", "Completed", "Cancelled"])
            remarks = st.text_area("Remarks")
            submit_button = st.form_submit_button("Add Appointment")
        
        if submit_button:
            add_appointment(patient_id, doctor_id, appointment_date, appointment_time, status, remarks)

    with tab3:
        st.subheader("Update/Delete Appointment")
        appointments_data = fetch_appointments()

        # Check if there are any appointments to update or delete
        if not appointments_data.empty:
            appointment_id = st.selectbox("Select Appointment to Update/Delete", appointments_data['appointment_id'])

            # Get selected appointment details
            selected_appointment = appointments_data[appointments_data['appointment_id'] == appointment_id]
            st.write(selected_appointment)

            # Extract current status
            current_status = selected_appointment['status'].values[0]  # Extract current status
            status_options = ["Scheduled", "Completed", "Cancelled"]

            # Ensure current status is a valid option
            current_status_index = status_options.index(current_status) if current_status in status_options else 0
            status = st.selectbox("Update Status", status_options, index=current_status_index)

            remarks = st.text_area("Update Remarks", selected_appointment['remarks'].values[0])

            update_button = st.button("Update Appointment")
            delete_button = st.button("Delete Appointment")

            if update_button:
                update_appointment(appointment_id, status, remarks)
            if delete_button:
                delete_appointment(appointment_id)
        else:
            st.write("No appointments available to update or delete.")

if __name__ == "__main__":
    receptionist_dashboard()
