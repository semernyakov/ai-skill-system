"""MCP Gateway API endpoints"""

from fastapi import APIRouter, HTTPException

from server.models.mcp import MCPService, ServiceStartRequest, ServiceStatus, ServiceStopRequest

router = APIRouter(prefix="/api/v1/mcp", tags=["mcp"])

services_db: dict[str, MCPService] = {
    "filesystem": MCPService(
        name="filesystem",
        status=ServiceStatus.STOPPED,
        host="localhost",
        port=8081,
    ),
    "git": MCPService(
        name="git",
        status=ServiceStatus.STOPPED,
        host="localhost",
        port=8082,
    ),
    "github": MCPService(
        name="github",
        status=ServiceStatus.STOPPED,
        host="localhost",
        port=8083,
    ),
}


@router.get("/services", response_model=list[MCPService])
async def list_services():
    return list(services_db.values())


@router.get("/services/{service_name}", response_model=MCPService)
async def get_service(service_name: str):
    if service_name not in services_db:
        raise HTTPException(status_code=404, detail="Service not found")
    return services_db[service_name]


@router.post("/services/start")
async def start_service(request: ServiceStartRequest):
    if request.service_name not in services_db:
        raise HTTPException(status_code=404, detail="Service not found")
    services_db[request.service_name].status = ServiceStatus.RUNNING
    return {"message": f"Service {request.service_name} started"}


@router.post("/services/stop")
async def stop_service(request: ServiceStopRequest):
    if request.service_name not in services_db:
        raise HTTPException(status_code=404, detail="Service not found")
    services_db[request.service_name].status = ServiceStatus.STOPPED
    return {"message": f"Service {request.service_name} stopped"}


@router.get("/services/{service_name}/health")
async def check_service_health(service_name: str):
    if service_name not in services_db:
        raise HTTPException(status_code=404, detail="Service not found")
    return {"service": service_name, "status": services_db[service_name].status}
