#!/usr/bin/env python3
"""
MCP Gateway Server

Central entry point for all MCP service requests.
Routes requests to appropriate service adapters.
"""
import json
import os
from pathlib import Path
from typing import Any, Dict
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import uvicorn

from .services import MCPServiceAdapter
from .services.filesystem import FilesystemAdapter
from .services.git import GitAdapter
from .services.github import GitHubAdapter


# Load configuration
CONFIG_PATH = Path(__file__).parent / "config.json"


def load_config() -> Dict[str, Any]:
    """Load gateway configuration."""
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH) as f:
            return json.load(f)
    return {
        "gateway": {"host": "localhost", "port": 8080, "log_level": "info"},
        "services": {}
    }


# Initialize services
services: Dict[str, MCPServiceAdapter] = {}


def initialize_services(config: Dict[str, Any]):
    """Initialize service adapters from configuration."""
    services_config = config.get("services", {})
    
    # Filesystem service
    if "filesystem" in services_config:
        fs_config = services_config["filesystem"]
        if fs_config.get("enabled", True):
            services["filesystem"] = FilesystemAdapter(fs_config.get("config", {}))
    
    # Git service
    if "git" in services_config:
        git_config = services_config["git"]
        if git_config.get("enabled", True):
            services["git"] = GitAdapter(git_config.get("config", {}))
    
    # GitHub service
    if "github" in services_config:
        github_config = services_config["github"]
        if github_config.get("enabled", True):
            services["github"] = GitHubAdapter(github_config.get("config", {}))


# Create FastAPI app
app = FastAPI(title="MCP Gateway", version="1.0.0")


@app.get("/")
async def root():
    """Root endpoint."""
    return {"name": "MCP Gateway", "version": "1.0.0"}


@app.get("/mcp/services")
async def list_services():
    """List available MCP services."""
    return {
        "services": list(services.keys()),
        "count": len(services)
    }


@app.get("/mcp/health/{service_name}")
async def check_service_health(service_name: str):
    """Check service health."""
    if service_name not in services:
        raise HTTPException(status_code=404, detail="Service not found")
    
    healthy = await services[service_name].health()
    return {"service": service_name, "healthy": healthy}


@app.post("/mcp/{service_name}/invoke")
async def invoke_service(service_name: str, request: Dict[str, Any]):
    """Invoke MCP service method."""
    if service_name not in services:
        raise HTTPException(status_code=404, detail="Service not found")
    
    method = request.get("method")
    params = request.get("params", {})
    
    if not method:
        raise HTTPException(status_code=400, detail="Method is required")
    
    result = await services[service_name].invoke(method, params)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@app.get("/mcp/{service_name}/capabilities")
async def get_service_capabilities(service_name: str):
    """Get service capabilities."""
    if service_name not in services:
        raise HTTPException(status_code=404, detail="Service not found")
    
    return await services[service_name].capabilities()


def main():
    """Run the MCP gateway server."""
    config = load_config()
    gateway_config = config.get("gateway", {})
    
    host = gateway_config.get("host", "localhost")
    port = gateway_config.get("port", 8080)
    log_level = gateway_config.get("log_level", "info")
    
    # Initialize services
    initialize_services(config)
    
    print(f"Starting MCP Gateway on {host}:{port}")
    print(f"Available services: {list(services.keys())}")
    
    uvicorn.run(app, host=host, port=port, log_level=log_level)


if __name__ == "__main__":
    main()
