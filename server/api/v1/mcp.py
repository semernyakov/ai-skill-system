"""MCP Gateway API endpoints"""

from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session

from server.models.mcp import MCPService, ServiceStartRequest, ServiceStatus, ServiceStopRequest
from server.core.database import get_session
from server.core.auth import get_current_user, require_role
from server.core.redis_client import redis_set_json, redis_get_json
from server.db.models import User, UserRole

router = APIRouter(prefix="/api/v1/mcp", tags=["mcp"])

# Default services configuration
DEFAULT_SERVICES = [
    MCPService(
        name="filesystem",
        status=ServiceStatus.STOPPED,
        host="localhost",
        port=8081,
    ),
    MCPService(
        name="git",
        status=ServiceStatus.STOPPED,
        host="localhost",
        port=8082,
    ),
    MCPService(
        name="github",
        status=ServiceStatus.STOPPED,
        host="localhost",
        port=8083,
    ),
]


async def get_services() -> dict[str, MCPService]:
    """Get services from Redis or initialize defaults"""
    services_dict = await redis_get_json("mcp_services")
    if services_dict:
        return {k: MCPService(**v) for k, v in services_dict.items()}
    
    # Initialize with defaults
    services_dict = {s.name: s for s in DEFAULT_SERVICES}
    await redis_set_json("mcp_services", {k: v.model_dump() for k, v in services_dict.items()})
    return services_dict


async def save_services(services: dict[str, MCPService]):
    """Save services to Redis"""
    services_dict = {k: v.model_dump() for k, v in services.items()}
    await redis_set_json("mcp_services", services_dict)


@router.get("/services", response_model=list[MCPService])
async def list_services(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    services = await get_services()
    return list(services.values())


@router.get("/services/{service_name}", response_model=MCPService)
async def get_service(
    service_name: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    services = await get_services()
    if service_name not in services:
        raise HTTPException(status_code=404, detail="Service not found")
    return services[service_name]


@router.post("/services/start")
async def start_service(
    request: ServiceStartRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_role(UserRole.EDITOR))
):
    services = await get_services()
    if request.service_name not in services:
        raise HTTPException(status_code=404, detail="Service not found")
    services[request.service_name].status = ServiceStatus.RUNNING
    await save_services(services)
    return {"message": f"Service {request.service_name} started"}


@router.post("/services/stop")
async def stop_service(
    request: ServiceStopRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_role(UserRole.EDITOR))
):
    services = await get_services()
    if request.service_name not in services:
        raise HTTPException(status_code=404, detail="Service not found")
    services[request.service_name].status = ServiceStatus.STOPPED
    await save_services(services)
    return {"message": f"Service {request.service_name} stopped"}


@router.get("/health")
async def check_all_services_health(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    services = await get_services()
    health_data = {}
    for service_name, service in services.items():
        health_data[service_name] = {
            "healthy": service.status == ServiceStatus.RUNNING,
            "uptime": "N/A",
            "last_check": "N/A"
        }
    return health_data


@router.get("/services/{service_name}/health")
async def check_service_health(
    service_name: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    services = await get_services()
    if service_name not in services:
        raise HTTPException(status_code=404, detail="Service not found")
    return {"service": service_name, "status": services[service_name].status, "healthy": services[service_name].status == ServiceStatus.RUNNING}
