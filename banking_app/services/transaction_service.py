import logging
from decimal import Decimal
from sqlalchemy.exc import SQLAlchemyError
from db.connection import get_db
from db.models import Transaction
from services.account_service import update_account_balance

def create_transaction(account_id: int, transaction_type: str, amount: Decimal, description: str = None):
    """
    Record a transaction for the given account.
    transaction_type must be 'Deposit', 'Withdrawal', or 'Transfer'.
    For 'Deposit' and 'Withdrawal', the account balance is updated accordingly.
    Returns the new Transaction object.
    """
    if transaction_type not in ['Deposit', 'Withdrawal', 'Transfer']:
        raise ValueError("Invalid transaction type. Must be 'Deposit', 'Withdrawal', or 'Transfer'.")
    
    # Update the account balance before recording the transaction.
    if transaction_type == 'Deposit':
        update_account_balance(account_id, amount, operation="add")
    elif transaction_type == 'Withdrawal':
        update_account_balance(account_id, amount, operation="subtract")
    # For 'Transfer', you might implement separate logic (e.g., updating two accounts).

    db_gen = get_db()
    db = next(db_gen)
    try:
        new_transaction = Transaction(
            account_id=account_id,
            transaction_type=transaction_type,
            amount=amount,
            description=description
        )
        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)
        return new_transaction
    except SQLAlchemyError as e:
        db.rollback()
        logging.exception("Database error during transaction creation for account_id %s", account_id)
        raise e
    except Exception as e:
        db.rollback()
        logging.exception("Error creating transaction for account_id %s", account_id)
        raise e
    finally:
        try:
            db_gen.close()
        except Exception:
            pass

def get_transactions_by_account(account_id: int):
    """
    Retrieve all transactions for a specific account.
    Returns a list of Transaction objects.
    """
    db_gen = get_db()
    db = next(db_gen)
    try:
        transactions = db.query(Transaction).filter_by(account_id=account_id).all()
        return transactions
    except Exception as e:
        logging.exception("Error retrieving transactions for account_id %s", account_id)
        raise e
    finally:
        try:
            db_gen.close()
        except Exception:
            pass