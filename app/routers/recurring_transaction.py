from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging
from typing import List
from datetime import date

from app.schemas.recurring_transaction import RecurringTransactionCreate, RecurringTransactionResponse
from app.services.recurring_transaction import (
   create_recurring_transaction,
   get_recurring_transaction_by_id,
   get_user_recurring_transactions,
   get_account_recurring_transactions,
   update_recurring_transaction,
   delete_recurring_transaction
)
from app.database import get_db

logger = logging.getLogger(__name__)

router = APIRouter(
   prefix="/recurring-transactions",
   tags=["recurring transactions"],
   responses={
       400: {"description": "Bad Request - Invalid data"},
       404: {"description": "Recurring transaction not found"},
       500: {"description": "Internal Server Error"}
   }
)

@router.post(
   "/",
   response_model=RecurringTransactionResponse,
   status_code=status.HTTP_201_CREATED,
   summary="Create a new recurring transaction",
   description="Create a new recurring transaction for scheduled payments or income"
)
async def create_recurring_transaction_endpoint(
   transaction_data: RecurringTransactionCreate,
   db_session: Session = Depends(get_db)
) -> RecurringTransactionResponse:
   """
   Create a new recurring transaction with:
   
   - **account_id**: ID of the account for this transaction
   - **category_id**: ID of the category for this transaction
   - **amount**: Transaction amount
   - **description**: Optional description of the transaction
   - **start_date**: Date when the recurring transaction should start
   - **end_date**: Optional date when the recurring transaction should end
   - **frequency**: How often the transaction should occur (daily/weekly/monthly/yearly)
   """
   try:
       logger.info(f"Creating new recurring transaction for account: {transaction_data.account_id}")
       return await create_recurring_transaction(db_session, transaction_data)
   except Exception as e:
       logger.error(f"Error in create_recurring_transaction endpoint: {str(e)}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="An unexpected error occurred while creating the recurring transaction"
       ) from e

@router.get(
   "/account/{account_id}",
   response_model=List[RecurringTransactionResponse],
   summary="Get account recurring transactions",
   description="Retrieve all recurring transactions for a specific account"
)
async def get_account_recurring_transactions_endpoint(
   account_id: int,
   db_session: Session = Depends(get_db)
) -> List[RecurringTransactionResponse]:
   """
   Retrieve all recurring transactions for a specific account.
   
   - **account_id**: ID of the account to get recurring transactions for
   """
   try:
       return await get_account_recurring_transactions(db_session, account_id)
   except Exception as e:
       logger.error(f"Error retrieving recurring transactions for account {account_id}: {str(e)}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Error retrieving account recurring transactions"
       ) from e

@router.get(
   "/user/{user_id}",
   response_model=List[RecurringTransactionResponse],
   summary="Get user recurring transactions",
   description="Retrieve all recurring transactions for a specific user across all their accounts"
)
async def get_user_recurring_transactions_endpoint(
   user_id: int,
   db_session: Session = Depends(get_db)
) -> List[RecurringTransactionResponse]:
   """
   Retrieve all recurring transactions for a specific user.
   
   - **user_id**: ID of the user to get recurring transactions for
   """
   try:
       return await get_user_recurring_transactions(db_session, user_id)
   except Exception as e:
       logger.error(f"Error retrieving recurring transactions for user {user_id}: {str(e)}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Error retrieving user recurring transactions"
       ) from e

@router.put(
   "/{transaction_id}",
   response_model=RecurringTransactionResponse,
   summary="Update recurring transaction",
   description="Update an existing recurring transaction"
)
async def update_recurring_transaction_endpoint(
   transaction_id: int,
   transaction_data: RecurringTransactionCreate,
   db_session: Session = Depends(get_db)
) -> RecurringTransactionResponse:
   """
   Update an existing recurring transaction.
   
   - **transaction_id**: ID of the recurring transaction to update
   """
   try:
       return await update_recurring_transaction(db_session, transaction_id, transaction_data)
   except HTTPException:
       raise
   except Exception as e:
       logger.error(f"Error updating recurring transaction {transaction_id}: {str(e)}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Error updating recurring transaction"
       ) from e

@router.delete(
   "/{transaction_id}",
   status_code=status.HTTP_204_NO_CONTENT,
   summary="Delete recurring transaction",
   description="Delete an existing recurring transaction"
)
async def delete_recurring_transaction_endpoint(
   transaction_id: int,
   db_session: Session = Depends(get_db)
):
   """
   Delete a recurring transaction.
   
   - **transaction_id**: ID of the recurring transaction to delete
   """
   try:
       await delete_recurring_transaction(db_session, transaction_id)
   except HTTPException:
       raise
   except Exception as e:
       logger.error(f"Error deleting recurring transaction {transaction_id}: {str(e)}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Error deleting recurring transaction"
       ) from e