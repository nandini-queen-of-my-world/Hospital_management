import streamlit as st
import pandas as pd
from utils.database import get_connection

# Fetch rooms data
def fetch_rooms():
    conn = get_connection()
    query = "SELECT * FROM rooms;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Fetch bed allocations data
def fetch_bed_allocations():
    conn = get_connection()
    query = "SELECT * FROM bedallocation;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Add room function
def add_room(room_no, room_type, availability_status, rate_per_day):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO rooms (room_no, room_type, availability_status, rate_per_day)
        VALUES (%s, %s, %s, %s);
    """, (room_no, room_type, availability_status, rate_per_day))
    conn.commit()
    cursor.close()
    conn.close()
    st.success("Room added successfully!")

# Add bed allocation function
def add_bed_allocation(patient_id, room_no, date_allocated, date_released):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO bedallocation (patient_id, room_no, date_allocated, date_released)
        VALUES (%s, %s, %s, %s);
    """, (patient_id, room_no, date_allocated, date_released))
    conn.commit()
    cursor.close()
    conn.close()
    st.success("Bed allocation added successfully!")

# Update room function
def update_room(room_no, room_type, availability_status, rate_per_day):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE rooms
        SET room_type = %s, availability_status = %s, rate_per_day = %s
        WHERE room_no = %s;
    """, (room_type, availability_status, rate_per_day, room_no))
    conn.commit()
    cursor.close()
    conn.close()
    st.success("Room updated successfully!")

# Delete room function
def delete_room(room_no):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM rooms WHERE room_no = %s;", (room_no,))
    conn.commit()
    cursor.close()
    conn.close()
    st.success("Room deleted successfully!")

# Dashboard for services coordinator
def services_coordinator_dashboard():
    st.title("Services Coordinator Dashboard")

    # Tabs for managing rooms and bed allocations
    tab1, tab2, tab3 = st.tabs(["View Rooms", "Add/Update/Delete Room", "Manage Bed Allocations"])

    # Tab 1: View Rooms
    with tab1:
        st.subheader("Rooms List")
        rooms_data = fetch_rooms()
        st.dataframe(rooms_data)

    # Tab 2: Add/Update/Delete Room
    with tab2:
        st.subheader("Add or Update Room")
        with st.form(key='room_form'):
            room_no = st.text_input("Room Number (for update/delete)", value="0", help="Leave 0 if adding new room")

            room_type = st.selectbox("Room Type", ["Single", "Double", "Suite", "ICU"])
            availability_status = st.selectbox("Availability Status", ["Available", "Occupied"])
            rate_per_day = st.number_input("Rate Per Day", min_value=0)

            submit_room_button = st.form_submit_button("Submit")
            delete_room_button = st.form_submit_button("Delete Room")

            if submit_room_button:
                if room_no == 0:
                    add_room(room_no, room_type, availability_status, rate_per_day)
                else:
                    update_room(room_no, room_type, availability_status, rate_per_day)
            elif delete_room_button and room_no != 0:
                delete_room(room_no)

    # Tab 3: Manage Bed Allocations
    with tab3:
        st.subheader("Bed Allocations")
        st.write("View, allocate, or release beds.")

        bed_allocations_data = fetch_bed_allocations()
        st.dataframe(bed_allocations_data)

        with st.form(key='bed_allocation_form'):
            patient_id = st.number_input("Patient ID", min_value=1)
            room_no = st.number_input("Room Number", min_value=1)
            date_allocated = st.date_input("Date Allocated")
            date_released = st.date_input("Date Released", help="Leave empty if not yet released", key="date_released")

            submit_bed_allocation_button = st.form_submit_button("Allocate Bed")

            if submit_bed_allocation_button:
                add_bed_allocation(patient_id, room_no, date_allocated, date_released)

if __name__ == "__main__":
    services_coordinator_dashboard()
