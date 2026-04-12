"""Skill Pydantic models with validation"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class Skill(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid'
    )

    id: int
    name: str = Field(..., min_length=1, max_length=100, pattern=r'^[a-zA-Z0-9_-]+$')
    description: str = Field(..., min_length=10, max_length=5000)
    config: dict = Field(default_factory=dict)
    source: str = Field(default="internal", max_length=50)
    version: str | None = Field(None, max_length=20)
    active: bool = Field(default=True)
    created_at: datetime
    updated_at: datetime | None = None


class SkillCreate(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    name: str = Field(..., min_length=1, max_length=100, pattern=r'^[a-zA-Z0-9_-]+$')
    description: str = Field(..., min_length=10, max_length=5000)
    config: dict = Field(default_factory=dict)
    source: str = Field(default="internal", max_length=50)
    version: str | None = Field(None, max_length=20)
    active: bool = Field(default=True)


class SkillUpdate(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    name: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = Field(None, min_length=10)
    config: dict | None = None
    source: str | None = Field(None, max_length=50)
    version: str | None = Field(None, max_length=20)
    active: bool | None = None
