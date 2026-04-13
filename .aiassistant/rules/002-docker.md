<!-- PyCharm AI Project Rule -->
<!-- Source: .ai/rules/002-docker.mdc -->
<!-- Synced: Mon Apr 13 09:04:01 MSK 2026 -->
<!-- Rule type: Always (apply to all files) -->

---
description: Docker best practices for Python AI microservices.
globs: ["**/Dockerfile", "**/docker-compose*.yml", "**/.dockerignore"]
alwaysApply: false
---

# DOCKER

## Dockerfile Template (use this exact structure)
```dockerfile
FROM python:3.11-slim AS builder
WORKDIR /app
RUN pip install uv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

FROM python:3.11-slim AS runtime
WORKDIR /app
COPY --from=builder /app/.venv ./.venv
COPY app/ ./app/
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Rules
- Multi-stage build mandatory — builder + runtime
- Never install dev deps in runtime image
- `.dockerignore` must exclude: `.git`, `__pycache__`, `*.pyc`, `.env`, `tests/`, `*.md`
- Image labels: `org.opencontainers.image.*` standard
- Health check in every Dockerfile:
  ```dockerfile
  HEALTHCHECK --interval=30s --timeout=10s CMD curl -f http://localhost:8000/health || exit 1
  ```
- Non-root user: `RUN useradd -m app && USER app`
