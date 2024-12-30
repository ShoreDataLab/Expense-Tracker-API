from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal
from enum import Enum

class TransactionType(str, Enum):
   """Enumeration for transaction types."""
   INCOME = 'income'
   EXPENSE = 'expense'

class TransactionBase(BaseModel):
   """
   Base Transaction schema with common attributes.
   
   Attributes:
       account_id: ID of the account for this transaction
       category_id: ID of the category for this transaction
       amount: Transaction amount (positive for income, negative for expense)
       description: Optional description of the transaction
       date: Date when the transaction occurred
       type: Type of transaction (income or expense)
   """
   account_id: int = Field(..., gt=0)
   category_id: int = Field(..., gt=0)
   amount: Decimal = Field(..., decimal_places=2)
   description: Optional[str] = Field(None, max_length=255)
   date: datetime
   type: TransactionType

class TransactionCreate(TransactionBase):
   """Schema for creating a new transaction."""
   pass

class TransactionResponse(TransactionBase):
   """
   Schema for transaction responses, including database fields.
   
   Extends TransactionBase to add database-specific fields:
       id: Unique identifier for the transaction
       created_at: Timestamp when the transaction was created
       updated_at: Timestamp when the transaction was last updated
   """
   id: int
   created_at: datetime
   updated_at: Optional[datetime] = None

   class Config:
       from_attributes = True

   def __str__(self):
       return (
           f"Transaction(id={self.id}, "
           f"type={self.type}, "
           f"amount={self.amount}, "
           f"date={self.date})"
       )