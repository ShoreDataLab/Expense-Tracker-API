from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException, status
import logging

from app.models.account import Account
from app.schemas.account import AccountCreate

logger = logging.getLogger(__name__)

async def create_account(db: Session, account_data: AccountCreate) -> Account:
    """
    Create a new account in the database.
    
    Args:
        db: Database session
        account_data: Account creation data from request

    Returns:
        Account: Created account object

    Raises:
        HTTPException: If account creation fails or related entities don't exist
    """
    try:
        logger.info(f"Creating account: {account_data.name} for user {account_data.user_id}")
        
        # Create account instance
        db_account = Account(
            name=account_data.name,
            type=account_data.type,
            balance=account_data.balance,
            currency_id=account_data.currency_id,
            user_id=account_data.user_id
        )
        
        db.add(db_account)
        db.commit()
        db.refresh(db_account)
        
        logger.info(f"Successfully created account with ID: {db_account.id}")
        return db_account

    except IntegrityError as e:
        db.rollback()
        logger.error(f"Integrity error creating account: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid account data. Check user_id and currency_id exist."
        )
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error creating account: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error while creating account"
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error creating account: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error occurred"
        )

async def get_account_by_id(db: Session, account_id: int) -> Account:
    """
    Retrieve a specific account by its ID.
    
    Args:
        db: Database session
        account_id: ID of the account to retrieve

    Returns:
        Account: Account object if found

    Raises:
        HTTPException: If account not found
    """
    try:
        account = db.query(Account).filter(Account.id == account_id).first()
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Account with ID {account_id} not found"
            )
        return account
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving account {account_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving account"
        )

async def get_user_accounts(db: Session, user_id: int) -> list[Account]:
    """
    Retrieve all accounts belonging to a specific user.
    
    Args:
        db: Database session
        user_id: ID of the user whose accounts to retrieve

    Returns:
        list[Account]: List of user's accounts

    Raises:
        HTTPException: If database error occurs
    """
    try:
        return db.query(Account).filter(Account.user_id == user_id).all()
    except Exception as e:
        logger.error(f"Error retrieving accounts for user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving user accounts"
        )