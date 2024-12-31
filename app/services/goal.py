from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException, status
from decimal import Decimal
import logging

from app.models.goal import Goal
from app.schemas.goal import GoalCreate, GoalUpdate, GoalStatus

logger = logging.getLogger(__name__)

async def create_goal(db: Session, goal_data: GoalCreate) -> Goal:
   """
   Create a new goal in the database.
   
   Args:
       db: Database session
       goal_data: Goal data from request

   Returns:
       Goal: Created goal object

   Raises:
       HTTPException: If goal creation fails or related entities don't exist
   """
   try:
       logger.info(f"Creating goal for user: {goal_data.user_id}")
       
       # Create goal instance
       db_goal = Goal(
           user_id=goal_data.user_id,
           name=goal_data.name,
           description=goal_data.description,
           target_amount=goal_data.target_amount,
           current_amount=goal_data.current_amount,
           start_date=goal_data.start_date,
           end_date=goal_data.end_date,
           status=goal_data.status
       )
       
       db.add(db_goal)
       db.commit()
       db.refresh(db_goal)
       
       logger.info(f"Successfully created goal with ID: {db_goal.id}")
       return db_goal

   except IntegrityError as e:
       db.rollback()
       logger.error(f"Integrity error creating goal: {e}")
       raise HTTPException(
           status_code=status.HTTP_400_BAD_REQUEST,
           detail="Invalid goal data. Check user_id exists."
       )
   except SQLAlchemyError as e:
       db.rollback()
       logger.error(f"Database error creating goal: {e}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Database error while creating goal"
       )
   except Exception as e:
       db.rollback()
       logger.error(f"Unexpected error creating goal: {e}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Unexpected error occurred"
       )

async def get_goal_by_id(db: Session, goal_id: int) -> Goal:
   """
   Retrieve a specific goal by its ID.
   
   Args:
       db: Database session
       goal_id: ID of the goal to retrieve

   Returns:
       Goal: Goal object if found

   Raises:
       HTTPException: If goal not found
   """
   goal = db.query(Goal).filter(Goal.id == goal_id).first()
   if not goal:
       raise HTTPException(
           status_code=status.HTTP_404_NOT_FOUND,
           detail=f"Goal with ID {goal_id} not found"
       )
   return goal

async def get_user_goals(
   db: Session, 
   user_id: int, 
   status: GoalStatus = None
) -> list[Goal]:
   """
   Retrieve all goals for a specific user.
   
   Args:
       db: Database session
       user_id: ID of the user to get goals for
       status: Optional status to filter goals by

   Returns:
       list[Goal]: List of user's goals
   """
   try:
       query = db.query(Goal).filter(Goal.user_id == user_id)
       if status:
           query = query.filter(Goal.status == status)
       return query.all()
   except Exception as e:
       logger.error(f"Error retrieving goals for user {user_id}: {e}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Error retrieving user goals"
       )

async def update_goal_progress(
   db: Session,
   goal_id: int,
   current_amount: float
) -> Goal:
   """
   Update a goal's current amount and status.
   
   Args:
       db: Database session
       goal_id: ID of the goal to update
       current_amount: New current amount

   Returns:
       Goal: Updated goal object
   """
   try:
       goal = await get_goal_by_id(db, goal_id)
       goal.current_amount = Decimal(str(current_amount))
       
       # Update status if goal is achieved
       if goal.current_amount >= goal.target_amount:
           goal.status = GoalStatus.ACHIEVED
       elif goal.status == GoalStatus.ACHIEVED and goal.current_amount < goal.target_amount:
           goal.status = GoalStatus.IN_PROGRESS
           
       db.commit()
       db.refresh(goal)
       return goal
       
   except HTTPException:
       raise
   except Exception as e:
       db.rollback()
       logger.error(f"Error updating goal progress {goal_id}: {e}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Error updating goal progress"
       )

async def update_goal(
   db: Session,
   goal_id: int,
   goal_data: GoalUpdate
) -> Goal:
   """
   Update an existing goal.
   
   Args:
       db: Database session
       goal_id: ID of the goal to update
       goal_data: New goal data

   Returns:
       Goal: Updated goal object
   """
   try:
       goal = await get_goal_by_id(db, goal_id)
       
       # Update only provided fields
       update_data = goal_data.dict(exclude_unset=True)
       for field, value in update_data.items():
           setattr(goal, field, value)
           
       # Check if status should be updated based on amounts
       if hasattr(goal_data, 'current_amount') or hasattr(goal_data, 'target_amount'):
           if goal.current_amount >= goal.target_amount:
               goal.status = GoalStatus.ACHIEVED
           elif goal.status == GoalStatus.ACHIEVED:
               goal.status = GoalStatus.IN_PROGRESS
       
       db.commit()
       db.refresh(goal)
       return goal
       
   except HTTPException:
       raise
   except Exception as e:
       db.rollback()
       logger.error(f"Error updating goal {goal_id}: {e}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Error updating goal"
       )

async def delete_goal(db: Session, goal_id: int):
   """
   Delete a goal.
   
   Args:
       db: Database session
       goal_id: ID of the goal to delete
   """
   try:
       goal = await get_goal_by_id(db, goal_id)
       db.delete(goal)
       db.commit()
   except HTTPException:
       raise
   except Exception as e:
       db.rollback()
       logger.error(f"Error deleting goal {goal_id}: {e}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Error deleting goal"
       )