# AI Skill System

Cross-IDE system of rules and skills for AI-assisted development with MCP Gateway for unified service access.

## What's inside

- `.ai/rules/` — universal rules
- `.ai/skills/` — templates and agents for skill workflow
- `.ai/scripts/` — synchronization, migrations, eval scripts
- `.ai/mcp/` — MCP Gateway for centralized service access
- IDE mirrors: `.cursor/`, `.windsurf/`, `.idea/`

## Quick start

### Installation

```bash
# Install bun (if not already installed)
curl -fsSL https://bun.sh/install | bash

# Install dependencies
bun install
```

### Rule synchronization

```bash
.ai/scripts/sync-all.sh
```

### Start MCP Gateway

```bash
.ai/scripts/start-mcp-gateway.sh
```

Gateway will be available at `http://localhost:8080`

## Team model

Solo Founder + Expert Roles:
Arbitr (Ivan), Vasya, Yosya, Bosya, Manya, Sanya, Kirill.

## MCP Gateway

Centralized entry point for MCP services:

- **Filesystem Service** — file operations through secure API
- **Git Service** (in development) — git operations
- **GitHub Service** (in development) — GitHub API integration

See `MCP_GATEWAY.md` for more details
