from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException, status
import logging

from app.models.recurring_transaction import RecurringTransaction
from app.schemas.recurring_transaction import RecurringTransactionCreate

logger = logging.getLogger(__name__)

async def create_recurring_transaction(
   db: Session, 
   transaction_data: RecurringTransactionCreate
) -> RecurringTransaction:
   """
   Create a new recurring transaction in the database.
   
   Args:
       db: Database session
       transaction_data: Recurring transaction data from request

   Returns:
       RecurringTransaction: Created recurring transaction object

   Raises:
       HTTPException: If transaction creation fails or related entities don't exist
   """
   try:
       logger.info(f"Creating recurring transaction for account: {transaction_data.account_id}")
       
       # Create recurring transaction instance
       db_transaction = RecurringTransaction(
           account_id=transaction_data.account_id,
           category_id=transaction_data.category_id,
           amount=transaction_data.amount,
           description=transaction_data.description,
           start_date=transaction_data.start_date,
           end_date=transaction_data.end_date,
           frequency=transaction_data.frequency
       )
       
       db.add(db_transaction)
       db.commit()
       db.refresh(db_transaction)
       
       logger.info(f"Successfully created recurring transaction with ID: {db_transaction.id}")
       return db_transaction

   except IntegrityError as e:
       db.rollback()
       logger.error(f"Integrity error creating recurring transaction: {e}")
       raise HTTPException(
           status_code=status.HTTP_400_BAD_REQUEST,
           detail="Invalid recurring transaction data. Check account_id and category_id exist."
       )
   except SQLAlchemyError as e:
       db.rollback()
       logger.error(f"Database error creating recurring transaction: {e}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Database error while creating recurring transaction"
       )
   except Exception as e:
       db.rollback()
       logger.error(f"Unexpected error creating recurring transaction: {e}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Unexpected error occurred"
       )

async def get_user_recurring_transactions(db: Session, user_id: int) -> list[RecurringTransaction]:
   """
   Retrieve all recurring transactions for a specific user across all their accounts.
   
   Args:
       db: Database session
       user_id: ID of the user to get recurring transactions for

   Returns:
       list[RecurringTransaction]: List of user's recurring transactions
   """
   try:
       return (
           db.query(RecurringTransaction)
           .join(RecurringTransaction.account)
           .filter(RecurringTransaction.account.has(user_id=user_id))
           .all()
       )
   except Exception as e:
       logger.error(f"Error retrieving recurring transactions for user {user_id}: {e}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Error retrieving user recurring transactions"
       )

async def get_account_recurring_transactions(
   db: Session, 
   account_id: int
) -> list[RecurringTransaction]:
   """
   Retrieve all recurring transactions for a specific account.
   
   Args:
       db: Database session
       account_id: ID of the account to get recurring transactions for

   Returns:
       list[RecurringTransaction]: List of recurring transactions for the account
   """
   try:
       return db.query(RecurringTransaction).filter(
           RecurringTransaction.account_id == account_id
       ).all()
   except Exception as e:
       logger.error(f"Error retrieving recurring transactions for account {account_id}: {e}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Error retrieving account recurring transactions"
       )

async def update_recurring_transaction(
   db: Session,
   transaction_id: int,
   transaction_data: RecurringTransactionCreate
) -> RecurringTransaction:
   """
   Update an existing recurring transaction.
   
   Args:
       db: Database session
       transaction_id: ID of the transaction to update
       transaction_data: New transaction data

   Returns:
       RecurringTransaction: Updated recurring transaction object
   """
   try:
       db_transaction = db.query(RecurringTransaction).filter(
           RecurringTransaction.id == transaction_id
       ).first()
       
       if not db_transaction:
           raise HTTPException(
               status_code=status.HTTP_404_NOT_FOUND,
               detail=f"Recurring transaction with ID {transaction_id} not found"
           )
       
       # Update transaction fields
       for key, value in transaction_data.dict().items():
           setattr(db_transaction, key, value)
       
       db.commit()
       db.refresh(db_transaction)
       return db_transaction

   except HTTPException:
       raise
   except Exception as e:
       db.rollback()
       logger.error(f"Error updating recurring transaction {transaction_id}: {e}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Error updating recurring transaction"
       )

async def delete_recurring_transaction(db: Session, transaction_id: int):
   """
   Delete a recurring transaction.
   
   Args:
       db: Database session
       transaction_id: ID of the transaction to delete
   """
   try:
       db_transaction = db.query(RecurringTransaction).filter(
           RecurringTransaction.id == transaction_id
       ).first()
       
       if not db_transaction:
           raise HTTPException(
               status_code=status.HTTP_404_NOT_FOUND,
               detail=f"Recurring transaction with ID {transaction_id} not found"
           )
       
       db.delete(db_transaction)
       db.commit()

   except HTTPException:
       raise
   except Exception as e:
       db.rollback()
       logger.error(f"Error deleting recurring transaction {transaction_id}: {e}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Error deleting recurring transaction"
       )