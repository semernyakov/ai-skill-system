"""Pydantic models for MCP Gateway"""

from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class ServiceStatus(StrEnum):
    RUNNING = "running"
    STOPPED = "stopped"
    ERROR = "error"


class MCPService(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="forbid",
    )

    name: str
    status: ServiceStatus
    host: str
    port: int


class ServiceStartRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    service_name: str


class ServiceStopRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    service_name: str
