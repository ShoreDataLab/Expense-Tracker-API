from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class AlertType(str, Enum):
   """Enumeration for alert types."""
   BUDGET = 'budget'
   BILL = 'bill'
   GOAL = 'goal'

class AlertBase(BaseModel):
   """
   Base Alert schema with common attributes.
   
   Attributes:
       user_id: ID of the user who owns this alert
       message: Text content of the alert
       type: Type of alert (budget, bill, or goal)
       trigger_date: Date when the alert should be triggered
       is_read: Whether the alert has been read
   """
   user_id: int = Field(..., gt=0)
   message: str = Field(..., min_length=1, max_length=255)
   type: AlertType
   trigger_date: datetime
   is_read: bool = Field(default=False)

class AlertCreate(AlertBase):
   """Schema for creating a new alert."""
   pass

class AlertResponse(AlertBase):
   """
   Schema for alert responses, including database fields.
   
   Extends AlertBase to add database-specific fields:
       id: Unique identifier for the alert
       created_at: Timestamp when the alert was created
       updated_at: Timestamp when the alert was last updated
   """
   id: int
   created_at: datetime
   updated_at: Optional[datetime] = None

   class Config:
       from_attributes = True

   def __str__(self):
       return (
           f"Alert(id={self.id}, "
           f"type={self.type}, "
           f"trigger_date={self.trigger_date}, "
           f"is_read={self.is_read})"
       )

class AlertUpdate(BaseModel):
   """
   Schema for updating an existing alert.
   All fields are optional since updates can be partial.
   """
   message: Optional[str] = Field(None, min_length=1, max_length=255)
   type: Optional[AlertType] = None
   trigger_date: Optional[datetime] = None
   is_read: Optional[bool] = None