from datetime import datetime
from typing import Optional, Tuple
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.auth import LoginRequest
from app.utils.auth import (
    pwd_context,
    create_access_token,
    create_refresh_token
)

class AuthenticationError(Exception):
    """Custom exception for authentication errors."""
    pass

class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash."""
        return pwd_context.verify(plain_password, hashed_password)

    def _get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return self.db.query(User).filter(User.email == email).first()

    def _create_tokens(self, user_id: int, email: str) -> Tuple[str, str]:
        """Create access and refresh tokens."""
        token_data = {"sub": str(user_id), "email": email}
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)
        return access_token, refresh_token

    async def authenticate_user(self, login_data: LoginRequest) -> Tuple[User, str, str]:
        """Authenticate user and return tokens."""
        user = self._get_user_by_email(login_data.email)
        
        if not user:
            raise AuthenticationError("Invalid email or password")
            
        if not self._verify_password(login_data.password, user.password):
            raise AuthenticationError("Invalid email or password")

        # Create tokens
        access_token, refresh_token = self._create_tokens(
            user.id,
            user.email
        )

        # Update last login
        user.last_login = datetime.utcnow()
        self.db.commit()

        return user, access_token, refresh_token

    async def refresh_tokens(self, user_id: int, email: str) -> Tuple[str, str]:
        """Create new access and refresh tokens."""
        return self._create_tokens(user_id, email)