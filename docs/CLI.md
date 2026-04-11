# AI Skill System CLI

The AI Skill System CLI provides command-line access to all system management functions.

## Installation

The CLI is installed automatically with the package. Run with:

```bash
uv run ai-skill-system
```

## Commands

### Rules Management

```bash
# List all rules
uv run ai-skill-system rules list

# Create a new rule
uv run ai-skill-system rules create --name "My Rule" --description "Rule description"

# Delete a rule
uv run ai-skill-system rules delete <rule_id>
```

### Skills Management

```bash
# List all skills
uv run ai-skill-system skills list

# Create a new skill
uv run ai-skill-system skills create --name "My Skill" --description "Skill description"

# Delete a skill
uv run ai-skill-system skills delete <skill_id>
```

### MCP Gateway Management

```bash
# List all MCP services
uv run ai-skill-system mcp list

# Start an MCP service
uv run ai-skill-system mcp start <service_name>

# Stop an MCP service
uv run ai-skill-system mcp stop <service_name>

# Check health of all MCP services
uv run ai-skill-system mcp health
```

### IDE Synchronization

```bash
# Run IDE synchronization
uv run ai-skill-system sync run

# Force sync all IDEs
uv run ai-skill-system sync run --force-all
```

### System Audit

```bash
# Run security audit
uv run ai-skill-system audit run --type security

# Run performance audit
uv run ai-skill-system audit run --type performance

# Run architecture audit
uv run ai-skill-system audit run --type architecture

# Run compliance audit
uv run ai-skill-system audit run --type compliance

# List all audit results
uv run ai-skill-system audit results
```

### System Logs

```bash
# View logs
uv run ai-skill-system logs view

# View logs for specific service
uv run ai-skill-system logs view --service api

# View logs with specific level
uv run ai-skill-system logs view --level ERROR

# Limit number of logs
uv run ai-skill-system logs view --limit 100
```

## Examples

```bash
# Create a rule and list all rules
uv run ai-skill-system rules create --name "Test Rule" --description "A test rule"
uv run ai-skill-system rules list

# Start MCP filesystem service and check health
uv run ai-skill-system mcp start filesystem
uv run ai-skill-system mcp health

# Run security audit
uv run ai-skill-system audit run --type security
uv run ai-skill-system audit results

# View recent error logs
uv run ai-skill-system logs view --level ERROR --limit 20
```
