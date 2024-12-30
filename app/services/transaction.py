from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException, status
from datetime import datetime, date
import logging

from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate

logger = logging.getLogger(__name__)

async def create_transaction(db: Session, transaction_data: TransactionCreate) -> Transaction:
   """
   Create a new transaction in the database.
   
   Args:
       db: Database session
       transaction_data: Transaction data from request

   Returns:
       Transaction: Created transaction object

   Raises:
       HTTPException: If transaction creation fails or related entities don't exist
   """
   try:
       logger.info(f"Creating transaction for account: {transaction_data.account_id}")
       
       # Create transaction instance
       db_transaction = Transaction(
           account_id=transaction_data.account_id,
           category_id=transaction_data.category_id,
           amount=transaction_data.amount,
           description=transaction_data.description,
           date=transaction_data.date,
           type=transaction_data.type
       )
       
       db.add(db_transaction)
       db.commit()
       db.refresh(db_transaction)
       
       logger.info(f"Successfully created transaction with ID: {db_transaction.id}")
       return db_transaction

   except IntegrityError as e:
       db.rollback()
       logger.error(f"Integrity error creating transaction: {e}")
       raise HTTPException(
           status_code=status.HTTP_400_BAD_REQUEST,
           detail="Invalid transaction data. Check account_id and category_id exist."
       )
   except SQLAlchemyError as e:
       db.rollback()
       logger.error(f"Database error creating transaction: {e}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Database error while creating transaction"
       )
   except Exception as e:
       db.rollback()
       logger.error(f"Unexpected error creating transaction: {e}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Unexpected error occurred"
       )

async def get_transaction_by_id(db: Session, transaction_id: int) -> Transaction:
   """
   Retrieve a specific transaction by its ID.
   
   Args:
       db: Database session
       transaction_id: ID of the transaction to retrieve

   Returns:
       Transaction: Transaction object if found

   Raises:
       HTTPException: If transaction not found
   """
   try:
       transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
       if not transaction:
           raise HTTPException(
               status_code=status.HTTP_404_NOT_FOUND,
               detail=f"Transaction with ID {transaction_id} not found"
           )
       return transaction
   except HTTPException:
       raise
   except Exception as e:
       logger.error(f"Error retrieving transaction {transaction_id}: {e}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Error retrieving transaction"
       )

async def get_account_transactions(db: Session, account_id: int) -> list[Transaction]:
   """
   Retrieve all transactions for a specific account.
   
   Args:
       db: Database session
       account_id: ID of the account to get transactions for

   Returns:
       list[Transaction]: List of transactions for the account
   """
   try:
       return db.query(Transaction).filter(Transaction.account_id == account_id).all()
   except Exception as e:
       logger.error(f"Error retrieving transactions for account {account_id}: {e}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Error retrieving account transactions"
       )

async def get_user_transactions(db: Session, user_id: int) -> list[Transaction]:
   """
   Retrieve all transactions for a specific user across all their accounts.
   
   Args:
       db: Database session
       user_id: ID of the user to get transactions for

   Returns:
       list[Transaction]: List of user's transactions
   """
   try:
       return (
           db.query(Transaction)
           .join(Transaction.account)
           .filter(Transaction.account.has(user_id=user_id))
           .all()
       )
   except Exception as e:
       logger.error(f"Error retrieving transactions for user {user_id}: {e}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Error retrieving user transactions"
       )

async def get_transactions_by_date_range(
   db: Session, 
   start_date: date, 
   end_date: date,
   account_id: int = None
) -> list[Transaction]:
   """
   Retrieve transactions within a specific date range.
   
   Args:
       db: Database session
       start_date: Start date for transaction search
       end_date: End date for transaction search
       account_id: Optional account ID to filter transactions

   Returns:
       list[Transaction]: List of transactions within the date range
   """
   try:
       query = db.query(Transaction).filter(
           Transaction.date >= start_date,
           Transaction.date <= end_date
       )
       
       if account_id:
           query = query.filter(Transaction.account_id == account_id)
           
       return query.all()
   except Exception as e:
       logger.error(f"Error retrieving transactions for date range: {e}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Error retrieving transactions"
       )