"""Authentication dependencies for FastAPI"""



from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import Session

from server.core.database import get_session
from server.core.security import decode_token
from server.db.models import User, UserRole

security = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    session: Session = Depends(get_session)
) -> User | None:
    """Get current user from JWT token (optional)"""
    if credentials is None:
        return None

    token = credentials.credentials
    payload = decode_token(token)

    if payload is None:
        return None

    username: str = payload.get("sub")
    if username is None:
        return None

    user = session.get(User, username)
    if user is None:
        return None

    return user


async def get_current_user_required(
    current_user: User | None = Depends(get_current_user)
) -> User:
    """Get current user from JWT token (required)"""
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user


def require_role(required_role: UserRole):
    """Require specific role to access endpoint"""
    async def role_checker(current_user: User = Depends(get_current_user_required)) -> User:
        role_hierarchy = {
            UserRole.ADMIN: 3,
            UserRole.EDITOR: 2,
            UserRole.VIEWER: 1
        }

        if role_hierarchy[current_user.role] < role_hierarchy[required_role]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    return role_checker
