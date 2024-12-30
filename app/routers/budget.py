from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging
from typing import List
from datetime import date

from app.schemas.budget import BudgetCreate, BudgetResponse, BudgetUpdate
from app.services.budget import (
    create_budget,
    get_budget_by_id,
    get_user_budgets,
    get_category_budgets,
    update_budget,
    delete_budget
)
from app.database import get_db

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/budgets",
    tags=["budgets"],
    responses={
        400: {"description": "Bad Request - Invalid budget data"},
        404: {"description": "Budget not found"},
        500: {"description": "Internal Server Error"}
    }
)

@router.post(
    "/",
    response_model=BudgetResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new budget",
    description="Create a new budget for a specific category and time period"
)
async def create_budget_endpoint(
    budget_data: BudgetCreate,
    db_session: Session = Depends(get_db)
) -> BudgetResponse:
    """
    Create a new budget with:
    
    - **user_id**: ID of the user who owns this budget
    - **category_id**: ID of the category this budget is for
    - **amount**: Budgeted amount for the category
    - **start_date**: Start date of the budget period
    - **end_date**: End date of the budget period
    """
    try:
        logger.info(f"Creating new budget for category: {budget_data.category_id}")
        return await create_budget(db_session, budget_data)
    except Exception as e:
        logger.error(f"Error in create_budget endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating the budget"
        ) from e

@router.get(
    "/user/{user_id}",
    response_model=List[BudgetResponse],
    summary="Get user budgets",
    description="Retrieve all budgets for a specific user"
)
async def get_user_budgets_endpoint(
    user_id: int,
    db_session: Session = Depends(get_db)
) -> List[BudgetResponse]:
    """
    Retrieve all budgets for a specific user.
    
    - **user_id**: ID of the user to get budgets for
    """
    try:
        return await get_user_budgets(db_session, user_id)
    except Exception as e:
        logger.error(f"Error retrieving budgets for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving user budgets"
        ) from e

@router.get(
    "/{budget_id}",
    response_model=BudgetResponse,
    summary="Get budget by ID",
    description="Retrieve a specific budget by its ID"
)
async def get_budget_endpoint(
    budget_id: int,
    db_session: Session = Depends(get_db)
) -> BudgetResponse:
    """
    Retrieve a specific budget by its ID.
    
    - **budget_id**: ID of the budget to retrieve
    """
    try:
        budget = await get_budget_by_id(db_session, budget_id)
        if not budget:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Budget with ID {budget_id} not found"
            )
        return budget
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving budget {budget_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving budget"
        ) from e

@router.get(
    "/category/{category_id}",
    response_model=List[BudgetResponse],
    summary="Get category budgets",
    description="Retrieve all budgets for a specific category"
)
async def get_category_budgets_endpoint(
    category_id: int,
    db_session: Session = Depends(get_db)
) -> List[BudgetResponse]:
    """
    Retrieve all budgets for a specific category.
    
    - **category_id**: ID of the category to get budgets for
    """
    try:
        return await get_category_budgets(db_session, category_id)
    except Exception as e:
        logger.error(f"Error retrieving budgets for category {category_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving category budgets"
        ) from e

@router.put(
    "/{budget_id}",
    response_model=BudgetResponse,
    summary="Update budget",
    description="Update an existing budget"
)
async def update_budget_endpoint(
    budget_id: int,
    budget_data: BudgetUpdate,
    db_session: Session = Depends(get_db)
) -> BudgetResponse:
    """
    Update an existing budget.
    
    - **budget_id**: ID of the budget to update
    """
    try:
        return await update_budget(db_session, budget_id, budget_data)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating budget {budget_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating budget"
        ) from e

@router.delete(
    "/{budget_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete budget",
    description="Delete an existing budget"
)
async def delete_budget_endpoint(
    budget_id: int,
    db_session: Session = Depends(get_db)
):
    """
    Delete a budget.
    
    - **budget_id**: ID of the budget to delete
    """
    try:
        await delete_budget(db_session, budget_id)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting budget {budget_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting budget"
        ) from e