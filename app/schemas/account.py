from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal

class AccountBase(BaseModel):
    """
    Base Account schema with common attributes.
    
    Attributes:
        name: Name of the account (e.g., "Main Checking", "Savings")
        type: Type of account (e.g., "checking", "savings", "credit")
        balance: Current balance of the account
    """
    name: str = Field(..., min_length=3, max_length=255)
    type: str = Field(..., min_length=1, max_length=255)
    balance: Decimal = Field(..., decimal_places=2, ge=0)
    currency_id: int = Field(..., gt=0)
    user_id: int = Field(..., gt=0)

class AccountCreate(AccountBase):
    """Schema for creating a new account."""
    pass

class AccountResponse(AccountBase):
    """
    Schema for account responses, including database fields.
    
    Extends AccountBase to add database-specific fields:
        id: Unique identifier for the account
        created_at: Timestamp when the account was created
        updated_at: Timestamp when the account was last updated
    """
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        
    def __str__(self):
        return f"Account(id={self.id}, name={self.name}, type={self.type}, balance={self.balance})"