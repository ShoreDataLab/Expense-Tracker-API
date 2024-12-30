from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class Alert(Base):
   """
   SQLAlchemy model representing an alert/notification.

   Attributes:
       id (int): Primary key and unique identifier for the alert
       user_id (int): Foreign key referencing the User table
       message (str): Alert message or notification text
       type (enum): Type of the alert (budget, bill, goal)
       trigger_date (datetime): Date when the alert should be triggered
       is_read (bool): Indicates whether the alert has been read by the user
       created_at (datetime): Timestamp when the alert was created
       updated_at (datetime): Timestamp when the alert was last updated
   """
   __tablename__ = "Alert"

   id = Column(Integer, primary_key=True, autoincrement=True)
   user_id = Column(Integer, ForeignKey('User.id', ondelete='CASCADE'), nullable=False)
   message = Column(String(255), nullable=False)
   type = Column(Enum('budget', 'bill', 'goal', name='alert_type'), nullable=False)
   trigger_date = Column(DateTime, nullable=False)
   is_read = Column(Boolean, nullable=False, default=False)
   created_at = Column(DateTime, server_default=func.now(), nullable=False)
   updated_at = Column(DateTime, nullable=True, onupdate=func.now())

   # Relationships
   user = relationship("User", back_populates="alerts")

   def __repr__(self):
       return (
           f"Alert(id={self.id}, "
           f"type={self.type}, "
           f"trigger_date={self.trigger_date}, "
           f"is_read={self.is_read})"
       )