# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- JWT authentication with role-based access control (RBAC)
- Password complexity validation
- System audit functionality
- CLI authentication commands (login, logout, auth-status)

### Changed
- **BREAKING**: Stack simplified for MVP - removed Redis, rate limiting, TUI, MCP Gateway
- Replaced `@app.on_event("startup")` with `lifespan` event handler
- Updated API tests to handle authentication requirements
- Updated performance and security tests for authentication

### Removed
- Redis dependency and rate limiting (slowapi, fastapi-limiter)
- Textual TUI (Text User Interface) and related commands
- MCP Gateway endpoints and services
- Mock endpoints (audit, sync, mcp)
- TUI documentation (docs/TUI.md)
- MCP-related CLI tests

### Fixed
- Fixed circular import in server/api/v1/__init__.py (removed mcp import)
- Fixed lint errors (22 issues resolved)
- Fixed test failures (32 tests passing, 1 skipped)
- Fixed deprecation warnings in FastAPI lifespan handler

### Security
- Identified 3 P0 critical issues in audit:
  - Hardcoded JWT_SECRET_KEY
  - Hardcoded admin password
  - Wildcard CORS configuration
- Identified P1-P3 issues requiring attention before production

## [1.0.0] - 2026-04-12

### Added
- Initial MVP release
- FastAPI backend with SQLite database
- Rules and Skills CRUD API
- JWT authentication system
- CLI tool for system management
- Basic test suite
- Justfile for common tasks

### Documentation
- README with quick start guide
- API documentation
- System guide
- Deployment guide
- Just command guide
