"""MCP Gateway API endpoints - commented out during stack simplification"""

# MCP Gateway endpoints commented out - removed during stack simplification
# To restore: uncomment this file and add router to main.py

# from fastapi import APIRouter, Depends, HTTPException
# from server.core.auth import get_current_user
# from server.db.models import User

# router = APIRouter(prefix="/api/v1/mcp", tags=["mcp"])

# @router.get("/services")
# async def list_services(
#     current_user: User = Depends(get_current_user)
# ):
#     """List available MCP services"""
#     return [
#         {"name": "filesystem", "status": "running", "description": "File operations"},
#         {"name": "git", "status": "stopped", "description": "Git operations"},
#         {"name": "github", "status": "stopped", "description": "GitHub API"},
#     ]

# @router.post("/services/start")
# async def start_service(
#     service_name: str,
#     current_user: User = Depends(get_current_user)
# ):
#     """Start an MCP service"""
#     return {"name": service_name, "status": "running"}

# @router.post("/services/stop")
# async def stop_service(
#     service_name: str,
#     current_user: User = Depends(get_current_user)
# ):
#     """Stop an MCP service"""
#     return {"name": service_name, "status": "stopped"}
