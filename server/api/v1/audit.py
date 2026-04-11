"""System Audit API endpoints"""

from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Literal
from enum import StrEnum
from sqlmodel import Session

from server.core.database import get_session
from server.core.auth import get_current_user, require_role
from server.core.redis_client import redis_set_json, redis_get_json, redis_list_append, redis_list_get_all
from server.db.models import User, UserRole

router = APIRouter(prefix="/api/v1/audit", tags=["audit"])


class Severity(StrEnum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class AuditType(StrEnum):
    SECURITY = "SECURITY"
    PERFORMANCE = "PERFORMANCE"
    ARCHITECTURE = "ARCHITECTURE"
    COMPLIANCE = "COMPLIANCE"


class AuditFinding(BaseModel):
    severity: Severity
    category: str
    message: str
    location: str
    recommendation: str


class AuditResult(BaseModel):
    id: int
    audit_type: AuditType
    status: str
    started_at: datetime
    completed_at: datetime
    findings: list[AuditFinding]
    summary: str


class AuditRequest(BaseModel):
    audit_type: AuditType
    target: str | None = None


@router.post("/run", response_model=AuditResult)
async def run_audit(
    request: AuditRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_role(UserRole.EDITOR))
):
    """Run system audit"""
    findings: list[AuditFinding] = []
    
    # Simulate audit findings based on type
    if request.audit_type == AuditType.SECURITY:
        findings = [
            AuditFinding(
                severity=Severity.HIGH,
                category="Security",
                message="API endpoint missing rate limiting",
                location="server/api/v1/rules.py",
                recommendation="Add rate limiting middleware"
            ),
            AuditFinding(
                severity=Severity.MEDIUM,
                category="Security",
                message="CORS configuration too permissive",
                location="server/main.py",
                recommendation="Restrict CORS origins"
            )
        ]
    elif request.audit_type == AuditType.PERFORMANCE:
        findings = [
            AuditFinding(
                severity=Severity.MEDIUM,
                category="Performance",
                message="Database query not optimized",
                location="server/api/v1/skills.py",
                recommendation="Add database index"
            )
        ]
    elif request.audit_type == AuditType.ARCHITECTURE:
        findings = [
            AuditFinding(
                severity=Severity.LOW,
                category="Architecture",
                message="Circular dependency detected",
                location="server/core/deps.py",
                recommendation="Refactor dependency injection"
            )
        ]
    elif request.audit_type == AuditType.COMPLIANCE:
        findings = [
            AuditFinding(
                severity=Severity.HIGH,
                category="Compliance",
                message="GDPR compliance issue: missing consent tracking",
                location="server/core/config.py",
                recommendation="Implement consent management"
            )
        ]
    
    result = AuditResult(
        id=0,  # Will be generated from Redis
        audit_type=request.audit_type,
        status="completed",
        started_at=datetime.now(),
        completed_at=datetime.now(),
        findings=findings,
        summary=f"{len(findings)} findings detected"
    )
    
    # Store in Redis
    result_dict = result.model_dump()
    await redis_list_append("audit_results", result_dict)
    result.id = len(await redis_list_get_all("audit_results"))
    
    return result


@router.get("/results", response_model=list[AuditResult])
async def get_audit_results(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get all audit results"""
    results = await redis_list_get_all("audit_results")
    return results


@router.get("/results/{audit_id}", response_model=AuditResult)
async def get_audit_result(
    audit_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get specific audit result"""
    results = await redis_list_get_all("audit_results")
    for result in results:
        if result["id"] == audit_id:
            return AuditResult(**result)
    raise HTTPException(status_code=404, detail="Audit result not found")
