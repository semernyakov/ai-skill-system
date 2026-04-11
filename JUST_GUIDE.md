# Just - Project Management Guide

## Installation

```bash
# Linux
curl -fsSL https://just.systems/install.sh | bash

# macOS
brew install just

# Or download from https://github.com/casey/just/releases
```

## Quick Start

```bash
# List all available commands
just

# Run server in development mode
just server:dev

# Run client in development mode
just client:dev

# Run both server and client
just dev
```

## Root Commands

### Server Commands
```bash
just server:help              # Show server commands
just server:dev              # Run server (main.py)
just server:dev-with-reload   # Run server with auto-reload
just server:tui              # Run TUI
just server:cli <args>       # Run CLI with args
just server:test             # Run tests
just server:lint             # Run linter
just server:format           # Format code
just server:sync             # Sync dependencies
just server:clear-cache      # Clear all caches
just server:clear-python-cache   # Clear Python cache
just server:clear-redis-cache   # Clear Redis cache
```

### Client Commands
```bash
just client:help              # Show client commands
just client:dev               # Run dev server
just client:build             # Build for production
just client:preview           # Preview production build
just client:lint              # Run linter
just client:sync              # Install dependencies
just client:clear-cache       # Clear bun cache
```

### Database Commands
```bash
just db-init                  # Initialize database
just db-migrate               # Run migrations
just db-reset                 # Reset database
```

### MCP Gateway Commands
```bash
just mcp:start                # Start MCP Gateway
just mcp:help                # Show MCP commands
```

### Rules Sync Commands
```bash
just sync:all                 # Sync all IDE rules
just sync:cursor              # Sync Cursor rules
```

### System Commands
```bash
just install                  # Install all dependencies
just clean                    # Clean all caches
just dev                      # Start dev environment (server + client)
```

## Module-Specific Commands

### Server (Yosya)
```bash
cd server
just dev                     # Run server
just dev-with-reload          # Run with auto-reload
just dev-with-debug           # Run with debug logging
just tui                      # Run TUI
just cli <args>               # Run CLI
just db-init                  # Initialize database
just db-migrate               # Run migrations
just db-reset                 # Reset database
just test                     # Run tests
just test-coverage            # Run tests with coverage
just lint                     # Run linter
just lint-fix                 # Run linter with auto-fix
just format                   # Format code
just bandit                   # Run security linter
just sync                     # Sync dependencies
just add <package>            # Add package
just add-dev <package>        # Add dev package
just clear-cache              # Clear all caches
```

### Client (Vasya)
```bash
cd client
just dev                      # Run dev server
just build                    # Build for production
just preview                  # Preview production build
just test                     # Run tests
just lint                     # Run linter
just lint-fix                 # Run linter with auto-fix
just format                   # Format code
just type-check               # Check TypeScript types
just sync                     # Install dependencies
just add <package>            # Add package
just add-dev <package>        # Add dev package
just clear-cache              # Clear bun cache
```

## Features

### Autocompletion
Just supports shell autocompletion. Add to your shell config:

```bash
# Bash
eval "$(just --completions bash)"

# Zsh
eval "$(just --completions zsh)"

# Fish
just --completions fish | source
```

### Variables
Just supports variables in justfile:

```justfile
# Define variables
python := "uv run python"
port := "8000"

# Use variables
dev:
    {{python}} main.py --port {{port}}
```

### Environment Variables
Pass environment variables:

```bash
just dev PORT=3000
```

### Conditional Execution
```justfile
# Conditional execution
dev:
    #!/usr/bin/env bash
    if [ -f ".env" ]; then
        uv run main.py
    else
        echo ".env not found"
    fi
```

## Best Practices

1. **Use descriptive recipe names** - `server:dev` instead of `s:dev`
2. **Keep recipes simple** - Complex logic in scripts
3. **Use shebang recipes** - For multi-line bash scripts
4. **Document recipes** - Add comments in justfile
5. **Use `--list`** - Always include help command

## Troubleshooting

### Just not found
```bash
# Install Just
curl -fsSL https://just.systems/install.sh | bash
```

### Permission denied
```bash
# Make justfile executable
chmod +x justfile
```

### Recipe not found
```bash
# List available recipes
just --list
```

## Integration with Existing Tools

### uv (Python)
```bash
just server:sync              # uv sync
just server:add <package>     # uv add
```

### bun (JavaScript)
```bash
just client:sync              # bun install
just client:add <package>     # bun add
```

### Redis
```bash
just server:clear-redis-cache # redis-cli FLUSHALL
```

## Migration from Make

| Make | Just |
| ---- | ---- |
| `make dev` | `just dev` |
| `make server:dev` | `just server:dev` |
| `make clean` | `just clean` |
| `VARIABLE=value make target` | `just target VARIABLE=value` |

## Additional Resources

- [Just Documentation](https://just.systems/)
- [Just GitHub](https://github.com/casey/just)
- [Just Examples](https://github.com/casey/just/tree/master/just-examples)
