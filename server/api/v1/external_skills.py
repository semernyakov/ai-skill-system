"""External Skills API endpoints for interacting with skills-ref library"""

import subprocess
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException

from server.core.auth import get_current_user
from server.db.models import User

router = APIRouter(prefix="/api/v1/external-skills", tags=["external-skills"])

SKILLS_REF_PATH = Path("external/agentskills/skills-ref")


@router.post("/validate")
async def validate_skill(
    skill_path: str,
    current_user: User = Depends(get_current_user),
):
    """Validate a skill using skills-ref library"""
    try:
        full_path = SKILLS_REF_PATH / skill_path
        result = subprocess.run(
            ["uv", "run", "skills-ref", "validate", str(full_path)],
            capture_output=True,
            text=True,
            cwd=str(SKILLS_REF_PATH),
        )

        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr if result.returncode != 0 else None,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/read-properties")
async def read_skill_properties(
    skill_path: str,
    current_user: User = Depends(get_current_user),
):
    """Read skill properties using skills-ref library"""
    try:
        full_path = SKILLS_REF_PATH / skill_path
        result = subprocess.run(
            ["uv", "run", "skills-ref", "read-properties", str(full_path)],
            capture_output=True,
            text=True,
            cwd=str(SKILLS_REF_PATH),
        )

        if result.returncode != 0:
            raise HTTPException(status_code=400, detail=result.stderr)

        # Parse JSON output
        import json

        return json.loads(result.stdout)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse output: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/to-prompt")
async def generate_prompt(
    skill_paths: list[str],
    current_user: User = Depends(get_current_user),
):
    """Generate XML prompt for available skills using skills-ref library"""
    try:
        full_paths = [str(SKILLS_REF_PATH / path) for path in skill_paths]
        result = subprocess.run(
            ["uv", "run", "skills-ref", "to-prompt"] + full_paths,
            capture_output=True,
            text=True,
            cwd=str(SKILLS_REF_PATH),
        )

        if result.returncode != 0:
            raise HTTPException(status_code=400, detail=result.stderr)

        return {"prompt": result.stdout}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list")
async def list_external_skills(
    current_user: User = Depends(get_current_user),
):
    """List available skills in the external agentskills repository"""
    try:
        skills_ref_dir = SKILLS_REF_PATH
        if not skills_ref_dir.exists():
            return []

        skills = []
        # Look for skill directories (containing SKILL.md)
        for item in skills_ref_dir.rglob("SKILL.md"):
            skill_dir = item.parent
            relative_path = skill_dir.relative_to(SKILLS_REF_PATH)

            # Try to read skill properties
            try:
                result = subprocess.run(
                    ["uv", "run", "skills-ref", "read-properties", str(skill_dir)],
                    capture_output=True,
                    text=True,
                    cwd=str(SKILLS_REF_PATH),
                )

                if result.returncode == 0:
                    import json

                    props = json.loads(result.stdout)
                    skills.append(
                        {
                            "path": str(relative_path),
                            "name": props.get("name", "Unknown"),
                            "description": props.get("description", ""),
                            "source": "agentskills",
                        }
                    )
            except Exception:
                # If we can't read properties, still add the skill
                skills.append(
                    {
                        "path": str(relative_path),
                        "name": skill_dir.name,
                        "description": "",
                        "source": "agentskills",
                    }
                )

        return skills
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
