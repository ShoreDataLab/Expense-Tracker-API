from sqlalchemy import Column, Integer, DECIMAL, DateTime, Date, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class Budget(Base):
   """
   SQLAlchemy model representing a budget.

   Attributes:
       id (int): Primary key and unique identifier for the budget
       user_id (int): Foreign key referencing the User table
       category_id (int): Foreign key referencing the Category table
       amount (decimal): Budgeted amount for the category
       start_date (date): Start date of the budget period
       end_date (date): End date of the budget period
       created_at (datetime): Timestamp when the budget was created
       updated_at (datetime): Timestamp when the budget was last updated
   """
   __tablename__ = "Budget"

   id = Column(Integer, primary_key=True, autoincrement=True)
   user_id = Column(Integer, ForeignKey('User.id', ondelete='CASCADE'), nullable=False)
   category_id = Column(Integer, ForeignKey('Category.id'), nullable=False)
   amount = Column(DECIMAL(10, 2), nullable=False)
   start_date = Column(Date, nullable=False)
   end_date = Column(Date, nullable=False)
   created_at = Column(DateTime, server_default=func.now(), nullable=False)
   updated_at = Column(DateTime, nullable=True, onupdate=func.now())

   # Relationships
   user = relationship("User", back_populates="budgets")
   category = relationship("Category", back_populates="budgets")

   def __repr__(self):
       return (
           f"Budget(id={self.id}, "
           f"category_id={self.category_id}, "
           f"amount={self.amount}, "
           f"period={self.start_date} to {self.end_date})"
       )