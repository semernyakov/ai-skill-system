"""Authentication API endpoints"""

import re
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field, field_validator
from sqlmodel import Session

from server.core.config import settings
from server.core.database import get_session
from server.core.security import create_access_token, verify_password
from server.db.models import User

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

class LoginRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8, max_length=128)

    @field_validator('password')
    @classmethod
    def validate_password_complexity(cls, v: str) -> str:
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain at least one digit')
        return v


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user_role: str


@router.post("/login", response_model=TokenResponse)
async def login(
    login_data: LoginRequest,
    session: Session = Depends(get_session)
):
    """Login and get JWT token"""
    user = session.get(User, login_data.username)

    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_role": user.role
    }
