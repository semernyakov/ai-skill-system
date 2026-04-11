"""IDE Synchronization API endpoints"""

from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlmodel import Session

from server.core.database import get_session
from server.core.auth import get_current_user, require_role
from server.core.redis_client import redis_set_json, redis_get_json
from server.db.models import User, UserRole

router = APIRouter(prefix="/api/v1/sync", tags=["sync"])


class SyncRequest(BaseModel):
    force_all: bool = False
    targets: list[str] = []  # "cursor", "windsurf", "idea"


class SyncStatus(BaseModel):
    status: str
    last_sync: datetime | None
    targets_synced: list[str]
    errors: list[str]


@router.post("", response_model=SyncStatus)
async def trigger_sync(
    request: SyncRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_role(UserRole.EDITOR))
):
    """Trigger IDE synchronization"""
    sync_status = SyncStatus(
        status="syncing",
        last_sync=datetime.now(),
        targets_synced=request.targets if request.targets else ["cursor", "windsurf"],
        errors=[]
    )
    
    # Simulate sync process
    if request.force_all:
        sync_status.targets_synced = ["cursor", "windsurf", "idea"]
    
    sync_status.status = "completed"
    
    # Store in Redis
    await redis_set_json("sync_status", sync_status.model_dump())
    
    return sync_status


@router.get("/status", response_model=SyncStatus)
async def get_sync_status(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get current sync status"""
    status_dict = await redis_get_json("sync_status")
    if status_dict:
        return SyncStatus(**status_dict)
    return SyncStatus(
        status="idle",
        last_sync=None,
        targets_synced=[],
        errors=[]
    )
