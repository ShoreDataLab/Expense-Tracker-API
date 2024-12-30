from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging

from app.schemas.account import AccountCreate, AccountResponse
from app.services.account import create_account, get_user_accounts, get_account_by_id
from app.database import get_db

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/accounts",
    tags=["accounts"],
    responses={
        400: {"description": "Bad Request - Invalid account data"},
        404: {"description": "Account not found"},
        500: {"description": "Internal Server Error"}
    }
)

@router.post(
    "/", 
    status_code=status.HTTP_201_CREATED, 
    response_model=AccountResponse,
    summary="Create a new account",
    description="Create a new financial account with specified details"
)
async def create_account_endpoint(
    account_creation_data: AccountCreate, 
    db_session: Session = Depends(get_db)
) -> AccountResponse:
    """
    Create a new financial account with the following information:
    
    - **name**: Name of the account (e.g., "Main Checking", "Savings")
    - **type**: Type of account (e.g., "checking", "savings", "credit card")
    - **balance**: Initial balance of the account
    - **currency_id**: ID of the currency for this account (must exist in Currency table)
    - **user_id**: ID of the user who owns this account (must exist in User table)
    """
    try:
        logger.info(f"Creating new account: {account_creation_data.name}")
        return await create_account(db_session, account_creation_data)
    except Exception as e:
        logger.error(f"Error in create_account endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating the account"
        ) from e

@router.get(
    "/user/{user_id}",
    response_model=list[AccountResponse],
    summary="Get user accounts",
    description="Retrieve all accounts belonging to a specific user"
)
async def get_user_accounts_endpoint(
    user_id: int,
    db_session: Session = Depends(get_db)
) -> list[AccountResponse]:
    """
    Retrieve all accounts for a specific user.
    
    - **user_id**: ID of the user whose accounts to retrieve
    """
    try:
        return await get_user_accounts(db_session, user_id)
    except Exception as e:
        logger.error(f"Error retrieving accounts for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while retrieving accounts"
        ) from e

@router.get(
    "/{account_id}",
    response_model=AccountResponse,
    summary="Get account by ID",
    description="Retrieve a specific account by its ID"
)
async def get_account_endpoint(
    account_id: int,
    db_session: Session = Depends(get_db)
) -> AccountResponse:
    """
    Retrieve a specific account by its ID.
    
    - **account_id**: ID of the account to retrieve
    """
    try:
        account = await get_account_by_id(db_session, account_id)
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Account with ID {account_id} not found"
            )
        return account
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving account {account_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while retrieving the account"
        ) from e