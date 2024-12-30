from pydantic import BaseModel, constr
from typing import Optional
from datetime import datetime

class CategoryBase(BaseModel):
    name: str = constr(min_length=3, max_length=50)
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # Use this instead of orm_mode=True as it's newer

    def __str__(self):
        return f"Category(id={self.id}, name={self.name}, description={self.description})"