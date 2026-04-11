"""Skill Pydantic models with validation"""

from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, field_validator


class Skill(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid'
    )

    id: int
    name: str = Field(..., min_length=1, max_length=100, pattern=r'^[a-zA-Z0-9_-]+$')
    description: str = Field(..., min_length=10, max_length=5000)
    created_at: datetime
    updated_at: datetime | None = None


class SkillCreate(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    name: str = Field(..., min_length=1, max_length=100, pattern=r'^[a-zA-Z0-9_-]+$')
    description: str = Field(..., min_length=10, max_length=5000)

    @field_validator('description')
    @classmethod
    def validate_no_sql_injection(cls, v: str) -> str:
        sql_keywords = ['DROP', 'DELETE', 'UNION', 'INSERT', 'UPDATE', 'ALTER', 'TRUNCATE', 'EXEC', 'EXECUTE']
        upper_v = v.upper()
        for keyword in sql_keywords:
            if keyword in upper_v:
                raise ValueError(f"SQL keyword '{keyword}' not allowed in description")
        return v


class SkillUpdate(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    name: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = Field(None, min_length=10)
