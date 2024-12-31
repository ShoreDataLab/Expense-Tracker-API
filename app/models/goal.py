from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, Enum, ForeignKey, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class Goal(Base):
   """
   SQLAlchemy model representing a financial goal.

   Attributes:
       id (int): Primary key and unique identifier for the goal
       user_id (int): Foreign key referencing the User table
       name (str): Name or title of the goal
       description (str): Optional description of the goal
       target_amount (decimal): Target amount to be achieved
       current_amount (decimal): Current amount saved towards the goal
       start_date (date): Start date of the goal
       end_date (date): Target end date of the goal
       status (enum): Current status of the goal (in_progress, achieved, abandoned)
       created_at (datetime): Timestamp when the goal was created
       updated_at (datetime): Timestamp when the goal was last updated
   """
   __tablename__ = "Goal"

   id = Column(Integer, primary_key=True, autoincrement=True)
   user_id = Column(Integer, ForeignKey('User.id', ondelete='CASCADE'), nullable=False)
   name = Column(String(255), nullable=False)
   description = Column(String(255), nullable=True)
   target_amount = Column(DECIMAL(10, 2), nullable=False)
   current_amount = Column(DECIMAL(10, 2), nullable=False, default=0.00)
   start_date = Column(Date, nullable=False)
   end_date = Column(Date, nullable=False)
   status = Column(
       Enum('in_progress', 'achieved', 'abandoned', name='goal_status'),
       nullable=False,
       default='in_progress'
   )
   created_at = Column(DateTime, server_default=func.now(), nullable=False)
   updated_at = Column(DateTime, nullable=True, onupdate=func.now())

   # Relationships
   user = relationship("User", back_populates="goals")

   def __repr__(self):
       return (
           f"Goal(id={self.id}, "
           f"name={self.name}, "
           f"status={self.status}, "
           f"target={self.target_amount})"
       )