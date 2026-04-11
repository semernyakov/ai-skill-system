"""Skills API endpoints"""

from datetime import datetime
from fastapi import APIRouter, HTTPException
from server.models.skill import Skill, SkillCreate, SkillUpdate

router = APIRouter(prefix="/api/v1/skills", tags=["skills"])

skills_db: list[Skill] = []


@router.get("", response_model=list[Skill])
async def list_skills():
    return skills_db


@router.post("", response_model=Skill, status_code=201)
async def create_skill(skill: SkillCreate):
    new_skill = Skill(
        id=len(skills_db) + 1,
        name=skill.name,
        description=skill.description,
        created_at=datetime.now(),
    )
    skills_db.append(new_skill)
    return new_skill


@router.get("/{skill_id}", response_model=Skill)
async def get_skill(skill_id: int):
    for skill in skills_db:
        if skill.id == skill_id:
            return skill
    raise HTTPException(status_code=404, detail="Skill not found")


@router.put("/{skill_id}", response_model=Skill)
async def update_skill(skill_id: int, skill_update: SkillUpdate):
    for skill in skills_db:
        if skill.id == skill_id:
            if skill_update.name is not None:
                skill.name = skill_update.name
            if skill_update.description is not None:
                skill.description = skill_update.description
            skill.updated_at = datetime.now()
            return skill
    raise HTTPException(status_code=404, detail="Skill not found")


@router.delete("/{skill_id}", status_code=204)
async def delete_skill(skill_id: int):
    for i, skill in enumerate(skills_db):
        if skill.id == skill_id:
            skills_db.pop(i)
            return
    raise HTTPException(status_code=404, detail="Skill not found")
