from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException, status
import logging

from app.models.alert import Alert
from app.schemas.alert import AlertCreate, AlertUpdate

logger = logging.getLogger(__name__)

async def create_alert(db: Session, alert_data: AlertCreate) -> Alert:
   """
   Create a new alert in the database.
   
   Args:
       db: Database session
       alert_data: Alert data from request

   Returns:
       Alert: Created alert object

   Raises:
       HTTPException: If alert creation fails or related entities don't exist
   """
   try:
       logger.info(f"Creating alert for user: {alert_data.user_id}")
       
       # Create alert instance
       db_alert = Alert(
           user_id=alert_data.user_id,
           message=alert_data.message,
           type=alert_data.type,
           trigger_date=alert_data.trigger_date,
           is_read=alert_data.is_read
       )
       
       db.add(db_alert)
       db.commit()
       db.refresh(db_alert)
       
       logger.info(f"Successfully created alert with ID: {db_alert.id}")
       return db_alert

   except IntegrityError as e:
       db.rollback()
       logger.error(f"Integrity error creating alert: {e}")
       raise HTTPException(
           status_code=status.HTTP_400_BAD_REQUEST,
           detail="Invalid alert data. Check user_id exists."
       )
   except SQLAlchemyError as e:
       db.rollback()
       logger.error(f"Database error creating alert: {e}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Database error while creating alert"
       )
   except Exception as e:
       db.rollback()
       logger.error(f"Unexpected error creating alert: {e}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Unexpected error occurred"
       )

async def get_alert_by_id(db: Session, alert_id: int) -> Alert:
   """
   Retrieve a specific alert by its ID.
   
   Args:
       db: Database session
       alert_id: ID of the alert to retrieve

   Returns:
       Alert: Alert object if found

   Raises:
       HTTPException: If alert not found
   """
   alert = db.query(Alert).filter(Alert.id == alert_id).first()
   if not alert:
       raise HTTPException(
           status_code=status.HTTP_404_NOT_FOUND,
           detail=f"Alert with ID {alert_id} not found"
       )
   return alert

async def get_user_alerts(db: Session, user_id: int) -> list[Alert]:
   """
   Retrieve all alerts for a specific user.
   
   Args:
       db: Database session
       user_id: ID of the user to get alerts for

   Returns:
       list[Alert]: List of user's alerts
   """
   try:
       return db.query(Alert).filter(Alert.user_id == user_id).all()
   except Exception as e:
       logger.error(f"Error retrieving alerts for user {user_id}: {e}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Error retrieving user alerts"
       )

async def get_user_unread_alerts(db: Session, user_id: int) -> list[Alert]:
   """
   Retrieve all unread alerts for a specific user.
   
   Args:
       db: Database session
       user_id: ID of the user to get unread alerts for

   Returns:
       list[Alert]: List of user's unread alerts
   """
   try:
       return db.query(Alert).filter(
           Alert.user_id == user_id,
           Alert.is_read == False
       ).all()
   except Exception as e:
       logger.error(f"Error retrieving unread alerts for user {user_id}: {e}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Error retrieving unread alerts"
       )

async def mark_alert_as_read(db: Session, alert_id: int) -> Alert:
   """
   Mark an alert as read.
   
   Args:
       db: Database session
       alert_id: ID of the alert to mark as read

   Returns:
       Alert: Updated alert object
   """
   try:
       alert = await get_alert_by_id(db, alert_id)
       alert.is_read = True
       db.commit()
       db.refresh(alert)
       return alert
   except HTTPException:
       raise
   except Exception as e:
       db.rollback()
       logger.error(f"Error marking alert {alert_id} as read: {e}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Error updating alert"
       )

async def update_alert(
   db: Session,
   alert_id: int,
   alert_data: AlertUpdate
) -> Alert:
   """
   Update an existing alert.
   
   Args:
       db: Database session
       alert_id: ID of the alert to update
       alert_data: New alert data

   Returns:
       Alert: Updated alert object
   """
   try:
       alert = await get_alert_by_id(db, alert_id)
       
       # Update only provided fields
       update_data = alert_data.dict(exclude_unset=True)
       for field, value in update_data.items():
           setattr(alert, field, value)
       
       db.commit()
       db.refresh(alert)
       return alert
   except HTTPException:
       raise
   except Exception as e:
       db.rollback()
       logger.error(f"Error updating alert {alert_id}: {e}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Error updating alert"
       )

async def delete_alert(db: Session, alert_id: int):
   """
   Delete an alert.
   
   Args:
       db: Database session
       alert_id: ID of the alert to delete
   """
   try:
       alert = await get_alert_by_id(db, alert_id)
       db.delete(alert)
       db.commit()
   except HTTPException:
       raise
   except Exception as e:
       db.rollback()
       logger.error(f"Error deleting alert {alert_id}: {e}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Error deleting alert"
       )