from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, Enum, ForeignKey, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class RecurringTransaction(Base):
    """
    SQLAlchemy model representing a recurring financial transaction.

    Attributes:
        id (int): Primary key and unique identifier for the recurring transaction
        account_id (int): Foreign key referencing the Account table
        category_id (int): Foreign key referencing the Category table
        amount (decimal): Amount of the recurring transaction
        description (str): Optional description or note for the transaction
        start_date (date): Start date of the recurring transaction
        end_date (date): Optional end date of the recurring transaction
        frequency (enum): Frequency of recurrence (daily, weekly, monthly, yearly)
        created_at (datetime): Timestamp when the recurring transaction was created
        updated_at (datetime): Timestamp when the recurring transaction was last updated
    """
    __tablename__ = "Recurring_Transaction"

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey('Account.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('Category.id'), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    description = Column(String(255), nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    frequency = Column(
        Enum('daily', 'weekly', 'monthly', 'yearly', name='recurring_frequency'), 
        nullable=False
    )
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, nullable=True, onupdate=func.now())

    # Relationships
    account = relationship("Account", back_populates="recurring_transactions")
    category = relationship("Category", back_populates="recurring_transactions")

    def __repr__(self):
        return (
            f"RecurringTransaction(id={self.id}, "
            f"amount={self.amount}, "
            f"frequency={self.frequency}, "
            f"start_date={self.start_date})"
        )