import logging
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from db.connection import get_db
from db.models import User

# Create a Blueprint for authentication routes
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handles user registration.
    Expects form data: username, email, password, and confirm_password.
    """
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()

        if not username or not email or not password or not confirm_password:
            flash("All fields are required.", "warning")
            return redirect(url_for('auth.register'))

        if password != confirm_password:
            flash("Passwords do not match.", "warning")
            return redirect(url_for('auth.register'))

        # Generate a secure password hash
        password_hash = generate_password_hash(password)

        # Obtain a database session from the generator
        db_gen = get_db()
        db = next(db_gen)
        try:
            # Check if the username or email is already taken
            existing_user = db.query(User).filter((User.username == username) | (User.email == email)).first()
            if existing_user:
                flash("Username or email already exists.", "warning")
                return redirect(url_for('auth.register'))

            # Create and save the new user
            new_user = User(username=username, email=email, password_hash=password_hash)
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.rollback()
            logging.exception("Error during registration")
            flash("An error occurred during registration. Please try again.", "danger")
            return redirect(url_for('auth.register'))
        finally:
            try:
                db_gen.close()
            except Exception:
                pass

    # For GET requests, render the registration form
    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles user login.
    Expects form data: username and password.
    """
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if not username or not password:
            flash("Username and password are required.", "warning")
            return redirect(url_for('auth.login'))

        db_gen = get_db()
        db = next(db_gen)
        try:
            # Retrieve user by username
            user = db.query(User).filter_by(username=username).first()
            if user and check_password_hash(user.password_hash, password):
                session['user_id'] = user.user_id
                flash("Logged in successfully.", "success")
                return redirect(url_for('dashboard.dashboard'))
            else:
                flash("Invalid username or password.", "danger")
                return redirect(url_for('auth.login'))
        except Exception as e:
            logging.exception("Error during login")
            flash("An error occurred during login. Please try again.", "danger")
            return redirect(url_for('auth.login'))
        finally:
            try:
                db_gen.close()
            except Exception:
                pass

    # For GET requests, render the login form
    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    """
    Logs the user out by removing their session data.
    """
    session.pop('user_id', None)
    flash("Logged out successfully.", "info")
    return redirect(url_for('auth.login'))