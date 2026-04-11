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

router = APIRouter(prefix="/api/v1/skills", tags=["skills"])

@router.get("", response_model=List[Skill])
async def list_skills(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    skills = session.exec(select(SkillDB)).all()
    return skills


@router.post("", response_model=Skill, status_code=201)
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
    session.commit()
    session.refresh(new_skill)
    return new_skill


@router.get("/{skill_id}", response_model=Skill)
async def get_skill(
    skill_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    skill = session.get(SkillDB, skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill


@router.put("/{skill_id}", response_model=Skill)
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
    
    if skill_update.name is not None or skill_update.description is not None:
        skill.updated_at = datetime.now()
    
    session.add(skill)
    session.commit()
    session.refresh(skill)
    return skill


@router.delete("/{skill_id}", status_code=204)
async def delete_skill(
    skill_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_role(UserRole.EDITOR))
):
    skill = session.get(SkillDB, skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    session.delete(skill)
    session.commit()
    return
