# db/connection.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base  # Import the Base class from models.py

# Database connection URL
# Format: mysql+pymysql://<username>:<password>@<host>/<database_name>
DATABASE_URL = "mysql+pymysql://vault_app_user:AVNS_5FuZQyHkHtS6ObQbxXj@vault-db-bank-application.h.aivencloud.com:14867/vault-db"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)  # Set echo=False in production

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()