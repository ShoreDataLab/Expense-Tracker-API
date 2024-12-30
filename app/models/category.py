from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base

class Category(Base):
   """
   SQLAlchemy model representing a spending category.

   Attributes:
       id (int): Primary key and unique identifier for the category
       name (str): Name of the category, must be unique
       description (str): Optional description of the category
       created_at (datetime): Timestamp when the category was created
       updated_at (datetime): Timestamp when the category was last updated
   """
   
   __tablename__ = "Category"
   
   id = Column(Integer, primary_key=True, autoincrement=True, index=True)
   name = Column(String(255), unique=True, nullable=False)
   description = Column(String(255), nullable=True)
   created_at = Column(DateTime, server_default=func.now(), nullable=False)
   updated_at = Column(DateTime, nullable=True, onupdate=func.now())

   transactions = relationship("Transaction", back_populates="category")
   recurring_transactions = relationship("RecurringTransaction", back_populates="category")
   budgets = relationship("Budget", back_populates="category")

   def __repr__(self):
       return f"Category(id={self.id}, name={self.name})"