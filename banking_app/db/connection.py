import os
import mysql.connector

def get_db_connection():
    # Fetch DB credentials from environment variables
    db_host = os.getenv("DB_HOST")
    db_user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_PASS")
    db_name = os.getenv("DB_NAME")
    db_port = os.getenv("DB_PORT")

    # Check if all environment variables are set
    if not db_host or not db_user or not db_pass or not db_name or not db_port:
        raise ValueError("Database credentials not set in environment variables")

    # Connect to the database
    try:
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_pass,
            database=db_name,
            port=db_port,
            ssl_disabled=False  # ssl_mode="REQUIRED"
        )
        
        return connection
    
    except mysql.connector.Error as err:
        print(f"Error while connecting to MySQL: {err}")
        return None

def close_connection(connection):
    if connection and connection.is_connected():
        connection.close()