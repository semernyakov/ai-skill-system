"""Pydantic models for Skills"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class Skill(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="forbid",
    )

    id: int
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=10)
    created_at: datetime
    updated_at: datetime | None = None


class SkillCreate(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=10)


class SkillUpdate(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    name: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = Field(None, min_length=10)
