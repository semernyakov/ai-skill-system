"""Logs API endpoints"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime
from typing import Literal
from sqlmodel import Session

from server.core.database import get_session
from server.core.auth import get_current_user, require_role
from server.core.redis_client import redis_list_append, redis_list_get_all
from server.db.models import User, UserRole

router = APIRouter(prefix="/api/v1/logs", tags=["logs"])


class LogEntry(BaseModel):
    timestamp: datetime
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR"]
    service: str
    message: str
    context: dict | None = None


class LogsRequest(BaseModel):
    service: str | None = None
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] | None = None
    limit: int = 100


# Default mock log data
DEFAULT_LOGS = [
    LogEntry(
        timestamp=datetime.now(),
        level="INFO",
        service="api",
        message="Server started on port 8000"
    ),
    LogEntry(
        timestamp=datetime.now(),
        level="INFO",
        service="api",
        message="API router registered: rules"
    ),
    LogEntry(
        timestamp=datetime.now(),
        level="WARNING",
        service="mcp",
        message="Service filesystem failed to start",
        context={"error": "Connection refused"}
    ),
    LogEntry(
        timestamp=datetime.now(),
        level="ERROR",
        service="database",
        message="Connection timeout",
        context={"timeout": 30}
    )
]


async def get_logs_from_redis() -> list[LogEntry]:
    """Get logs from Redis or initialize defaults"""
    logs_list = await redis_list_get_all("logs")
    if logs_list:
        return [LogEntry(**log) for log in logs_list]
    
    # Initialize with defaults
    for log in DEFAULT_LOGS:
        await redis_list_append("logs", log.model_dump())
    return DEFAULT_LOGS


@router.post("", response_model=list[LogEntry])
async def get_logs(
    request: LogsRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_role(UserRole.VIEWER))
):
    """Get logs with optional filtering"""
    logs = await get_logs_from_redis()
    filtered_logs = logs
    
    if request.service:
        filtered_logs = [log for log in filtered_logs if log.service == request.service]
    
    if request.level:
        filtered_logs = [log for log in filtered_logs if log.level == request.level]
    
    return filtered_logs[:request.limit]


@router.get("/stream")
async def stream_logs(
    session: Session = Depends(get_session),
    current_user: User = Depends(require_role(UserRole.VIEWER))
):
    """Stream logs in real-time (SSE endpoint)"""
    # This would typically use Server-Sent Events
    # For now, return the current logs
    logs = await get_logs_from_redis()
    return logs
