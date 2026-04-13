"""Skills API endpoints with SQLModel and authentication"""


from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from server.core.auth import get_current_user, get_current_user_required, require_role
from server.core.database import get_session
from server.core.deps import get_skill_runner, get_skill_service, get_sync_service
from server.db.models import User, UserRole
from server.models.skill import Skill, SkillCreate, SkillUpdate

router = APIRouter(prefix="/api/v1/skills", tags=["skills"])

@router.get("", response_model=list[Skill])
async def list_skills(
    page: int = 1,
    limit: int = 50,
    session: Session = Depends(get_session),
    current_user: User | None = Depends(get_current_user),
    skill_service = Depends(get_skill_service)
):
    skills = await skill_service.list_skills()
    offset = (page - 1) * limit
    return skills[offset:offset + limit]


@router.post("", response_model=Skill, status_code=201)
async def create_skill(
    skill: SkillCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_role(UserRole.EDITOR)),
    skill_service = Depends(get_skill_service)
):
    new_skill = await skill_service.create_skill(skill)
    return new_skill


@router.get("/{skill_id}", response_model=Skill)
async def get_skill(
    skill_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user_required),
    skill_service = Depends(get_skill_service)
):
    skill = await skill_service.get_skill(skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill


@router.put("/{skill_id}", response_model=Skill)
async def update_skill(
    skill_id: int,
    skill_update: SkillUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_role(UserRole.EDITOR)),
    skill_service = Depends(get_skill_service)
):
    skill = await skill_service.update_skill(skill_id, skill_update)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill


@router.delete("/{skill_id}", status_code=204)
async def delete_skill(
    skill_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_role(UserRole.EDITOR)),
    skill_service = Depends(get_skill_service)
):
    deleted = await skill_service.delete_skill(skill_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Skill not found")
    return


@router.post("/{skill_id}/execute")
async def execute_skill(
    skill_id: int,
    input_data: dict,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user_required),
    skill_runner = Depends(get_skill_runner)
):
    """Execute skill with given input"""
    result = await skill_runner.execute(skill_id, input_data)
    return result


@router.post("/sync/run")
async def sync_skills(
    session: Session = Depends(get_session),
    current_user: User = Depends(require_role(UserRole.EDITOR)),
    sync_service = Depends(get_sync_service)
):
    """Sync skills from external agentskills repository"""
    result = await sync_service.run_sync()
    return result
