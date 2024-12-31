from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging
from typing import List
from datetime import date

from app.schemas.alert import AlertCreate, AlertResponse, AlertUpdate
from app.services.alert import (
   create_alert,
   get_alert_by_id,
   get_user_alerts,
   update_alert,
   delete_alert,
   mark_alert_as_read,
   get_user_unread_alerts
)
from app.database import get_db

logger = logging.getLogger(__name__)

router = APIRouter(
   prefix="/alerts",
   tags=["alerts"],
   responses={
       400: {"description": "Bad Request - Invalid alert data"},
       404: {"description": "Alert not found"},
       500: {"description": "Internal Server Error"}
   }
)

@router.post(
   "/",
   response_model=AlertResponse,
   status_code=status.HTTP_201_CREATED,
   summary="Create a new alert",
   description="Create a new alert or notification for a user"
)
async def create_alert_endpoint(
   alert_data: AlertCreate,
   db_session: Session = Depends(get_db)
) -> AlertResponse:
   """
   Create a new alert with:
   
   - **user_id**: ID of the user who should receive this alert
   - **message**: Alert message content
   - **type**: Type of alert (budget, bill, or goal)
   - **trigger_date**: When the alert should be triggered
   """
   try:
       logger.info(f"Creating new alert for user: {alert_data.user_id}")
       return await create_alert(db_session, alert_data)
   except Exception as e:
       logger.error(f"Error in create_alert endpoint: {str(e)}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="An unexpected error occurred while creating the alert"
       ) from e

@router.get(
   "/user/{user_id}",
   response_model=List[AlertResponse],
   summary="Get user alerts",
   description="Retrieve all alerts for a specific user"
)
async def get_user_alerts_endpoint(
   user_id: int,
   unread_only: bool = False,
   db_session: Session = Depends(get_db)
) -> List[AlertResponse]:
   """
   Retrieve alerts for a specific user.
   
   - **user_id**: ID of the user to get alerts for
   - **unread_only**: If true, return only unread alerts
   """
   try:
       if unread_only:
           return await get_user_unread_alerts(db_session, user_id)
       return await get_user_alerts(db_session, user_id)
   except Exception as e:
       logger.error(f"Error retrieving alerts for user {user_id}: {str(e)}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Error retrieving user alerts"
       ) from e

@router.patch(
   "/{alert_id}/read",
   response_model=AlertResponse,
   summary="Mark alert as read",
   description="Mark a specific alert as read"
)
async def mark_alert_read_endpoint(
   alert_id: int,
   db_session: Session = Depends(get_db)
) -> AlertResponse:
   """
   Mark an alert as read.
   
   - **alert_id**: ID of the alert to mark as read
   """
   try:
       return await mark_alert_as_read(db_session, alert_id)
   except HTTPException:
       raise
   except Exception as e:
       logger.error(f"Error marking alert {alert_id} as read: {str(e)}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Error updating alert"
       ) from e

@router.put(
   "/{alert_id}",
   response_model=AlertResponse,
   summary="Update alert",
   description="Update an existing alert"
)
async def update_alert_endpoint(
   alert_id: int,
   alert_data: AlertUpdate,
   db_session: Session = Depends(get_db)
) -> AlertResponse:
   """
   Update an existing alert.
   
   - **alert_id**: ID of the alert to update
   """
   try:
       return await update_alert(db_session, alert_id, alert_data)
   except HTTPException:
       raise
   except Exception as e:
       logger.error(f"Error updating alert {alert_id}: {str(e)}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Error updating alert"
       ) from e

@router.delete(
   "/{alert_id}",
   status_code=status.HTTP_204_NO_CONTENT,
   summary="Delete alert",
   description="Delete an existing alert"
)
async def delete_alert_endpoint(
   alert_id: int,
   db_session: Session = Depends(get_db)
):
   """
   Delete an alert.
   
   - **alert_id**: ID of the alert to delete
   """
   try:
       await delete_alert(db_session, alert_id)
   except HTTPException:
       raise
   except Exception as e:
       logger.error(f"Error deleting alert {alert_id}: {str(e)}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Error deleting alert"
       ) from e