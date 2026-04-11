"""Skills API endpoints with SQLModel and authentication"""

from datetime import datetime
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select

from server.models.skill import Skill, SkillCreate, SkillUpdate
from server.db.models import Skill as SkillDB
from server.core.database import get_session
from server.core.auth import get_current_user, require_role
from server.db.models import User, UserRole
from server.core.rate_limit import get_read_rate_limiter, get_write_rate_limiter

router = APIRouter(prefix="/api/v1/skills", tags=["skills"])

@router.get("", response_model=List[Skill], dependencies=[Depends(get_read_rate_limiter)])
async def list_skills(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    skills = session.exec(select(SkillDB)).all()
    return skills


@router.post("", response_model=Skill, status_code=201, dependencies=[Depends(get_write_rate_limiter)])
async def create_skill(
    skill: SkillCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_role(UserRole.EDITOR))
):
    new_skill = SkillDB(
        name=skill.name,
        description=skill.description,
        created_at=datetime.now(),
    )
    session.add(new_skill)
    try:
        session.commit()
        session.refresh(new_skill)
    except Exception:
        session.rollback()
        raise
    return new_skill


@router.get("/{skill_id}", response_model=Skill, dependencies=[Depends(get_read_rate_limiter)])
async def get_skill(
    skill_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    skill = session.get(SkillDB, skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill


@router.put("/{skill_id}", response_model=Skill, dependencies=[Depends(get_write_rate_limiter)])
async def update_skill(
    skill_id: int,
    skill_update: SkillUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_role(UserRole.EDITOR))
):
    skill = session.get(SkillDB, skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    skill_data = skill_update.model_dump(exclude_unset=True)
    for key, value in skill_data.items():
        setattr(skill, key, value)
    
    if skill_data:
        skill.updated_at = datetime.now()
    
    session.add(skill)
    try:
        session.commit()
        session.refresh(skill)
    except Exception:
        session.rollback()
        raise
    return skill


@router.delete("/{skill_id}", status_code=204, dependencies=[Depends(get_write_rate_limiter)])
async def delete_skill(
    skill_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_role(UserRole.EDITOR))
):
    skill = session.get(SkillDB, skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    session.delete(skill)
    try:
        session.commit()
    except Exception:
        session.rollback()
        raise
    return
