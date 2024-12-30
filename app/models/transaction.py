from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class Transaction(Base):
    """
    SQLAlchemy model representing a financial transaction.

    Attributes:
        id (int): Primary key and unique identifier for the transaction
        account_id (int): Foreign key referencing the Account table
        category_id (int): Foreign key referencing the Category table
        amount (decimal): Amount of the transaction
        description (str): Optional description or note for the transaction
        date (date): Date when the transaction occurred
        type (enum): Type of transaction (income or expense)
        created_at (datetime): Timestamp when the transaction was created
        updated_at (datetime): Timestamp when the transaction was last updated
    """
    __tablename__ = "Transaction"

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey('Account.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('Category.id'), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    description = Column(String(255), nullable=True)
    date = Column(DateTime, nullable=False)
    type = Column(Enum('income', 'expense', name='transaction_type'), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, nullable=True, onupdate=func.now())

    # Relationships
    account = relationship("Account", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")

    def __repr__(self):
        return f"Transaction(id={self.id}, type={self.type}, amount={self.amount}, date={self.date})"