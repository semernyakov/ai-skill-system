"""IDE Synchronization API endpoints"""

from datetime import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/sync", tags=["sync"])


class SyncRequest(BaseModel):
    force_all: bool = False
    targets: list[str] = []  # "cursor", "windsurf", "idea"


class SyncStatus(BaseModel):
    status: str
    last_sync: datetime | None
    targets_synced: list[str]
    errors: list[str]


sync_status = SyncStatus(
    status="idle",
    last_sync=None,
    targets_synced=[],
    errors=[]
)


@router.post("", response_model=SyncStatus)
async def trigger_sync(request: SyncRequest):
    """Trigger IDE synchronization"""
    global sync_status
    
    sync_status.status = "syncing"
    sync_status.last_sync = datetime.now()
    sync_status.targets_synced = request.targets if request.targets else ["cursor", "windsurf"]
    sync_status.errors = []
    
    # Simulate sync process
    if request.force_all:
        sync_status.targets_synced = ["cursor", "windsurf", "idea"]
    
    sync_status.status = "completed"
    return sync_status


@router.get("/status", response_model=SyncStatus)
async def get_sync_status():
    """Get current sync status"""
    return sync_status
