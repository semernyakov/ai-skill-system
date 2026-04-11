"""Rules API endpoints with SQLModel and authentication"""

from datetime import datetime
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
import json

from server.models.rule import Rule, RuleCreate, RuleUpdate
from server.db.models import Rule as RuleDB
from server.core.database import get_session
from server.core.auth import get_current_user, require_role
from server.db.models import User, UserRole
from server.core.rate_limit import get_read_rate_limiter, get_write_rate_limiter

router = APIRouter(prefix="/api/v1/rules", tags=["rules"])


@router.get("", response_model=List[Rule], dependencies=[Depends(get_read_rate_limiter)])
async def list_rules(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    rules = session.exec(select(RuleDB)).all()
    result = []
    for r in rules:
        try:
            globs = json.loads(r.globs) if r.globs else []
        except json.JSONDecodeError:
            globs = []
        result.append(
            Rule(
                id=r.id,
                name=r.name,
                description=r.description,
                globs=globs,
                always_apply=r.always_apply,
                created_at=r.created_at,
                updated_at=r.updated_at
            )
        )
    return result


@router.post("", response_model=Rule, status_code=201, dependencies=[Depends(get_write_rate_limiter)])
async def create_rule(
    rule: RuleCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_role(UserRole.EDITOR))
):
    new_rule = RuleDB(
        name=rule.name,
        description=rule.description,
        globs=json.dumps(rule.globs),
        always_apply=rule.always_apply,
        created_at=datetime.now(),
    )
    session.add(new_rule)
    try:
        session.commit()
        session.refresh(new_rule)
    except Exception:
        session.rollback()
        raise
    return Rule(
        id=new_rule.id,
        name=new_rule.name,
        description=new_rule.description,
        globs=rule.globs,
        always_apply=new_rule.always_apply,
        created_at=new_rule.created_at,
        updated_at=new_rule.updated_at
    )


@router.get("/{rule_id}", response_model=Rule, dependencies=[Depends(get_read_rate_limiter)])
async def get_rule(
    rule_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    rule = session.get(RuleDB, rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    try:
        globs = json.loads(rule.globs) if rule.globs else []
    except json.JSONDecodeError:
        globs = []
    return Rule(
        id=rule.id,
        name=rule.name,
        description=rule.description,
        globs=globs,
        always_apply=rule.always_apply,
        created_at=rule.created_at,
        updated_at=rule.updated_at
    )


@router.put("/{rule_id}", response_model=Rule, dependencies=[Depends(get_write_rate_limiter)])
async def update_rule(
    rule_id: int,
    rule_update: RuleUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_role(UserRole.EDITOR))
):
    rule = session.get(RuleDB, rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    
    rule_data = rule_update.model_dump(exclude_unset=True)
    for key, value in rule_data.items():
        if key == 'globs' and value is not None:
            setattr(rule, key, json.dumps(value))
        else:
            setattr(rule, key, value)
    
    if rule_data:
        rule.updated_at = datetime.now()
    
    try:
        session.add(rule)
        session.commit()
        session.refresh(rule)
    except Exception:
        session.rollback()
        raise
    try:
        globs = json.loads(rule.globs) if rule.globs else []
    except json.JSONDecodeError:
        globs = []
    return Rule(
        id=rule.id,
        name=rule.name,
        description=rule.description,
        globs=globs,
        always_apply=rule.always_apply,
        created_at=rule.created_at,
        updated_at=rule.updated_at
    )


@router.delete("/{rule_id}", status_code=204, dependencies=[Depends(get_write_rate_limiter)])
async def delete_rule(
    rule_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_role(UserRole.EDITOR))
):
    rule = session.get(RuleDB, rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    session.delete(rule)
    try:
        session.commit()
    except Exception:
        session.rollback()
        raise
    return
