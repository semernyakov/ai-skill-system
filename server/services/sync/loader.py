"""Load skills from external agentskills repository"""

import logging
from collections.abc import Generator
from pathlib import Path

logger = logging.getLogger(__name__)


class SkillLoader:
    """Load skill files from agentskills repository"""

    def __init__(self, agentskills_path: Path):
        self.agentskills_path = agentskills_path

    def load_skill_dirs(self) -> Generator[Path, None, None]:
        """Yield skill directories from agentskills repository"""
        if not self.agentskills_path.exists():
            logger.warning(f"Agentskills path not found: {self.agentskills_path}")
            return

        for skill_dir in self.agentskills_path.iterdir():
            if not skill_dir.is_dir():
                continue
            yield skill_dir

    def load_skill_yaml(self, skill_dir: Path) -> Path | None:
        """Get skill.yaml path from skill directory"""
        skill_yaml = skill_dir / "skill.yaml"
        if skill_yaml.exists():
            return skill_yaml
        return None

    def load_prompt_md(self, skill_dir: Path) -> Path | None:
        """Get prompt.md path from skill directory"""
        prompt_md = skill_dir / "prompt.md"
        if prompt_md.exists():
            return prompt_md
        return None
