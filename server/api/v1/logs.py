"""Logs API endpoints"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import Literal

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


# Mock log data
mock_logs: list[LogEntry] = [
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


@router.post("", response_model=list[LogEntry])
async def get_logs(request: LogsRequest):
    """Get logs with optional filtering"""
    filtered_logs = mock_logs
    
    if request.service:
        filtered_logs = [log for log in filtered_logs if log.service == request.service]
    
    if request.level:
        filtered_logs = [log for log in filtered_logs if log.level == request.level]
    
    return filtered_logs[:request.limit]


@router.get("/stream")
async def stream_logs():
    """Stream logs in real-time (SSE endpoint)"""
    # This would typically use Server-Sent Events
    # For now, return the current logs
    return mock_logs
