"""Pydantic models for Rules"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class Rule(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="forbid",
    )

    id: int
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=10)
    globs: list[str] = Field(default_factory=list)
    always_apply: bool = False
    created_at: datetime
    updated_at: datetime | None = None


class RuleCreate(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=10)
    globs: list[str] = Field(default_factory=list)
    always_apply: bool = False


class RuleUpdate(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    name: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = Field(None, min_length=10)
    globs: list[str] | None = None
    always_apply: bool | None = None
