from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException, status
import logging

from app.models.currency import Currency
from app.schemas.currency import CurrencyCreate

logger = logging.getLogger(__name__)

async def create_currency(db: Session, currency_data: CurrencyCreate) -> Currency:
   """
   Create a new currency in the database.
   
   Args:
       db: Database session
       currency_data: Currency data from request

   Returns:
       Currency: Created currency object

   Raises:
       HTTPException: If currency already exists or other database errors occur
   """
   try:
       logger.info(f"Creating currency with code: {currency_data.code}")
       
       # Create currency instance
       db_currency = Currency(
           code=currency_data.code.upper(),
           name=currency_data.name,
           symbol=currency_data.symbol
       )
       
       db.add(db_currency)
       db.commit()
       db.refresh(db_currency)
       
       logger.info(f"Successfully created currency with code: {db_currency.code}")
       return db_currency

   except IntegrityError:
       db.rollback()
       logger.error(f"Currency with code {currency_data.code} already exists")
       raise HTTPException(
           status_code=status.HTTP_400_BAD_REQUEST,
           detail=f"Currency with code {currency_data.code} already exists"
       )
   except SQLAlchemyError as e:
       db.rollback()
       logger.error(f"Database error creating currency: {e}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Error creating currency"
       )
   except Exception as e:
       db.rollback()
       logger.error(f"Unexpected error creating currency: {e}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Unexpected error occurred"
       )

async def get_all_currencies(db: Session) -> list[Currency]:
   """
   Retrieve all currencies from the database.
   
   Args:
       db: Database session

   Returns:
       list[Currency]: List of all currencies
   """
   try:
       return db.query(Currency).all()
   except Exception as e:
       logger.error(f"Error retrieving currencies: {e}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Error retrieving currencies"
       )

async def get_currency_by_code(db: Session, code: str) -> Currency:
   """
   Retrieve a specific currency by its code.
   
   Args:
       db: Database session
       code: Three-letter ISO currency code

   Returns:
       Currency: Currency object if found

   Raises:
       HTTPException: If currency not found
   """
   try:
       currency = db.query(Currency).filter(Currency.code == code.upper()).first()
       if not currency:
           logger.warning(f"Currency with code {code} not found")
           raise HTTPException(
               status_code=status.HTTP_404_NOT_FOUND,
               detail=f"Currency with code {code} not found"
           )
       return currency
   except HTTPException:
       raise
   except Exception as e:
       logger.error(f"Error retrieving currency {code}: {e}")
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail="Error retrieving currency"
       )