# AI Rules & Skills

Universal AI configuration for Cursor, Windsurf, and PyCharm with MCP Gateway.

## Structure

```
.ai/
├── rules/          # Core rules (*.mdc files)
├── skills/         # Skill Creator system
├── mcp/            # MCP Gateway for service access
│   ├── gateway.py  # FastAPI server
│   ├── config.json # Service configuration
│   └── services/   # Service adapters
├── prompts/        # System prompts for agents
└── scripts/        # Automation scripts
```

## Setup

```bash
# Install bun (if not already installed)
curl -fsSL https://bun.sh/install | bash

# Install dependencies
bun install

# Sync to all IDEs (including .aiassistant/rules/ for PyCharm)
.ai/scripts/sync-all.sh

# Auto-sync on git commits
.ai/scripts/install-hooks.sh

# Start MCP Gateway
.ai/scripts/start-mcp-gateway.sh
```

## MCP Gateway

Central entry point for MCP services:
- Filesystem Service — file operations
- Git Service (planned) — git operations
- GitHub Service (planned) — GitHub API

Gateway runs on `http://localhost:8080`

See `MCP_GATEWAY.md` for architecture details.

## IDE-Specific Instructions

### Cursor
Rules auto-load from `.cursor/rules/`.

### Windsurf  
Rules load from `.windsurf/rules/` or `.windsurfrules` file.

### PyCharm
**Official (recommended):**
1. Open Settings (Ctrl+Alt+S) → Tools → AI Assistant → Rules
2. Files in `.aiassistant/rules/` are auto-detected
3. Set Rule type: Always (rules), Manually (skills), By file patterns (domain-specific)

**Alternative:**
1. Open Settings → Tools → AI Assistant → Rules
2. Click New Project Rules File
3. Select `.idea/ai-context.txt`
4. Set Rule type to Always

## Editing Rules

**Always edit files in `.ai/rules/` only!**

Other locations are auto-generated. Run `sync-all.sh` after changes.
