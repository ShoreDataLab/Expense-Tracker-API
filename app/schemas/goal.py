from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date, datetime
from decimal import Decimal
from enum import Enum

class GoalStatus(str, Enum):
   """Enumeration for goal status types."""
   IN_PROGRESS = 'in_progress'
   ACHIEVED = 'achieved'
   ABANDONED = 'abandoned'

class GoalBase(BaseModel):
   """
   Base Goal schema with common attributes.
   
   Attributes:
       user_id: ID of the user who owns this goal
       name: Name or title of the goal
       description: Optional description of the goal
       target_amount: Target amount to be achieved
       current_amount: Current amount saved towards the goal
       start_date: Start date of the goal
       end_date: End date of the goal
       status: Current status of the goal
   """
   user_id: int = Field(..., gt=0)
   name: str = Field(..., min_length=1, max_length=255)
   description: Optional[str] = Field(None, max_length=255)
   target_amount: Decimal = Field(..., decimal_places=2, gt=0)
   current_amount: Decimal = Field(default=0, decimal_places=2, ge=0)
   start_date: date
   end_date: date
   status: GoalStatus = Field(default=GoalStatus.IN_PROGRESS)

   @field_validator('end_date')
   def end_date_must_be_after_start_date(cls, v: date, info) -> date:
       """Validate that end_date is after start_date."""
       start_date = info.data.get('start_date')
       if v and start_date and v < start_date:
           raise ValueError('end_date must be after start_date')
       return v

   @field_validator('current_amount')
   def current_amount_must_not_exceed_target(cls, v: Decimal, info) -> Decimal:
       """Validate that current_amount does not exceed target_amount."""
       target_amount = info.data.get('target_amount')
       if target_amount and v > target_amount:
           raise ValueError('current_amount cannot exceed target_amount')
       return v

class GoalCreate(GoalBase):
   """Schema for creating a new goal."""
   pass

class GoalResponse(GoalBase):
   """
   Schema for goal responses, including database fields.
   
   Extends GoalBase to add database-specific fields:
       id: Unique identifier for the goal
       created_at: Timestamp when the goal was created
       updated_at: Timestamp when the goal was last updated
   """
   id: int
   created_at: datetime
   updated_at: Optional[datetime] = None

   class Config:
       from_attributes = True

   def __str__(self):
       return (
           f"Goal(id={self.id}, "
           f"name={self.name}, "
           f"status={self.status}, "
           f"progress={self.current_amount}/{self.target_amount})"
       )

class GoalUpdate(BaseModel):
   """
   Schema for updating an existing goal.
   All fields are optional since updates can be partial.
   """
   name: Optional[str] = Field(None, min_length=1, max_length=255)
   description: Optional[str] = Field(None, max_length=255)
   target_amount: Optional[Decimal] = Field(None, decimal_places=2, gt=0)
   current_amount: Optional[Decimal] = Field(None, decimal_places=2, ge=0)
   start_date: Optional[date] = None
   end_date: Optional[date] = None
   status: Optional[GoalStatus] = None

   @field_validator('end_date')
   def validate_end_date(cls, v: Optional[date], info) -> Optional[date]:
       """Validate end_date if provided."""
       if v is not None:
           start_date = info.data.get('start_date')
           if start_date and v < start_date:
               raise ValueError('end_date must be after start_date')
       return v