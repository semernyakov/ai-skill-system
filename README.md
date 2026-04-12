# AI Skill System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Bun](https://img.shields.io/badge/Bun-1.0+-white.svg)](https://bun.sh/)

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

See `docs/guides/MCP_GATEWAY.md` for more details

## Documentation

### Guides
- [System Guide](docs/guides/SYSTEM_GUIDE.md) — Complete system architecture and setup
- [MCP Gateway](docs/guides/MCP_GATEWAY.md) — Gateway architecture and service adapters
- [Just Guide](docs/guides/JUST_GUIDE.md) — Quick reference for common tasks

### Project
- [Changelog](docs/project/CHANGELOG.md) — Version history and changes
- [Contributing](docs/project/CONTRIBUTING.md) — Contribution guidelines
- [Code of Conduct](docs/project/CODE_OF_CONDUCT.md) — Community guidelines
- [Team](docs/project/TEAM.md) — Team protocol and roles
- [Authors](docs/project/AUTHORS.md) — Project contributors

### Security & Legal
- [Security](docs/security/SECURITY.md) — Security policy and reporting
- [Disclaimer](docs/legal/DISCLAIMER.md) — Liability and usage terms

### Support
- [Support](docs/support/SUPPORT.md) — Help, FAQ, and common issues
