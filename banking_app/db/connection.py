import os
import mysql.connector

class EnvironmentVariableError(Exception):
    """Custom exception for missing environment variables."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class DBConnectionError(Exception):
    """Custom exception for database connection errors."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

def get_db_connection():
    """Establish a database connection."""
    try:
        # Fetch environment variables
        db_host = os.getenv("DB_HOST")
        db_user = os.getenv("DB_USER")
        db_pass = os.getenv("DB_PASS")
        db_name = os.getenv("DB_NAME")
        db_port = os.getenv("DB_PORT")

        # Check if all required environment variables are present
        if not all([db_host, db_user, db_pass, db_name, db_port]):
            missing_vars = []
            if not db_host: missing_vars.append("DB_HOST")
            if not db_user: missing_vars.append("DB_USER")
            if not db_pass: missing_vars.append("DB_PASS")
            if not db_name: missing_vars.append("DB_NAME")
            if not db_port: missing_vars.append("DB_PORT")
            raise EnvironmentVariableError(
                f"Missing environment variables: {', '.join(missing_vars)}. "
                "The application isn't properly installed. Please reinstall it."
            )

        # Try connecting to the database
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_pass,
            database=db_name,
            port=db_port,
            ssl_disabled=False
        )
        if connection.is_connected():
            return connection
        else:
            raise DBConnectionError("Failed to connect to the database.")
    except mysql.connector.Error as err:
        raise DBConnectionError(f"Error while connecting to MySQL: {err}")
    except Exception as err:
        raise DBConnectionError(f"An unexpected error occurred: {err}")