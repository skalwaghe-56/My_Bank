import logging
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError
from db.connection import get_db
from db.models import User

def create_user(username: str, email: str, password: str):
    """
    Create a new user with the given username, email, and password.
    Returns the new user object, or raises an exception if creation fails.
    """
    password_hash = generate_password_hash(password)
    db_gen = get_db()
    db = next(db_gen)
    try:
        # Check if a user with the same username or email already exists
        if db.query(User).filter(or_(User.username == username, User.email == email)).first():
            raise ValueError("Username or email already exists.")
        
        new_user = User(username=username, email=email, password_hash=password_hash)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except SQLAlchemyError as e:
        db.rollback()
        logging.exception("Database error during user creation")
        raise e
    except Exception as e:
        db.rollback()
        logging.exception("Error creating user")
        raise e
    finally:
        try:
            db_gen.close()
        except Exception:
            pass

def verify_user(username: str, password: str):
    """
    Verify user credentials.
    Returns the user object if the username and password match; otherwise, returns None.
    """
    db_gen = get_db()
    db = next(db_gen)
    try:
        user = db.query(User).filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            return user
        return None
    except Exception as e:
        logging.exception("Error verifying user credentials")
        raise e
    finally:
        try:
            db_gen.close()
        except Exception:
            pass