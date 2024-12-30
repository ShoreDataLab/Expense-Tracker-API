from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException, status
import logging

from app.models.category import Category
from app.schemas.category import CategoryCreate

# Configure logging
logger = logging.getLogger(__name__)

async def create_category(db: Session, category_data: CategoryCreate) -> Category:
    """Create a new category."""
    try:
        logger.info(f"Creating category with name: {category_data.name}")
        
        # Create category instance
        db_category = Category(
            name=category_data.name,
            description=category_data.description
        )
        
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        
        logger.info(f"Successfully created category with ID: {db_category.id}")
        return db_category

    except IntegrityError:
        db.rollback()
        logger.error("Category name already exists")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category name already exists"
        )
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error"
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error"
        )