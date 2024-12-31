from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException, status
from datetime import date
import logging

from app.models.expense import Expense
from app.schemas.expense import ExpenseCreate, ExpenseUpdate

logger = logging.getLogger(__name__)

async def create_expense(db: Session, expense_data: ExpenseCreate) -> Expense:
   """
   Create a new expense in the database.
   
   Args:
       db: Database session
       expense_data: Expense data from request

   Returns:
       Expense: Created expense object

   Raises:
       HTTPException: If expense creation fails or related entities don't exist
   """
   try:
       logger.info(f"Creating expense for user: {expense_data.user_id}")
       
       # Create expense instance
       db_expense = Expense(
           user_id=expense_data.user_id,
           category_id=expense_data.category_id,
           account_id=expense_data.account_id,
           amount=expense_data.amount,
           description=expense_data.description,
           date=expense_data.date
       )
       
       db.add(db_expense)
       db.commit()
       db.refresh(db_expense)
       
       logger.info(f"Successfully created expense with ID: {db_expense.id}")
       return db_expense

   except IntegrityError as e:
       db.rollback()
       logger.error(f"Integrity error creating expense: {e}")
       raise HTTPException(
           status_code=status.HTTP_400_BAD_REQUEST,
           detail="Invalid expense data. Check user_id, category_id, and account_id exist."
       )
   except SQLAlchemyError as e:
       db.rollback()
       logger.error(f"Database error creating expense: {e}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Database error while creating expense"
       )
   except Exception as e:
       db.rollback()
       logger.error(f"Unexpected error creating expense: {e}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Unexpected error occurred"
       )

async def get_expense_by_id(db: Session, expense_id: int) -> Expense:
   """
   Retrieve a specific expense by its ID.
   
   Args:
       db: Database session
       expense_id: ID of the expense to retrieve

   Returns:
       Expense: Expense object if found

   Raises:
       HTTPException: If expense not found
   """
   expense = db.query(Expense).filter(Expense.id == expense_id).first()
   if not expense:
       raise HTTPException(
           status_code=status.HTTP_404_NOT_FOUND,
           detail=f"Expense with ID {expense_id} not found"
       )
   return expense

async def get_user_expenses(
   db: Session, 
   user_id: int, 
   start_date: date = None,
   end_date: date = None
) -> list[Expense]:
   """
   Retrieve all expenses for a specific user with optional date filtering.
   
   Args:
       db: Database session
       user_id: ID of the user to get expenses for
       start_date: Optional start date for filtering
       end_date: Optional end date for filtering

   Returns:
       list[Expense]: List of user's expenses
   """
   try:
       query = db.query(Expense).filter(Expense.user_id == user_id)
       
       if start_date:
           query = query.filter(Expense.date >= start_date)
       if end_date:
           query = query.filter(Expense.date <= end_date)
           
       return query.order_by(Expense.date.desc()).all()
   except Exception as e:
       logger.error(f"Error retrieving expenses for user {user_id}: {e}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Error retrieving user expenses"
       )

async def get_account_expenses(db: Session, account_id: int) -> list[Expense]:
   """
   Retrieve all expenses for a specific account.
   
   Args:
       db: Database session
       account_id: ID of the account to get expenses for

   Returns:
       list[Expense]: List of expenses for the account
   """
   try:
       return db.query(Expense).filter(
           Expense.account_id == account_id
       ).order_by(Expense.date.desc()).all()
   except Exception as e:
       logger.error(f"Error retrieving expenses for account {account_id}: {e}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Error retrieving account expenses"
       )

async def get_category_expenses(db: Session, category_id: int) -> list[Expense]:
   """
   Retrieve all expenses for a specific category.
   
   Args:
       db: Database session
       category_id: ID of the category to get expenses for

   Returns:
       list[Expense]: List of expenses for the category
   """
   try:
       return db.query(Expense).filter(
           Expense.category_id == category_id
       ).order_by(Expense.date.desc()).all()
   except Exception as e:
       logger.error(f"Error retrieving expenses for category {category_id}: {e}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Error retrieving category expenses"
       )

async def update_expense(
   db: Session,
   expense_id: int,
   expense_data: ExpenseUpdate
) -> Expense:
   """
   Update an existing expense.
   
   Args:
       db: Database session
       expense_id: ID of the expense to update
       expense_data: New expense data

   Returns:
       Expense: Updated expense object
   """
   try:
       expense = await get_expense_by_id(db, expense_id)
       
       # Update only provided fields
       update_data = expense_data.dict(exclude_unset=True)
       for field, value in update_data.items():
           setattr(expense, field, value)
       
       db.commit()
       db.refresh(expense)
       return expense
       
   except HTTPException:
       raise
   except Exception as e:
       db.rollback()
       logger.error(f"Error updating expense {expense_id}: {e}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Error updating expense"
       )

async def delete_expense(db: Session, expense_id: int):
   """
   Delete an expense.
   
   Args:
       db: Database session
       expense_id: ID of the expense to delete
   """
   try:
       expense = await get_expense_by_id(db, expense_id)
       db.delete(expense)
       db.commit()
   except HTTPException:
       raise
   except Exception as e:
       db.rollback()
       logger.error(f"Error deleting expense {expense_id}: {e}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Error deleting expense"
       )