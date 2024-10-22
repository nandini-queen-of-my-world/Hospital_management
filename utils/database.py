import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="hospital_management",
        user="postgres",
        password="nandini@108"
    )
