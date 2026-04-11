# AI Skill System TUI

The AI Skill System TUI (Terminal User Interface) provides an interactive terminal-based interface for system management.

## Installation

The TUI is installed automatically with the package. Run with:

```bash
uv run ai-skill-system-tui
```

## Navigation

The TUI uses keyboard navigation:

- **d** - Dashboard view
- **r** - Rules Manager
- **s** - Skills Manager
- **m** - MCP Gateway
- **a** - Audit
- **q** - Quit

## Screens

### Dashboard
Shows system overview with statistics for rules, skills, and MCP services.

### Rules Manager
Displays all rules with their names and descriptions.

### Skills Manager
Displays all skills with their names and descriptions.

### MCP Gateway
Shows MCP Gateway services and their status (running/stopped).

### Audit
Provides access to system audit functionality.

## Examples

```bash
# Start the TUI
uv run ai-skill-system-tui

# Navigate using keyboard shortcuts
# Press 'd' for Dashboard
# Press 'r' for Rules
# Press 'm' for MCP Gateway
# Press 'q' to quit
```
