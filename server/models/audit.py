"""Pydantic models for System Audit"""

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class Severity(StrEnum):
    P0 = "P0"
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"


class AuditType(StrEnum):
    SECURITY = "security"
    PERFORMANCE = "performance"
    ARCHITECTURE = "architecture"
    COMPLIANCE = "compliance"


class Finding(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="forbid",
    )

    id: str
    type: AuditType
    severity: Severity
    category: str
    title: str
    file: str | None = None
    line: int | None = None
    description: str
    recommendation: str


class AuditResult(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="forbid",
    )

    audit_timestamp: datetime
    audit_version: str
    project_root: str
    duration_seconds: float
    findings: list[Finding]
    summary: dict[str, int]
