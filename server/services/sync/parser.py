"""Parse skill.yaml and prompt.md files"""

import logging
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)


class SkillParser:
    """Parse skill metadata and content"""

    def parse_skill_yaml(self, skill_yaml: Path) -> dict[str, Any] | None:
        """Parse skill.yaml file"""
        try:
            with open(skill_yaml) as f:
                content = yaml.safe_load(f)

            if not isinstance(content, dict):
                logger.warning(f"Invalid skill.yaml format: {skill_yaml}")
                return None

            return content
        except Exception as e:
            logger.error(f"Failed to parse {skill_yaml}: {e}")
            return None

    def parse_prompt_md(self, prompt_md: Path) -> str:
        """Parse prompt.md file"""
        try:
            with open(prompt_md) as f:
                return f.read()
        except Exception as e:
            logger.error(f"Failed to parse {prompt_md}: {e}")
            return ""
