"""Rules API endpoints"""

from datetime import datetime

from fastapi import APIRouter, HTTPException

from server.models.rule import Rule, RuleCreate, RuleUpdate

router = APIRouter(prefix="/api/v1/rules", tags=["rules"])

rules_db: list[Rule] = []


@router.get("", response_model=list[Rule])
async def list_rules():
    return rules_db


@router.post("", response_model=Rule, status_code=201)
async def create_rule(rule: RuleCreate):
    new_rule = Rule(
        id=len(rules_db) + 1,
        name=rule.name,
        description=rule.description,
        globs=rule.globs,
        always_apply=rule.always_apply,
        created_at=datetime.now(),
    )
    rules_db.append(new_rule)
    return new_rule


@router.get("/{rule_id}", response_model=Rule)
async def get_rule(rule_id: int):
    for rule in rules_db:
        if rule.id == rule_id:
            return rule
    raise HTTPException(status_code=404, detail="Rule not found")


@router.put("/{rule_id}", response_model=Rule)
async def update_rule(rule_id: int, rule_update: RuleUpdate):
    for rule in rules_db:
        if rule.id == rule_id:
            if rule_update.name is not None:
                rule.name = rule_update.name
            if rule_update.description is not None:
                rule.description = rule_update.description
            if rule_update.globs is not None:
                rule.globs = rule_update.globs
            if rule_update.always_apply is not None:
                rule.always_apply = rule_update.always_apply
            rule.updated_at = datetime.now()
            return rule
    raise HTTPException(status_code=404, detail="Rule not found")


@router.delete("/{rule_id}", status_code=204)
async def delete_rule(rule_id: int):
    for i, rule in enumerate(rules_db):
        if rule.id == rule_id:
            rules_db.pop(i)
            return
    raise HTTPException(status_code=404, detail="Rule not found")
