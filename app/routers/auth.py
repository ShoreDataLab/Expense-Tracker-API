from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.database import get_db
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    RefreshTokenRequest,
    TokenData
)
from app.services.auth import AuthService, AuthenticationError
from app.utils.auth import verify_refresh_token

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/login", response_model=LoginResponse)
async def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
) -> LoginResponse:
    """Login user and return tokens."""
    try:
        auth_service = AuthService(db)
        user, access_token, refresh_token = await auth_service.authenticate_user(
            login_data
        )
        
        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user_id=user.id,
            email=user.email,
            username=user.username
        )
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

@router.post("/refresh", response_model=TokenData)
async def refresh_token(
    refresh_request: RefreshTokenRequest,
    db: Session = Depends(get_db)
) -> TokenData:
    """Refresh access token using refresh token."""
    # Verify refresh token
    payload = verify_refresh_token(refresh_request.refresh_token)
    
    # Create new tokens
    auth_service = AuthService(db)
    access_token, refresh_token = await auth_service.refresh_tokens(
        int(payload["sub"]),
        payload["email"]
    )
    
    return TokenData(
        access_token=access_token,
        refresh_token=refresh_token
    )