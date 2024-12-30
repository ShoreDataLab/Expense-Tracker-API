from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base

class Account(Base):
    """
    SQLAlchemy model representing a financial account.

    Attributes:
        id (int): Primary key and unique identifier for the account
        user_id (int): Foreign key referencing the User table
        name (str): Name of the account (e.g., "Main Checking", "Savings")
        type (str): Type of account (e.g., "checking", "savings", "credit card")
        balance (decimal): Current balance of the account
        currency_id (int): Foreign key referencing the Currency table
        created_at (datetime): Timestamp when the account was created
        updated_at (datetime): Timestamp when the account was last updated
    """
    __tablename__ = "Account"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('User.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(255), nullable=False)
    type = Column(String(255), nullable=False)
    balance = Column(DECIMAL(10, 2), nullable=False, default=0.00)
    currency_id = Column(Integer, ForeignKey('Currency.id'), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, nullable=True, onupdate=func.now())

    # Relationships
    transactions = relationship("Transaction", back_populates="account")
    recurring_transactions = relationship("RecurringTransaction", back_populates="account")