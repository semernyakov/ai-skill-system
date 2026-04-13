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
    @echo "🖥️  Server Commands:"
    @echo "  just server-dev           - Launch backend"
    @echo "  just server-dev-reload     - Hot-reload backend"
    @echo "  just server-tui           - Open terminal UI"
    @echo "  just server-cli <args>    - Run CLI commands"
    @echo ""
    @echo "🔧 Maintenance:"
    @echo "  just server-test          - Run tests"
    @echo "  just server-lint          - Check code quality"
    @echo "  just server-format        - Format code"
    @echo ""
    @echo "📦 Dependencies:"
    @echo "  just server-sync          - Install dependencies"
    @echo "  just server-clear-cache   - Clear all caches"

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

client-format:
    #!/usr/bin/env bash
    cd client && bun run format

client-sync:
    #!/usr/bin/env bash
    cd client && bun install

client-clear-cache:
    #!/usr/bin/env bash
    bun pm cache rm

client-help:
    @echo "🌐 Client Commands:"
    @echo "  just client-dev           - Start dev server"
    @echo "  just client-build         - Build for production"
    @echo "  just client-preview       - Preview production build"
    @echo ""
    @echo "🔧 Maintenance:"
    @echo "  just client-lint          - Check code quality"
    @echo "  just client-format        - Format code with auto-fix"
    @echo ""
    @echo "📦 Dependencies:"
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
    echo "⚠️  WARNING: This will delete the database and all data!"
    echo "Type 'yes' to confirm, or anything else to cancel."
    read -p "Are you sure? " confirmation
    if [ "$confirmation" != "yes" ]; then
        echo "❌ Database reset cancelled"
        exit 0
    fi
    echo "🗑️  Deleting database..."
    rm -f server/ai_skill_system.db
    echo "🔄 Reinitializing database..."
    @just db-init
    echo "✅ Database reset complete!"

# MCP Gateway commands
mcp-start:
    #!/usr/bin/env bash
    .ai/scripts/start-mcp-gateway.sh

mcp-help:
    @echo "🔌 MCP Gateway:"
    @echo "  just mcp-start     - Start MCP Gateway"

# External/Submodule commands
external-init:
    #!/usr/bin/env bash
    echo "📦 Initializing submodules..."
    git submodule update --init --recursive
    echo "✅ Submodules initialized"

external-update:
    #!/usr/bin/env bash
    echo "📦 Updating submodules to latest..."
    git submodule update --remote
    echo "✅ Submodules updated"

external-status:
    #!/usr/bin/env bash
    echo "📊 Submodule status:"
    git submodule status

external-sync:
    #!/usr/bin/env bash
    echo "📦 Installing dependencies in submodules..."
    cd external/agentskills/skills-ref && uv sync
    echo "✅ Submodule dependencies installed"

external-help:
    @echo "📦 External/Submodules:"
    @echo "  just external-init        - Initialize submodules"
    @echo "  just external-update      - Update submodules to latest"
    @echo "  just external-status      - Check submodule status"
    @echo "  just external-sync        - Install submodule dependencies"

# Rules sync commands
sync-all:
    #!/usr/bin/env bash
    .ai/scripts/sync-all.sh

sync-cursor:
    #!/usr/bin/env bash
    .ai/scripts/sync-all.sh

# System commands
start:
    #!/usr/bin/env bash
    set -e
    echo "🚀 Quick Start: Setting up AI Skill System..."
    just system-init
    just system-run

install:
    echo "📦 Installing dependencies..."
    just server-sync
    just client-sync

clean:
    echo "🧹 Cleaning caches..."
    just server-clear-cache
    just client-clear-cache

system-init:
    echo "Let's set up your AI Skill System..."
    echo ""
    echo "📦 First, we'll grab the dependencies..."
    just server-sync || { echo "Server sync failed"; exit 1; }
    just client-sync || { echo "Client sync failed"; exit 1; }
    echo "✅ Dependencies installed!"
    echo ""
    echo "🗄️  Now, let's set up the database..."
    just db-init || { echo "Database initialization failed"; exit 1; }
    echo "✅ Database ready!"
    echo ""
    echo "🎉 You're all set! Run 'just start' or 'just system-run' to begin."

system-run:
    #!/usr/bin/env bash
    set -e
    echo "🚀 Launching AI Skill System..."
    echo ""
    echo "🖥️  Starting backend with hot-reload..."
    just server-dev-reload &
    SERVER_PID=$!
    echo "⏳ Waiting for backend to be ready..."
    sleep 3
    # Check if process is still running
    if ! kill -0 $SERVER_PID 2>/dev/null; then
        echo "❌ Backend failed to start (process died)"
        exit 1
    fi
    # Check health endpoint
    if ! curl -f http://127.0.0.1:8000/health > /dev/null 2>&1; then
        echo "❌ Backend health check failed"
        kill $SERVER_PID 2>/dev/null || true
        exit 1
    fi
    echo "✅ Backend is healthy!"
    echo ""
    echo "🌐 Starting frontend..."
    just client-dev
    kill $SERVER_PID 2>/dev/null || true

dev:
    #!/usr/bin/env bash
    set -e
    echo "🛠️  Starting dev environment..."
    echo ""
    echo "🖥️  Launching backend..."
    just server-dev-reload &
    SERVER_PID=$!
    echo "🌐 Launching frontend..."
    just client-dev
    kill $SERVER_PID 2>/dev/null || true

help:
    @echo "🚀 AI Skill System - Quick Start"
    @echo ""
    @echo "  just start                 - Setup and run everything (recommended)"
    @echo ""
    @echo "🛠️  Development:"
    @echo "  just dev                   - Start dev environment"
    @echo "  just server-help           - Backend commands"
    @echo "  just client-help           - Frontend commands"
    @echo ""
    @echo "🗄️  Database:"
    @echo "  just db-init               - Initialize database"
    @echo "  just db-migrate            - Run migrations"
    @echo "  just db-reset              - Reset database (destructive)"
    @echo ""
    @echo "� External/Submodules:"
    @echo "  just external-help         - External dependency commands"
    @echo ""
    @echo "�🔌 MCP Gateway:"
    @echo "  just mcp-help              - MCP commands"
    @echo ""
    @echo "📦 Setup & Maintenance:"
    @echo "  just install               - Install dependencies"
    @echo "  just clean                 - Clear caches"
    @echo "  just system-init           - Full system initialization"
    @echo "  just system-run            - Start all services"
    @echo ""
    @echo "🔄 Sync:"
    @echo "  just sync-all              - Sync rules to all IDEs"
