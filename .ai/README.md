# AI Rules & Skills

Universal AI configuration for Cursor, Windsurf, and PyCharm.

## Structure

```
.ai/
├── rules/          # Core rules (*.mdc files)
├── skills/         # Skill Creator system
├── prompts/        # System prompts for agents
└── scripts/        # Automation scripts
```

## Setup

```bash
# Initial setup
./ai/scripts/setup.sh

# Sync to all IDEs
.ai/scripts/sync-all.sh

# Auto-sync on git commits
.ai/scripts/install-hooks.sh
```

## IDE-Specific Instructions

### Cursor
Rules auto-load from `.cursor/rules/` or root `*.mdc` files.

### Windsurf  
Rules load from `.windsurf/rules/` or `.windsurfrules` file.

### PyCharm
1. Open Settings → Tools → AI Assistant
2. Under "Custom Instructions", click "Attach Context"
3. Select `.idea/ai-context.txt`

## Editing Rules

**Always edit files in `.ai/rules/` only!**

Other locations are auto-generated. Run `sync-all.sh` after changes.
