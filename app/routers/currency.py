from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging

from app.schemas.currency import CurrencyCreate, CurrencyResponse
from app.services.currency import create_currency, get_all_currencies, get_currency_by_code
from app.database import get_db

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/currencies",
    tags=["currencies"],
    responses={
        400: {"description": "Bad Request - Currency already exists"},
        404: {"description": "Currency not found"},
        500: {"description": "Internal Server Error"}
    }
)

@router.post(
    "/", 
    response_model=CurrencyResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new currency",
    description="Add a new currency to the system with code, name, and symbol"
)
async def create_currency_endpoint(
    currency_data: CurrencyCreate,
    db: Session = Depends(get_db)
) -> CurrencyResponse:
    """
    Create a new currency with the following information:

    - **code**: Three-letter ISO currency code (e.g., USD, EUR, GBP)
    - **name**: Full name of the currency (e.g., US Dollar)
    - **symbol**: Currency symbol (e.g., $, €, £)
    """
    try:
        logger.info(f"Creating new currency: {currency_data.code}")
        return await create_currency(db, currency_data)
    except Exception as e:
        logger.error(f"Error in create_currency endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating the currency"
        ) from e

@router.get(
    "/",
    response_model=list[CurrencyResponse],
    summary="Get all currencies",
    description="Retrieve a list of all available currencies"
)
async def get_currencies(
    db: Session = Depends(get_db)
) -> list[CurrencyResponse]:
    """Retrieve all currencies from the database."""
    try:
        return await get_all_currencies(db)
    except Exception as e:
        logger.error(f"Error retrieving currencies: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while retrieving currencies"
        ) from e

@router.get(
    "/{code}",
    response_model=CurrencyResponse,
    summary="Get currency by code",
    description="Retrieve a specific currency by its ISO code"
)
async def get_currency(
    code: str,
    db: Session = Depends(get_db)
) -> CurrencyResponse:
    """
    Retrieve a specific currency by its code.
    
    - **code**: Three-letter ISO currency code (e.g., USD, EUR, GBP)
    """
    try:
        currency = await get_currency_by_code(db, code.upper())
        if not currency:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Currency with code {code} not found"
            )
        return currency
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving currency {code}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while retrieving the currency"
        ) from e