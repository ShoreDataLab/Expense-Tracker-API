from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging
from typing import List
from datetime import date

from app.schemas.expense import ExpenseCreate, ExpenseResponse, ExpenseUpdate
from app.services.expense import (
   create_expense,
   get_expense_by_id,
   get_user_expenses,
   get_account_expenses,
   get_category_expenses,
   update_expense,
   delete_expense
)
from app.database import get_db

logger = logging.getLogger(__name__)

router = APIRouter(
   prefix="/expenses",
   tags=["expenses"],
   responses={
       400: {"description": "Bad Request - Invalid expense data"},
       404: {"description": "Expense not found"},
       500: {"description": "Internal Server Error"}
   }
)

@router.post(
   "/",
   response_model=ExpenseResponse,
   status_code=status.HTTP_201_CREATED,
   summary="Create a new expense",
   description="Create a new expense record"
)
async def create_expense_endpoint(
   expense_data: ExpenseCreate,
   db_session: Session = Depends(get_db)
) -> ExpenseResponse:
   """
   Create a new expense with:
   
   - **user_id**: ID of the user who owns this expense
   - **category_id**: ID of the category this expense belongs to
   - **account_id**: ID of the account this expense is from
   - **amount**: Amount of the expense
   - **description**: Optional description of the expense
   - **date**: Date when the expense occurred
   """
   try:
       logger.info(f"Creating new expense for user: {expense_data.user_id}")
       return await create_expense(db_session, expense_data)
   except Exception as e:
       logger.error(f"Error in create_expense endpoint: {str(e)}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="An unexpected error occurred while creating the expense"
       ) from e

@router.get(
   "/user/{user_id}",
   response_model=List[ExpenseResponse],
   summary="Get user expenses",
   description="Retrieve all expenses for a specific user"
)
async def get_user_expenses_endpoint(
   user_id: int,
   start_date: date = None,
   end_date: date = None,
   db_session: Session = Depends(get_db)
) -> List[ExpenseResponse]:
   """
   Retrieve expenses for a specific user with optional date filtering.
   
   - **user_id**: ID of the user to get expenses for
   - **start_date**: Optional start date for filtering
   - **end_date**: Optional end date for filtering
   """
   try:
       return await get_user_expenses(db_session, user_id, start_date, end_date)
   except Exception as e:
       logger.error(f"Error retrieving expenses for user {user_id}: {str(e)}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Error retrieving user expenses"
       ) from e

@router.get(
   "/account/{account_id}",
   response_model=List[ExpenseResponse],
   summary="Get account expenses",
   description="Retrieve all expenses for a specific account"
)
async def get_account_expenses_endpoint(
   account_id: int,
   db_session: Session = Depends(get_db)
) -> List[ExpenseResponse]:
   """
   Retrieve expenses for a specific account.
   
   - **account_id**: ID of the account to get expenses for
   """
   try:
       return await get_account_expenses(db_session, account_id)
   except Exception as e:
       logger.error(f"Error retrieving expenses for account {account_id}: {str(e)}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Error retrieving account expenses"
       ) from e

@router.get(
   "/category/{category_id}",
   response_model=List[ExpenseResponse],
   summary="Get category expenses",
   description="Retrieve all expenses for a specific category"
)
async def get_category_expenses_endpoint(
   category_id: int,
   db_session: Session = Depends(get_db)
) -> List[ExpenseResponse]:
   """
   Retrieve expenses for a specific category.
   
   - **category_id**: ID of the category to get expenses for
   """
   try:
       return await get_category_expenses(db_session, category_id)
   except Exception as e:
       logger.error(f"Error retrieving expenses for category {category_id}: {str(e)}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Error retrieving category expenses"
       ) from e

@router.put(
   "/{expense_id}",
   response_model=ExpenseResponse,
   summary="Update expense",
   description="Update an existing expense"
)
async def update_expense_endpoint(
   expense_id: int,
   expense_data: ExpenseUpdate,
   db_session: Session = Depends(get_db)
) -> ExpenseResponse:
   """
   Update an existing expense.
   
   - **expense_id**: ID of the expense to update
   """
   try:
       return await update_expense(db_session, expense_id, expense_data)
   except HTTPException:
       raise
   except Exception as e:
       logger.error(f"Error updating expense {expense_id}: {str(e)}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Error updating expense"
       ) from e

@router.delete(
   "/{expense_id}",
   status_code=status.HTTP_204_NO_CONTENT,
   summary="Delete expense",
   description="Delete an existing expense"
)
async def delete_expense_endpoint(
   expense_id: int,
   db_session: Session = Depends(get_db)
):
   """
   Delete an expense.
   
   - **expense_id**: ID of the expense to delete
   """
   try:
       await delete_expense(db_session, expense_id)
   except HTTPException:
       raise
   except Exception as e:
       logger.error(f"Error deleting expense {expense_id}: {str(e)}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Error deleting expense"
       ) from e