from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from datetime import datetime

# Base Models
class UserBase(BaseModel):
    email: EmailStr
    username: constr(min_length=3, max_length=50)

class UserProfileBase(BaseModel):
    first_name: str
    last_name: str
    avatar: Optional[str] = None

# Create Models
class UserCreate(UserBase):
    password: constr(min_length=8, max_length=50)
    first_name: str
    last_name: str

# Response Models
class UserProfileResponse(UserProfileBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    profile: Optional[UserProfileResponse] = None

    class Config:
        from_attributes = True

# Optional: Simple response for lists or when profile isn't needed
class UserSimple(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True