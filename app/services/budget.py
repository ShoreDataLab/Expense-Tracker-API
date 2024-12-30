from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException, status
import logging

from app.models.budget import Budget
from app.schemas.budget import BudgetCreate, BudgetUpdate

logger = logging.getLogger(__name__)

async def create_budget(db: Session, budget_data: BudgetCreate) -> Budget:
   """
   Create a new budget in the database.
   
   Args:
       db: Database session
       budget_data: Budget data from request

   Returns:
       Budget: Created budget object

   Raises:
       HTTPException: If budget creation fails or related entities don't exist
   """
   try:
       logger.info(f"Creating budget for user: {budget_data.user_id}, category: {budget_data.category_id}")
       
       # Create budget instance
       db_budget = Budget(
           user_id=budget_data.user_id,
           category_id=budget_data.category_id,
           amount=budget_data.amount,
           start_date=budget_data.start_date,
           end_date=budget_data.end_date
       )
       
       db.add(db_budget)
       db.commit()
       db.refresh(db_budget)
       
       logger.info(f"Successfully created budget with ID: {db_budget.id}")
       return db_budget

   except IntegrityError as e:
       db.rollback()
       logger.error(f"Integrity error creating budget: {e}")
       raise HTTPException(
           status_code=status.HTTP_400_BAD_REQUEST,
           detail="Invalid budget data. Check user_id and category_id exist."
       )
   except SQLAlchemyError as e:
       db.rollback()
       logger.error(f"Database error creating budget: {e}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Database error while creating budget"
       )
   except Exception as e:
       db.rollback()
       logger.error(f"Unexpected error creating budget: {e}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Unexpected error occurred"
       )

async def get_budget_by_id(db: Session, budget_id: int) -> Budget:
   """
   Retrieve a specific budget by its ID.
   
   Args:
       db: Database session
       budget_id: ID of the budget to retrieve

   Returns:
       Budget: Budget object if found

   Raises:
       HTTPException: If budget not found
   """
   budget = db.query(Budget).filter(Budget.id == budget_id).first()
   if not budget:
       raise HTTPException(
           status_code=status.HTTP_404_NOT_FOUND,
           detail=f"Budget with ID {budget_id} not found"
       )
   return budget

async def get_user_budgets(db: Session, user_id: int) -> list[Budget]:
   """
   Retrieve all budgets for a specific user.
   
   Args:
       db: Database session
       user_id: ID of the user to get budgets for

   Returns:
       list[Budget]: List of user's budgets
   """
   try:
       return db.query(Budget).filter(Budget.user_id == user_id).all()
   except Exception as e:
       logger.error(f"Error retrieving budgets for user {user_id}: {e}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Error retrieving user budgets"
       )

async def get_category_budgets(db: Session, category_id: int) -> list[Budget]:
   """
   Retrieve all budgets for a specific category.
   
   Args:
       db: Database session
       category_id: ID of the category to get budgets for

   Returns:
       list[Budget]: List of budgets for the category
   """
   try:
       return db.query(Budget).filter(Budget.category_id == category_id).all()
   except Exception as e:
       logger.error(f"Error retrieving budgets for category {category_id}: {e}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Error retrieving category budgets"
       )

async def update_budget(
   db: Session,
   budget_id: int,
   budget_data: BudgetUpdate
) -> Budget:
   """
   Update an existing budget.
   
   Args:
       db: Database session
       budget_id: ID of the budget to update
       budget_data: New budget data

   Returns:
       Budget: Updated budget object

   Raises:
       HTTPException: If budget not found or update fails
   """
   try:
       db_budget = await get_budget_by_id(db, budget_id)
       
       # Update only provided fields
       update_data = budget_data.dict(exclude_unset=True)
       for field, value in update_data.items():
           setattr(db_budget, field, value)
       
       db.commit()
       db.refresh(db_budget)
       return db_budget

   except HTTPException:
       raise
   except Exception as e:
       db.rollback()
       logger.error(f"Error updating budget {budget_id}: {e}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Error updating budget"
       )

async def delete_budget(db: Session, budget_id: int):
   """
   Delete a budget.
   
   Args:
       db: Database session
       budget_id: ID of the budget to delete

   Raises:
       HTTPException: If budget not found or deletion fails
   """
   try:
       db_budget = await get_budget_by_id(db, budget_id)
       db.delete(db_budget)
       db.commit()
       
   except HTTPException:
       raise
   except Exception as e:
       db.rollback()
       logger.error(f"Error deleting budget {budget_id}: {e}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Error deleting budget"
       )