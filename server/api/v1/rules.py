"""Rules API endpoints with SQLModel and authentication"""

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from server.core.auth import get_current_user, require_role
from server.core.database import get_session
from server.core.deps import get_rule_service
from server.db.models import User, UserRole
from server.models.rule import Rule, RuleCreate, RuleUpdate

router = APIRouter(prefix="/api/v1/rules", tags=["rules"])


@router.get("", response_model=list[Rule])
async def list_rules(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    rule_service = Depends(get_rule_service)
):
    rules = await rule_service.list_rules()
    return rules


@router.post("", response_model=Rule, status_code=201)
async def create_rule(
    rule: RuleCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_role(UserRole.EDITOR)),
    rule_service = Depends(get_rule_service)
):
    new_rule = await rule_service.create_rule(rule)
    return new_rule


@router.get("/{rule_id}", response_model=Rule)
async def get_rule(
    rule_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    rule_service = Depends(get_rule_service)
):
    rule = await rule_service.get_rule(rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    return rule


@router.put("/{rule_id}", response_model=Rule)
async def update_rule(
    rule_id: int,
    rule_update: RuleUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_role(UserRole.EDITOR)),
    rule_service = Depends(get_rule_service)
):
    rule = await rule_service.update_rule(rule_id, rule_update)
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    return rule


@router.delete("/{rule_id}", status_code=204)
async def delete_rule(
    rule_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_role(UserRole.EDITOR)),
    rule_service = Depends(get_rule_service)
):
    deleted = await rule_service.delete_rule(rule_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Rule not found")
    return
