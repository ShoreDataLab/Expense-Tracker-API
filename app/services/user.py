from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException, status
import logging

from app.models.user import User, UserProfile
from app.schemas.user import UserCreate
from app.utils.security import get_password_hash

# Configure logging
logger = logging.getLogger(__name__)

def create_user(db: Session, user_data: UserCreate) -> User:
    """Create a new user with profile."""
    try:
        # Create user instance
        hashed_password = get_password_hash(user_data.password)
        db_user = User(
            email=user_data.email,
            username=user_data.username,
            password=hashed_password
        )
        logger.info(f"Creating user with email: {user_data.email}")
        
        db.add(db_user)
        db.flush()  # Flush to get the user ID

        # Create user profile
        db_profile = UserProfile(
            user_id=db_user.id,
            first_name=user_data.first_name,
            last_name=user_data.last_name
        )
        db.add(db_profile)
        db.commit()
        
        # Fetch the complete user with profile loaded
        complete_user = db.query(User).options(
            joinedload(User.profile)
        ).filter(User.id == db_user.id).first()
        
        logger.info(f"Successfully created user with ID: {complete_user.id}")
        return complete_user
            
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Integrity error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )
    
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error creating user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error occurred"
        )