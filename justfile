# AI Skill System - Project Management with Just

# Default recipe
default:
    @just --list

# Server commands
server-dev:
    #!/usr/bin/env bash
    cd server && uv run main.py

server-dev-reload:
    #!/usr/bin/env bash
    cd server && uv run uvicorn server.main:app --reload --host 127.0.0.1 --port 8000

server-tui:
    #!/usr/bin/env bash
    uv run ai-skill-system-tui

server-cli *args:
    #!/usr/bin/env bash
    uv run ai-skill-system {{args}}

server-test:
    #!/usr/bin/env bash
    cd server && uv run pytest

server-lint:
    #!/usr/bin/env bash
    cd server && uv run ruff check .

server-format:
    #!/usr/bin/env bash
    cd server && uv run ruff format .

server-sync:
    #!/usr/bin/env bash
    uv sync

server-clear-cache:
    #!/usr/bin/env bash
    uv run ai-skill-system-clear-cache

server-clear-python-cache:
    #!/usr/bin/env bash
    uv run ai-skill-system-clear-python-cache

server-clear-redis-cache:
    #!/usr/bin/env bash
    uv run ai-skill-system-clear-redis-cache

server-help:
    @echo "Server commands:"
    @echo "  just server-dev              - Run server (main.py)"
    @echo "  just server-dev-reload        - Run server with auto-reload"
    @echo "  just server-tui              - Run TUI"
    @echo "  just server-cli <args>       - Run CLI with args"
    @echo "  just server-test             - Run tests"
    @echo "  just server-lint             - Run linter"
    @echo "  just server-format           - Format code"
    @echo "  just server-sync             - Sync dependencies"
    @echo "  just server-clear-cache      - Clear all caches"
    @echo "  just server-clear-python-cache   - Clear Python cache"
    @echo "  just server-clear-redis-cache   - Clear Redis cache"

# Client commands
client-dev:
    #!/usr/bin/env bash
    cd client && bun run dev

client-build:
    #!/usr/bin/env bash
    cd client && bun run build

client-preview:
    #!/usr/bin/env bash
    cd client && bun run preview

client-lint:
    #!/usr/bin/env bash
    cd client && bun run lint

client-sync:
    #!/usr/bin/env bash
    cd client && bun install

client-clear-cache:
    #!/usr/bin/env bash
    bun pm cache rm

client-help:
    @echo "Client commands:"
    @echo "  just client-dev           - Run dev server"
    @echo "  just client-build         - Build for production"
    @echo "  just client-preview       - Preview production build"
    @echo "  just client-lint          - Run linter"
    @echo "  just client-sync          - Install dependencies"
    @echo "  just client-clear-cache   - Clear bun cache"

# Database commands
db-init:
    #!/usr/bin/env bash
    cd server && uv run python -m server.db.init_db

db-migrate:
    #!/usr/bin/env bash
    cd server && uv run alembic upgrade head

db-reset:
    #!/usr/bin/env bash
    rm -f server/ai_skill_system.db
    @just db-init

# MCP Gateway commands
mcp-start:
    #!/usr/bin/env bash
    .ai/scripts/start-mcp-gateway.sh

mcp-help:
    @echo "MCP commands:"
    @echo "  just mcp-start     - Start MCP Gateway"

# Rules sync commands
sync-all:
    #!/usr/bin/env bash
    .ai/scripts/sync-all.sh

sync-cursor:
    #!/usr/bin/env bash
    .ai/scripts/sync-all.sh

# System commands
install:
    #!/usr/bin/env bash
    echo "Installing dependencies..."
    @just server-sync
    @just client-sync

clean:
    #!/usr/bin/env bash
    echo "Cleaning caches..."
    @just server-clear-cache
    @just client-clear-cache

dev:
    #!/usr/bin/env bash
    echo "Starting development environment..."
    @just server-dev-reload &
    @just client-dev

help:
    @echo "AI Skill System - Just Commands"
    @echo ""
    @echo "Server: just server-help"
    @echo "Client: just client-help"
    @echo "Database: just db-init, just db-migrate, just db-reset"
    @echo "MCP: just mcp-help"
    @echo "Sync: just sync-all"
    @echo "Install: just install"
    @echo "Clean: just clean"
    @echo "Dev: just dev"
