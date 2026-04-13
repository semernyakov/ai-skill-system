# AI Skill System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)

Cross-IDE system of rules and skills for AI-assisted development. MVP stack: FastAPI + SQLite + JWT.

## What's inside

- `.ai/rules/` — universal rules
- `.ai/skills/` — templates and agents for skill workflow
- `.ai/scripts/` — synchronization, migrations, eval scripts
- `server/` — FastAPI backend with SQLite database
- IDE mirrors: `.cursor/`, `.windsurf/`, `.idea/`

## Quick start

### Installation

```bash
# Install Python dependencies
cd server
uv sync

# Initialize database
uv run python -m server.db.init_db
```

### Start server

```bash
cd server
just dev
```

Server will be available at `http://127.0.0.1:8000`

### CLI usage

```bash
# Login
ai-skill-system auth login

# List rules
ai-skill-system rules list

# List skills
ai-skill-system skills list
```

## Team model

Solo Founder + Expert Roles:
Arbitr (Ivan), Дава, Маня, Саша, Кирилл.

## Documentation

### Guides
- [System Guide](docs/guides/SYSTEM_GUIDE.md) — Complete system architecture and setup
- [Skills Guide](docs/guides/SKILLS.md) — Working with AI skills
- [Submodules Guide](docs/guides/SUBMODULES.md) — Working with Git submodules
- [Just Guide](docs/guides/JUST_GUIDE.md) — Quick reference for common tasks
- [API Documentation](docs/API.md) — API endpoints and usage

### Project
- [Changelog](CHANGELOG.md) — Version history and changes
- [Contributing](CONTRIBUTING.md) — Contribution guidelines
- [Code of Conduct](CODE_OF_CONDUCT.md) — Community guidelines
- [Team](TEAM.md) — Team protocol and roles
- [Authors](AUTHORS.md) — Project contributors

### Security & Legal
- [Security](SECURITY.md) — Security policy and reporting
- [Disclaimer](DISCLAIMER.md) — Liability and usage terms

### Support
- [Support](SUPPORT.md) — Help, FAQ, and common issues
