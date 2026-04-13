# Skills Guide

This guide explains how to work with skills in the AI Skill System.

## Overview

Skills are reusable AI capabilities that can be triggered by specific user requests. They follow a standardized format and can be used across different IDEs and AI platforms.

## Skill Structure

Skills in this project are located in `.ai/skills/`:

```
.ai/skills/
├── SKILL_CREATOR.md      # Guide for creating new skills
├── SKILL_TEMPLATE.md     # Template for skill structure
├── agents/               # Agent-based skills
├── assertions/           # Test assertions for skill evaluation
├── schemas/              # Data schemas for skill inputs/outputs
├── styles/               # CSS styles for HTML outputs
├── templates/            # HTML templates
├── system-analyzer/      # System analysis skill
├── system-auditor/       # System audit skill
└── templates/            # Skill templates
```

## Creating a New Skill

### 1. Use the Skill Creator

The Skill Creator agent helps you build production-ready skills with automated testing:

```
# Reference the skill creator in your AI assistant
.ai/skills/SKILL_CREATOR.md
```

The Skill Creator will:
1. Gather requirements for the skill
2. Create the SKILL.md file
3. Generate test cases
4. Run evaluations
5. Optimize the skill based on results

### 2. Manual Skill Creation

Follow the template in `.ai/skills/SKILL_TEMPLATE.md`:

```markdown
---
name: skill-name
description: >
  Concise description for triggering logic.
  Include when to use and trigger phrases.
  Aim for 80-120 words.
---

## Purpose
One sentence: what does this skill enable Claude to do?

## When to Use
Trigger conditions and non-trigger conditions.

## Instructions
Step-by-step, imperative style.

## Output Format
Example output and required elements.

## Edge Cases
Handle gracefully: empty input, invalid format, etc.
```

## Skill Evaluation

### Test Structure

Create `evals/evals.json` in your skill directory:

```json
{
  "skill_name": "my-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "Realistic user request that should trigger skill",
      "assertions": [
        {
          "type": "contains",
          "value": "expected substring in output"
        },
        {
          "type": "format",
          "value": "json|markdown|svg|etc"
        }
      ],
      "files": []
    }
  ]
}
```

### Running Evaluations

Use the evaluation framework to test your skills:

```bash
# Run skill evaluation
python -m server.services.skill_evaluator

# View results
open evals/results/latest/report.html
```

## Built-in Skills

### System Analyzer

Analyzes the entire codebase and outputs system statistics:
- File counts, LOC, language distribution
- Dependency analysis

**Trigger:** "analyze system", "codebase stats", "project metrics"

### System Auditor

Comprehensive system audit for AI microservices:
- Security, performance, architecture, compliance
- Prioritized findings and detailed report

**Trigger:** "audit system", "security check", "performance review"

## Skill Best Practices

### Token Economy

- Keep metadata (name + description) under 100 words
- Main body ideally under 500 lines
- Use external resources (scripts/, references/) for heavy content

### Triggering Accuracy

- Be "pushy" with descriptions - better to trigger extra than miss
- Include synonyms and implicit intents
- Test with realistic user queries (typos, slang, implicit requests)

### Output Format

- Show exact templates or examples
- Claude copies patterns better than interpreting descriptions
- Use structured outputs (JSON schema) over free text when possible

## Integration with IDEs

Skills can be used in multiple environments:

- **Cursor IDE:** `.cursor/skills/`
- **Windsurf:** `.windsurf/skills/`
- **Runtime agents:** `src/skills/`

All follow the same SKILL.md format.

## References

- [Skill Creator Guide](../../.ai/skills/SKILL_CREATOR.md) - Detailed skill creation workflow
- [Skill Template](../../.ai/skills/SKILL_TEMPLATE.md) - Skill structure template
- [System Guide](SYSTEM_GUIDE.md) - Overall system architecture
