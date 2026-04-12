"""Rule Pydantic models with validation"""

import json
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Rule(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid'
    )

    id: int
    name: str = Field(..., min_length=1, max_length=100, pattern=r'^[a-zA-Z0-9_-]+$')
    description: str = Field(..., min_length=10, max_length=5000)
    globs: list[str] = Field(default_factory=list)
    always_apply: bool = False
    created_at: datetime
    updated_at: datetime | None = None

    @field_validator('globs', mode='before')
    @classmethod
    def parse_globs(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return []
        return v


class RuleCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, pattern=r'^[a-zA-Z0-9_-]+$')
    description: str = Field(..., min_length=10, max_length=5000)
    globs: list[str] = Field(default_factory=list)
    always_apply: bool = False


class RuleUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100, pattern=r'^[a-zA-Z0-9_-]+$')
    description: str | None = Field(None, min_length=10, max_length=5000)
    globs: list[str] | None = None
    always_apply: bool | None = None
