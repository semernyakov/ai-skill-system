# Changelog

## 2026-04-12

### Security Fixes (Critical)
- Made JWT_SECRET_KEY required from environment with development default
- Removed password from console output in init_db.py
- Added authentication to all audit.py endpoints (EDITOR role required)
- Added authentication to all logs.py endpoints (VIEWER role required)
- Added authentication to all sync.py endpoints (EDITOR role required)
- Added authentication to all mcp.py endpoints (EDITOR role required)

### Architecture Improvements
- Added CORS middleware with configurable origins via settings.ALLOWED_ORIGINS
- Replaced global mutable state with Redis storage:
  - audit_results now stored in Redis (key: audit_results)
  - sync_status now stored in Redis (key: sync_status)
  - services_db now stored in Redis (key: mcp_services)
  - mock_logs now stored in Redis (key: logs)
- Created server/core/redis_client.py for shared state management
- Initialized Redis client on application startup

### Code Quality Improvements
- Fixed bare except clause in models/rule.py to catch json.JSONDecodeError
- Replaced print statements with logger in init_db.py
- Removed module-level JWT caching in security.py (now uses settings directly)
- Added .env.example with complete configuration template

### Configuration Updates
- Added ALLOWED_ORIGINS to settings (default: localhost:3000, 127.0.0.1:3000)
- JWT_SECRET_KEY now has development default (dev-secret-key-change-in-production)
- Added REDIS_URL to settings (default: redis://localhost:6379/0)

### Dependency Updates
- Added redis>=5.0.0 to dependencies
- Added fastapi-limiter>=0.2.0 to dependencies
- Added pyrate-limiter>=2.10.0 to dependencies

### Rate Limiting
- Added rate limiting to auth.py login endpoint
- Added rate limiting to rules.py endpoints
- Added rate limiting to skills.py endpoints
- Configured Redis backend for distributed rate limiting with fallback

### Database Improvements
- Added transaction rollback for all database operations in rules.py
- Added transaction rollback for all database operations in skills.py
- Fixed updated_at logic to correctly reflect changes
- Moved database initialization to startup event handler in main.py

### Model Updates
- Removed superficial SQL injection validation from RuleCreate and RuleUpdate models
- Removed superficial SQL injection validation from SkillCreate model
- Added JSON parsing error handling for globs field

## 2026-04-11

### MCP Gateway Implementation (Phase 1)
- Added MCP Gateway server (`.ai/mcp/gateway.py`) with FastAPI
- Implemented service adapter interface (`MCPServiceAdapter`)
- Added filesystem service adapter for file operations
- Created gateway configuration (`.ai/mcp/config.json`)
- Added start script (`.ai/scripts/start-mcp-gateway.sh`)
- Added `pyproject.toml` with dependencies (fastapi, uvicorn, pydantic)
- Created `MCP_GATEWAY.md` with architecture documentation

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
