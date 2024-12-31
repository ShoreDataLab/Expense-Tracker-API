from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, ForeignKey, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class Expense(Base):
   """
   SQLAlchemy model representing an expense.

   Attributes:
       id (int): Primary key and unique identifier for the expense
       user_id (int): Foreign key referencing the User table
       category_id (int): Foreign key referencing the Category table
       account_id (int): Foreign key referencing the Account table
       amount (decimal): Amount of the expense
       description (str): Optional description of the expense
       date (date): Date when the expense occurred
       created_at (datetime): Timestamp when the expense was created
       updated_at (datetime): Timestamp when the expense was last updated
   """
   __tablename__ = "Expense"

   id = Column(Integer, primary_key=True, autoincrement=True)
   user_id = Column(Integer, ForeignKey('User.id', ondelete='CASCADE'), nullable=False)
   category_id = Column(Integer, ForeignKey('Category.id'), nullable=False)
   account_id = Column(Integer, ForeignKey('Account.id'), nullable=False)
   amount = Column(DECIMAL(10, 2), nullable=False)
   description = Column(String(255), nullable=True)
   date = Column(Date, nullable=False)
   created_at = Column(DateTime, server_default=func.now(), nullable=False)
   updated_at = Column(DateTime, nullable=True, onupdate=func.now())

   # Relationships
   user = relationship("User", back_populates="expenses")
   category = relationship("Category", back_populates="expenses")
   account = relationship("Account", back_populates="expenses")

   def __repr__(self):
       return (
           f"Expense(id={self.id}, "
           f"amount={self.amount}, "
           f"category_id={self.category_id}, "
           f"date={self.date})"
       )