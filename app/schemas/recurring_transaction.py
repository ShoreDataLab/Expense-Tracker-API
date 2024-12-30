from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from decimal import Decimal
from enum import Enum

class FrequencyType(str, Enum):
   """Enumeration for recurring transaction frequency types."""
   DAILY = 'daily'
   WEEKLY = 'weekly'
   MONTHLY = 'monthly'
   YEARLY = 'yearly'

class RecurringTransactionBase(BaseModel):
   """
   Base Recurring Transaction schema with common attributes.
   
   Attributes:
       account_id: ID of the account for this recurring transaction
       category_id: ID of the category for this recurring transaction
       amount: Transaction amount
       description: Optional description of the recurring transaction
       start_date: Date when the recurring transaction should start
       end_date: Optional date when the recurring transaction should end
       frequency: How often the transaction should occur
   """
   account_id: int = Field(..., gt=0)
   category_id: int = Field(..., gt=0)
   amount: Decimal = Field(..., decimal_places=2, ge=0)
   description: Optional[str] = Field(None, max_length=255)
   start_date: date
   end_date: Optional[date] = None
   frequency: FrequencyType

   @validator('end_date')
   def end_date_must_be_after_start_date(cls, v, values):
       if v and 'start_date' in values and v < values['start_date']:
           raise ValueError('end_date must be after start_date')
       return v

class RecurringTransactionCreate(RecurringTransactionBase):
   """Schema for creating a new recurring transaction."""
   pass

class RecurringTransactionResponse(RecurringTransactionBase):
   """
   Schema for recurring transaction responses, including database fields.
   
   Extends RecurringTransactionBase to add database-specific fields:
       id: Unique identifier for the recurring transaction
       created_at: Timestamp when the recurring transaction was created
       updated_at: Timestamp when the recurring transaction was last updated
   """
   id: int
   created_at: datetime
   updated_at: Optional[datetime] = None

   class Config:
       from_attributes = True

   def __str__(self):
       return (
           f"RecurringTransaction(id={self.id}, "
           f"amount={self.amount}, "
           f"frequency={self.frequency}, "
           f"start_date={self.start_date})"
       )