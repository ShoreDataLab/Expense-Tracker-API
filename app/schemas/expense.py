from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from decimal import Decimal

class ExpenseBase(BaseModel):
    """
    Base Expense schema with common attributes.
    
    Attributes:
        user_id: ID of the user who owns this expense
        category_id: ID of the category this expense belongs to
        account_id: ID of the account this expense is from
        amount: Amount of the expense
        description: Optional description of the expense
        date: Date when the expense occurred
    """
    user_id: int = Field(..., gt=0)
    category_id: int = Field(..., gt=0)
    account_id: int = Field(..., gt=0)
    amount: Decimal = Field(..., decimal_places=2, gt=0)
    description: Optional[str] = Field(None, max_length=255)
    date: datetime

class ExpenseCreate(ExpenseBase):
    """Schema for creating a new expense."""
    pass

class ExpenseResponse(ExpenseBase):
    """
    Schema for expense responses, including database fields.
    
    Extends ExpenseBase to add database-specific fields:
        id: Unique identifier for the expense
        created_at: Timestamp when the expense was created
        updated_at: Timestamp when the expense was last updated
    """
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

    def __str__(self):
        return (
            f"Expense(id={self.id}, "
            f"amount={self.amount}, "
            f"category_id={self.category_id}, "
            f"date={self.date})"
        )

class ExpenseUpdate(BaseModel):
    """
    Schema for updating an existing expense.
    All fields are optional since updates can be partial.
    """
    category_id: Optional[int] = Field(None, gt=0)
    account_id: Optional[int] = Field(None, gt=0)
    amount: Optional[Decimal] = Field(None, decimal_places=2, gt=0)
    description: Optional[str] = Field(None, max_length=255)
    date: Optional[datetime] = None