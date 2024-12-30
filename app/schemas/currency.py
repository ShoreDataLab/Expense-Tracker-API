from pydantic import BaseModel, Field
from typing import Optional

class CurrencyBase(BaseModel):
    """
    Base Currency schema with common attributes.
    
    Attributes:
        code: Three-letter ISO currency code (e.g., USD, EUR, GBP)
        name: Full name of the currency (e.g., US Dollar)
        symbol: Currency symbol (e.g., $, €, £)
    """
    code: str = Field(..., min_length=3, max_length=3, pattern=r'^[A-Z]{3}$')
    name: str = Field(..., min_length=1, max_length=255)
    symbol: str = Field(..., min_length=1, max_length=10)

class CurrencyCreate(CurrencyBase):
    """Schema for creating a new currency."""
    pass

class CurrencyResponse(CurrencyBase):
    """
    Schema for currency responses, including database fields.
    
    Extends CurrencyBase to add database-specific fields:
        id: Unique identifier for the currency
    """
    id: int

    class Config:
        from_attributes = True

    def __str__(self):
        return f"Currency(id={self.id}, code={self.code}, symbol={self.symbol})"