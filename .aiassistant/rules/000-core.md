<!-- PyCharm AI Project Rule -->
<!-- Source: .ai/rules/000-core.mdc -->
<!-- Synced: Sun Apr 12 20:32:53 MSK 2026 -->
<!-- Rule type: Always (apply to all files) -->

---
description: Core rules for AI microservices. Token-first. Always active.
globs: ["**/*.py", "**/*.yaml", "**/*.yml", "**/*.dockerfile", "**/Dockerfile"]
alwaysApply: true
---

# CORE — AI Microservices

## Token Economy (ABSOLUTE PRIORITY)

- Answer ONLY the question asked — zero commentary
- Generate ONLY diff/changed blocks — never full files
- Use `# ... existing ...` for unchanged code
- Skip docstrings except on public API
- Inline comments ONLY for non-obvious logic
- No "best practices" sermons unless requested

## Output Discipline

**DO NOT:**

- Create files without explicit request
- Suggest project structure unprompted
- Add CI/CD/Docker/K8s unless asked
- Propose refactoring outside scope
- Write git commands or commit messages
- Generate tests without permission
- Offer alternatives unless asked
- Modify files outside current scope

**DO:**

- Minimum text, maximum signal
- Work within current file only
- Answer the literal question
- Stop when done

## Python Standards (non-negotiable)

- Python 3.13+, type hints everywhere
- Pydantic v2 for all models
- Async-first: `async def` for I/O, `httpx.AsyncClient`
- `uv` package manager, `pyproject.toml` only
- No `requirements.txt` unless explicitly requested

## Project Structure (enforce strictly)

```text
service-name/
├── src/
│   ├── main.py          # FastAPI app
│   ├── core/            # config, deps, logging
│   ├── agents/          # LLM agents
│   ├── skills/          # reusable functions
│   ├── api/v1/          # routers
│   └── models/          # Pydantic schemas
├── tests/
├── evals/               # skill evaluations
├── .cursor/
│   └── rules/           # cursor rules
├── Dockerfile
├── pyproject.toml
└── .env.example
```

## Error Handling (minimal)

- Custom exceptions in `src/core/exceptions.py`
- HTTP errors via `fastapi.HTTPException`
- Log with `structlog` JSON output
- No try/except unless error handling is essential

## Runtime Defaults (apply silently)

- Timeouts on all I/O (no infinite waits)
- Exponential backoff on retries (max 3)
- Graceful shutdown handlers
- Do NOT add unless explicitly needed for task

## Dependencies Management

- `uv add <package>` for new deps
- Lock with `uv lock`
- Ignore: `__pycache__/`, `*.egg-info/`, `.venv/`

## Code Style (enforced)

- `ruff` for linting (auto-fix enabled)
- `mypy` strict mode
- Max line length: 100
- No unused imports/variables
