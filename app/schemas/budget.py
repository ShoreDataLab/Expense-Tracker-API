from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date, datetime
from decimal import Decimal

class BudgetBase(BaseModel):
    """
    Base Budget schema with common attributes.
    
    Attributes:
        user_id: ID of the user who owns this budget
        category_id: ID of the category this budget is for
        amount: Budgeted amount for the category
        start_date: Start date of the budget period
        end_date: End date of the budget period
    """
    user_id: int = Field(..., gt=0)
    category_id: int = Field(..., gt=0)
    amount: Decimal = Field(..., decimal_places=2, ge=0)
    start_date: date
    end_date: date

    @field_validator('end_date')
    def end_date_must_be_after_start_date(cls, v: date, info) -> date:
        """Validate that end_date is after start_date."""
        start_date = info.data.get('start_date')
        if v and start_date and v < start_date:
            raise ValueError('end_date must be after start_date')
        return v

    @field_validator('amount')
    def amount_must_be_positive(cls, v: Decimal) -> Decimal:
        """Validate that budget amount is positive."""
        if v <= 0:
            raise ValueError('amount must be greater than 0')
        return v

class BudgetCreate(BudgetBase):
    """Schema for creating a new budget."""
    pass

class BudgetResponse(BudgetBase):
    """
    Schema for budget responses, including database fields.
    
    Extends BudgetBase to add database-specific fields:
        id: Unique identifier for the budget
        created_at: Timestamp when the budget was created
        updated_at: Timestamp when the budget was last updated
    """
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

    def __str__(self):
        return (
            f"Budget(id={self.id}, "
            f"category_id={self.category_id}, "
            f"amount={self.amount}, "
            f"period={self.start_date} to {self.end_date})"
        )

class BudgetUpdate(BaseModel):
    """
    Schema for updating an existing budget.
    All fields are optional since updates can be partial.
    """
    amount: Optional[Decimal] = Field(None, decimal_places=2, ge=0)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    category_id: Optional[int] = Field(None, gt=0)

    @field_validator('end_date')
    def end_date_must_be_after_start_date(cls, v: Optional[date], info) -> Optional[date]:
        """Validate that end_date is after start_date if both are provided."""
        start_date = info.data.get('start_date')
        if v and start_date and v < start_date:
            raise ValueError('end_date must be after start_date')
        return v