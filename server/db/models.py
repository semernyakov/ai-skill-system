"""SQLModel database models"""

from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel
from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"


class User(SQLModel, table=True):
    username: str = Field(default=None, primary_key=True, max_length=50)
    hashed_password: str = Field(max_length=255)
    role: UserRole = Field(default=UserRole.VIEWER)
    created_at: datetime = Field(default_factory=datetime.now)


class Rule(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=100)
    description: str = Field(max_length=5000)
    globs: str = Field(default="[]")  # JSON string
    always_apply: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default=None)

    @property
    def globs_list(self) -> list:
        import json
        try:
            return json.loads(self.globs)
        except json.JSONDecodeError:
            return []


class Skill(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=100)
    description: str = Field(max_length=5000)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default=None)


class Severity(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class AuditType(str, Enum):
    SECURITY = "SECURITY"
    PERFORMANCE = "PERFORMANCE"
    ARCHITECTURE = "ARCHITECTURE"
    COMPLIANCE = "COMPLIANCE"


class AuditResult(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    audit_type: AuditType
    status: str = Field(default="completed")
    started_at: datetime
    completed_at: datetime
    findings: str = Field(default="[]")  # JSON string
    summary: str = Field(max_length=500)


class LogEntry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.now, index=True)
    level: str = Field(index=True, max_length=10)
    service: Optional[str] = Field(default=None, max_length=50, index=True)
    message: str = Field(max_length=10000)
