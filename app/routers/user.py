from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import logging

from app.schemas.user import UserCreate, UserResponse
from app.services.user import create_user
from app.database import get_db

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={
        400: {"description": "Bad Request - Invalid input or duplicate user"},
        500: {"description": "Internal Server Error"}
    }
)

@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account with profile information."
)
async def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
) -> UserResponse:
    """
    Register a new user with the following information:
    
    - **email**: Valid email address
    - **username**: Username (3-50 characters)
    - **password**: Secure password (8-50 characters)
    - **first_name**: User's first name
    - **last_name**: User's last name
    """
    try:
        return create_user(db, user_data)
    except Exception as e:
        logger.error(f"Error in register_user endpoint: {str(e)}")
        raise