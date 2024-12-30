from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import logging

from app.schemas.category import CategoryCreate, CategoryResponse
from app.services.category import create_category
from app.database import get_db

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/categories",
    tags=["categories"],
    responses={
        400: {"description": "Bad Request - Category already exists"},
        500: {"description": "Internal Server Error"}
    }
)

@router.post(
    "/",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new category",
    description="Create a new expense category with name and optional description"
)
async def create_new_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db)
) -> CategoryResponse:
    """Create a new category."""
    try:
        return await create_category(db, category_data)
    except Exception as e:
        logger.error(f"Error in create_category endpoint: {str(e)}")
        raise