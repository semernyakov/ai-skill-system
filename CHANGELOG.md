# Changelog

## 2026-04-11

### MCP Gateway Implementation (Phase 1)
- Added MCP Gateway server (`.ai/mcp/gateway.py`) with FastAPI
- Implemented service adapter interface (`MCPServiceAdapter`)
- Added filesystem service adapter for file operations
- Created gateway configuration (`.ai/mcp/config.json`)
- Added start script (`.ai/scripts/start-mcp-gateway.sh`)
- Added `pyproject.toml` with dependencies (fastapi, uvicorn, pydantic)
- Created `MCP_GATEWAY_PROPOSAL.md` with architecture documentation

### Team Role Updates
- Renamed Dava to Vasya (Principal Software Engineer Front)
- Added Yosya (Principal AI/ML Engineer Backend)
- Renamed Sasha to Sanya (Behavioral Linguistics Expert)
- Renamed Kirill-QA to Kirill (Security & Performance Auditor)
- Added Bosya (Principal GeoOps / MlOps / DevOps Engineer)
- Updated all documentation with new roles

### Documentation Updates
- Updated `README.md` with MCP Gateway information
- Updated `SYSTEM_GUIDE.md` with MCP Gateway section
- Synchronized team roles across all documentation files
- Added DISCLAIMER.md with liability and usage terms
- Added SYSTEM_GUIDE.md with complete system description

### Script Updates
- Removed duplicate sync logic from `.pre-commit-config.yaml`
- Updated `.ai/scripts/sync-all.sh` to remove root .mdc copying

### Contact Information
- Updated contact email to `i.s.semernyakov@yandex.ru` throughout project

### Branding Updates
- Removed all mentions of omnikross.ru and omnikross.com from project

### Previous Changes
- Added LICENSE (MIT).
- Added CONTRIBUTING.md, CODE_OF_CONDUCT.md, SECURITY.md, SUPPORT.md, AUTHORS.md.
- Added GitHub templates: bug_report.md, feature_request.md, PULL_REQUEST_TEMPLATE.md.
- Added .pre-commit-config.yaml, .editorconfig, .gitattributes.
- Removed root `.mdc` files (rules now managed in `.ai/rules/` only).
- Removed `ai_skill_system_report.txt`.
- Renamed `chanelog.md` to `CHANGELOG.md`.
- Added root `README.md`.
- Added/updated `TEAM.md` and aligned `.ai/rules/003-team-protocol.mdc`.
- Updated `ide-compatibility-guide.md`.
- Updated `universal-rules-structure.md`.
