from connection import get_db_connection, DBConnectionError
from datetime import datetime
import bcrypt

class UserModel:
    def __init__(self):
        self.conn = get_db_connection()

    def create_user(self, username, password, email, phone):
        try:
            cursor = self.conn.cursor()
            query = "INSERT INTO Users (username, password_hash, email, phone, created_at) VALUES (%s, %s, %s, %s, %s)"
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(query, (username, password_hash, email, phone, created_at))
            self.conn.commit()
            return cursor.lastrowid
        except DBConnectionError as err:
            raise err

    def get_user_by_id(self, user_id):
        try:
            cursor = self.conn.cursor()
            query = "SELECT * FROM Users WHERE users_id = %s"
            cursor.execute(query, (user_id,))
            return cursor.fetchone()
        except DBConnectionError as err:
            raise err

    def get_user_by_username(self, username):
        try:
            cursor = self.conn.cursor()
            query = "SELECT * FROM Users WHERE username = %s"
            cursor.execute(query, (username,))
            return cursor.fetchone()
        except DBConnectionError as err:
            raise err

    def get_user_by_email(self, email):
        try:
            cursor = self.conn.cursor()
            query = "SELECT * FROM Users WHERE email = %s"
            cursor.execute(query, (email,))
            return cursor.fetchone()
        except DBConnectionError as err:
            raise err

    def update_user(self, user_id, username=None, password=None, email=None, phone=None):
        try:
            cursor = self.conn.cursor()
            query = "UPDATE Users SET "
            params = []
            if username:
                query += "username = %s, "
                params.append(username)
            if password:
                password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                query += "password_hash = %s, "
                params.append(password_hash)
            if email:
                query += "email = %s, "
                params.append(email)
            if phone:
                query += "phone = %s, "
                params.append(phone)
            query = query.rstrip(", ") + " WHERE users_id = %s"
            params.append(user_id)
            cursor.execute(query, params)
            self.conn.commit()
            return cursor.rowcount
        except DBConnectionError as err:
            raise err

    def delete_user(self, user_id):
        try:
            cursor = self.conn.cursor()
            query = "DELETE FROM Users WHERE users_id = %s"
            cursor.execute(query, (user_id,))
            self.conn.commit()
            return cursor.rowcount
        except DBConnectionError as err:
            raise err

    def authenticate_user(self, identifier, password):
        try:
            cursor = self.conn.cursor()
            if identifier.isdigit():  # Check if identifier is a user_id
                query = "SELECT password_hash FROM Users WHERE users_id = %s"
            elif "@" in identifier:  # Check if identifier is an email
                query = "SELECT password_hash FROM Users WHERE email = %s"
            elif identifier.replace("+", "").isdigit():  # Check if identifier is a phone number
                query = "SELECT password_hash FROM Users WHERE phone = %s"
            else:  # Assume identifier is a username
                query = "SELECT password_hash FROM Users WHERE username = %s"
            cursor.execute(query, (identifier,))
            stored_password_hash = cursor.fetchone()
            if stored_password_hash:
                # Compare the provided password with the stored password hash
                if bcrypt.checkpw(password.encode('utf-8'), stored_password_hash[0]):
                    return True
            return False
        except DBConnectionError as err:
            raise err