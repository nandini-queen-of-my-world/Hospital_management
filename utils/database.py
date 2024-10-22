import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="hospital_management",
        user="your_username",
        password="your_password"
    )
