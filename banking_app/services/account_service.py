import logging
from decimal import Decimal
from sqlalchemy.exc import SQLAlchemyError
from db.connection import get_db
from db.models import Account

def create_account(user_id: int, account_type: str, initial_balance: Decimal = Decimal("0.00")):
    """
    Create a new account for the given user.
    Accepts 'Savings' or 'Current' as account_type.
    Returns the new account object.
    """
    if account_type not in ['Savings', 'Current']:
        raise ValueError("Invalid account type. Must be 'Savings' or 'Current'.")
    
    db_gen = get_db()
    db = next(db_gen)
    try:
        new_account = Account(user_id=user_id, account_type=account_type, balance=initial_balance)
        db.add(new_account)
        db.commit()
        db.refresh(new_account)
        return new_account
    except SQLAlchemyError as e:
        db.rollback()
        logging.exception("Database error during account creation")
        raise e
    except Exception as e:
        db.rollback()
        logging.exception("Error creating account")
        raise e
    finally:
        try:
            db_gen.close()
        except Exception:
            pass

def get_accounts_by_user(user_id: int):
    """
    Retrieve all accounts associated with the specified user.
    Returns a list of Account objects.
    """
    db_gen = get_db()
    db = next(db_gen)
    try:
        accounts = db.query(Account).filter_by(user_id=user_id).all()
        return accounts
    except Exception as e:
        logging.exception("Error retrieving accounts for user_id %s", user_id)
        raise e
    finally:
        try:
            db_gen.close()
        except Exception:
            pass

def update_account_balance(account_id: int, amount: Decimal, operation: str = "add"):
    """
    Update the balance of an account.
    Operation can be 'add' (to deposit) or 'subtract' (to withdraw).
    Returns the updated account object.
    """
    db_gen = get_db()
    db = next(db_gen)
    try:
        account = db.query(Account).filter_by(account_id=account_id).first()
        if not account:
            raise ValueError("Account not found.")
        
        if operation == "add":
            account.balance += amount
        elif operation == "subtract":
            if account.balance < amount:
                raise ValueError("Insufficient funds.")
            account.balance -= amount
        else:
            raise ValueError("Invalid operation. Use 'add' or 'subtract'.")
        
        db.commit()
        db.refresh(account)
        return account
    except Exception as e:
        db.rollback()
        logging.exception("Error updating account balance for account_id %s", account_id)
        raise e
    finally:
        try:
            db_gen.close()
        except Exception:
            pass