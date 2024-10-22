import streamlit as st
import pandas as pd
from utils.database import get_connection

# Function to add payment to the database
def add_payment(payment_date, amount_paid, payment_method):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO payments (payment_date, amount_paid, payment_method)
            VALUES ( %s, %s, %s);
        """, (payment_date, amount_paid, payment_method))
        conn.commit()
        cursor.close()
        conn.close()
        st.success("Payment added successfully!")
    except Exception as e:
        st.error(f"Error adding payment: {e}")

# Function to fetch payments from the database
def fetch_payments():
    try:
        conn = get_connection()
        query = "SELECT * FROM payments;"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error fetching payments: {e}")
        return pd.DataFrame()  # Return an empty dataframe in case of error

# Accountant Dashboard Function
def accountant_dashboard():
    st.title("Accountant Dashboard")

    # Payments Section: View Payments
    st.subheader("View Payments")
    payments_data = fetch_payments()
    if not payments_data.empty:
        st.dataframe(payments_data)
    else:
        st.write("No payments found.")

    # Section to Add New Payment
    st.subheader("Add New Payment")
    with st.form(key='add_payment_form'):
        payment_date = st.date_input("Payment Date")
        amount_paid = st.number_input("Amount Paid", min_value=0.0, format="%.2f")
        payment_method = st.selectbox("Payment Method", options=["Cash", "Credit Card", "Insurance", "Online"])
        submit_payment_button = st.form_submit_button("Add Payment")

        if submit_payment_button:
            add_payment(payment_date, amount_paid, payment_method)

# Run the Accountant Dashboard
if __name__ == "__main__":
    accountant_dashboard()
