# db/models.py
from sqlalchemy import Column, Integer, String, Enum, DECIMAL, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

# Base class for declarative models
Base = declarative_base()

class User(Base):
    __tablename__ = 'Users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(15))
    created_at = Column(DateTime, default=func.now())

    def __repr__(self):
        return f"<User(user_id={self.user_id}, username={self.username}, email={self.email})>"

class Account(Base):
    __tablename__ = 'Accounts'

    account_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('Users.user_id'), nullable=False)
    account_type = Column(Enum('Savings', 'Current'), nullable=False)
    balance = Column(DECIMAL(15, 2), default=0.00)
    created_at = Column(DateTime, default=func.now())

    def __repr__(self):
        return f"<Account(account_id={self.account_id}, user_id={self.user_id}, balance={self.balance})>"

class Transaction(Base):
    __tablename__ = 'Transactions'

    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey('Accounts.account_id'), nullable=False)
    transaction_type = Column(Enum('Deposit', 'Withdrawal', 'Transfer'), nullable=False)
    amount = Column(DECIMAL(15, 2), nullable=False)
    timestamp = Column(DateTime, default=func.now())
    description = Column(String(255))

    def __repr__(self):
        return f"<Transaction(transaction_id={self.transaction_id}, account_id={self.account_id}, amount={self.amount})>"

class AuditLog(Base):
    __tablename__ = 'AuditLogs'

    log_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('Users.user_id'), nullable=False)
    action = Column(String(255), nullable=False)
    timestamp = Column(DateTime, default=func.now())

    def __repr__(self):
        return f"<AuditLog(log_id={self.log_id}, user_id={self.user_id}, action={self.action})>"