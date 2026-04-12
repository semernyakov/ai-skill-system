"""Logs API endpoints"""

from datetime import datetime
from typing import Literal

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session

from server.core.auth import require_role
from server.core.database import get_session
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


@router.get("", response_model=list[LogEntry])
async def get_logs(
    service: str | None = None,
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] | None = None,
    limit: int = 100,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_role(UserRole.VIEWER))
):
    """Get logs from database with optional filtering"""
    from sqlmodel import select

    from server.db.models import LogEntry as DBLogEntry

    query = select(DBLogEntry)

    if service:
        query = query.where(DBLogEntry.service == service)
    if level:
        query = query.where(DBLogEntry.level == level)

    query = query.order_by(DBLogEntry.timestamp.desc()).limit(limit)

    results = session.exec(query).all()

    return [
        LogEntry(
            timestamp=log.timestamp,
            level=log.level,
            service=log.service or "",
            message=log.message,
            context=None
        )
        for log in results
    ]


@router.get("/stream")
async def stream_logs(
    session: Session = Depends(get_session),
    current_user: User = Depends(require_role(UserRole.VIEWER))
):
    """Stream logs in real-time (SSE endpoint)"""
    # This would typically use Server-Sent Events
    # For now, return the current logs
    from sqlmodel import select

    from server.db.models import LogEntry as DBLogEntry

    query = select(DBLogEntry).order_by(DBLogEntry.timestamp.desc()).limit(100)
    results = session.exec(query).all()

    return [
        LogEntry(
            timestamp=log.timestamp,
            level=log.level,
            service=log.service or "",
            message=log.message,
            context=None
        )
        for log in results
    ]
