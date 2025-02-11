import logging
from functools import wraps
from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from db.connection import get_db
from db.models import User, Account, Transaction

# Create a Blueprint for dashboard-related routes
dashboard_bp = Blueprint('dashboard', __name__)

def login_required(f):
    """
    Decorator to ensure routes are accessed only by authenticated users.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("You must be logged in to access that page.", "warning")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


@dashboard_bp.route('/')
@login_required
def dashboard():
    """
    Displays the user's dashboard with their details, accounts, and recent transactions.
    """
    user_id = session.get('user_id')
    db_gen = get_db()
    db = next(db_gen)
    try:
        user = db.query(User).filter_by(user_id=user_id).first()
        if not user:
            flash("User not found.", "danger")
            return redirect(url_for('auth.login'))

        # Retrieve the user's accounts
        accounts = db.query(Account).filter_by(user_id=user_id).all()

        # Retrieve transactions across all of the user's accounts
        transactions = db.query(Transaction).join(Account).filter(Account.user_id == user_id).all()
    except Exception as e:
        logging.exception("Error fetching dashboard data")
        flash("An error occurred while fetching dashboard data.", "danger")
        user = None
        accounts = []
        transactions = []
    finally:
        try:
            db_gen.close()
        except Exception:
            pass

    return render_template('dashboard.html', user=user, accounts=accounts, transactions=transactions)


@dashboard_bp.route('/create_account', methods=['GET', 'POST'])
@login_required
def create_account():
    """
    Provides a form to create a new account.
    Accepts POST requests to create the account and GET requests to render the form.
    """
    if request.method == 'POST':
        account_type = request.form.get('account_type')
        user_id = session.get('user_id')

        if account_type not in ['Savings', 'Current']:
            flash("Invalid account type selected.", "warning")
            return redirect(url_for('dashboard.create_account'))

        db_gen = get_db()
        db = next(db_gen)
        try:
            new_account = Account(user_id=user_id, account_type=account_type, balance=0.00)
            db.add(new_account)
            db.commit()
            flash("Account created successfully.", "success")
            return redirect(url_for('dashboard.dashboard'))
        except Exception as e:
            db.rollback()
            logging.exception("Error creating account")
            flash("An error occurred while creating the account.", "danger")
            return redirect(url_for('dashboard.create_account'))
        finally:
            try:
                db_gen.close()
            except Exception:
                pass

    # For GET requests, render the account creation form
    return render_template('create_account.html')


@dashboard_bp.route('/account/<int:account_id>')
@login_required
def view_account(account_id):
    """
    Displays details and transactions for a specific account.
    """
    user_id = session.get('user_id')
    db_gen = get_db()
    db = next(db_gen)
    try:
        account = db.query(Account).filter_by(account_id=account_id, user_id=user_id).first()
        if not account:
            flash("Account not found or access denied.", "danger")
            return redirect(url_for('dashboard.dashboard'))
        transactions = db.query(Transaction).filter_by(account_id=account_id).all()
    except Exception as e:
        logging.exception("Error fetching account details")
        flash("An error occurred while fetching account details.", "danger")
        account = None
        transactions = []
    finally:
        try:
            db_gen.close()
        except Exception:
            pass

    return render_template('account_details.html', account=account, transactions=transactions)