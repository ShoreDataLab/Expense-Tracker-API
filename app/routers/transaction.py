from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging
from typing import List
from datetime import date

from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.services.transaction import (
    create_transaction, 
    get_transaction_by_id,
    get_user_transactions,
    get_account_transactions,
    get_transactions_by_date_range
)
from app.database import get_db

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
    responses={
        400: {"description": "Bad Request - Invalid data"},
        404: {"description": "Transaction not found"},
        500: {"description": "Internal Server Error"}
    }
)

@router.post(
    "/", 
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new transaction",
    description="Create a new financial transaction for an account"
)
async def create_transaction_endpoint(
    transaction_data: TransactionCreate,
    db_session: Session = Depends(get_db)
) -> TransactionResponse:
    """
    Create a new financial transaction with:
    
    - **account_id**: ID of the account for this transaction
    - **category_id**: ID of the category for this transaction
    - **amount**: Transaction amount (positive for income, negative for expense)
    - **description**: Optional description of the transaction
    - **date**: Date of the transaction
    - **type**: Type of transaction (income or expense)
    """
    try:
        logger.info(f"Creating new transaction for account: {transaction_data.account_id}")
        return await create_transaction(db_session, transaction_data)
    except Exception as e:
        logger.error(f"Error in create_transaction endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating the transaction"
        ) from e

@router.get(
    "/account/{account_id}",
    response_model=List[TransactionResponse],
    summary="Get account transactions",
    description="Retrieve all transactions for a specific account"
)
async def get_account_transactions_endpoint(
    account_id: int,
    db_session: Session = Depends(get_db)
) -> List[TransactionResponse]:
    """
    Retrieve all transactions for a specific account.
    
    - **account_id**: ID of the account to get transactions for
    """
    try:
        return await get_account_transactions(db_session, account_id)
    except Exception as e:
        logger.error(f"Error retrieving transactions for account {account_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving account transactions"
        ) from e

@router.get(
    "/user/{user_id}",
    response_model=List[TransactionResponse],
    summary="Get user transactions",
    description="Retrieve all transactions for a specific user across all their accounts"
)
async def get_user_transactions_endpoint(
    user_id: int,
    db_session: Session = Depends(get_db)
) -> List[TransactionResponse]:
    """
    Retrieve all transactions for a specific user.
    
    - **user_id**: ID of the user to get transactions for
    """
    try:
        return await get_user_transactions(db_session, user_id)
    except Exception as e:
        logger.error(f"Error retrieving transactions for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving user transactions"
        ) from e

@router.get(
    "/date-range",
    response_model=List[TransactionResponse],
    summary="Get transactions by date range",
    description="Retrieve transactions within a specific date range"
)
async def get_transactions_by_date_range_endpoint(
    start_date: date,
    end_date: date,
    account_id: int = None,
    db_session: Session = Depends(get_db)
) -> List[TransactionResponse]:
    """
    Retrieve transactions within a date range.
    
    - **start_date**: Start date for transaction search
    - **end_date**: End date for transaction search
    - **account_id**: Optional account ID to filter transactions
    """
    try:
        return await get_transactions_by_date_range(
            db_session, 
            start_date, 
            end_date, 
            account_id
        )
    except Exception as e:
        logger.error(f"Error retrieving transactions for date range: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving transactions"
        ) from e

@router.get(
    "/{transaction_id}",
    response_model=TransactionResponse,
    summary="Get transaction by ID",
    description="Retrieve a specific transaction by its ID"
)
async def get_transaction_endpoint(
    transaction_id: int,
    db_session: Session = Depends(get_db)
) -> TransactionResponse:
    """
    Retrieve a specific transaction by its ID.
    
    - **transaction_id**: ID of the transaction to retrieve
    """
    try:
        transaction = await get_transaction_by_id(db_session, transaction_id)
        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Transaction with ID {transaction_id} not found"
            )
        return transaction
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving transaction {transaction_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving transaction"
        ) from e