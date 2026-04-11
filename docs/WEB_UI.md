# AI Skill System Web UI

The AI Skill System Web UI provides a modern web-based interface for system management.

## Installation

The Web UI is built with React + Vite and uses Tailwind CSS for styling.

### Running the Web UI

```bash
cd client
bun install
bun run dev
```

The Web UI will be available at `http://localhost:5173`

## Pages

### Dashboard
- System overview with statistics
- Rules count
- Skills count
- MCP services count
- Recent rules and MCP services

### Rules Manager
- List all rules
- Create new rules
- Delete rules
- View rule details

### Skills Manager
- List all skills
- Create new skills
- Delete skills
- View skill details

### MCP Gateway
- List all MCP services
- Start/stop services
- View service status
- Monitor service health

### Audit
- Run system audits (Security, Performance, Architecture, Compliance)
- View audit results
- Review findings and recommendations

## API Integration

The Web UI communicates with the backend API at `http://127.0.0.1:8000/api/v1`

### API Endpoints Used

- `GET /api/v1/rules` - List rules
- `POST /api/v1/rules` - Create rule
- `DELETE /api/v1/rules/{id}` - Delete rule
- `GET /api/v1/skills` - List skills
- `POST /api/v1/skills` - Create skill
- `DELETE /api/v1/skills/{id}` - Delete skill
- `GET /api/v1/mcp/services` - List MCP services
- `POST /api/v1/mcp/services/start` - Start service
- `POST /api/v1/mcp/services/stop` - Stop service
- `POST /api/v1/audit/run` - Run audit
- `POST /api/v1/sync` - Trigger sync

## Development

### Adding New Pages

1. Create a new component in `client/src/pages/`
2. Add API methods to `client/src/services/api.ts`
3. Add navigation button in `client/src/Layout.tsx`

### Styling

The Web UI uses Tailwind CSS with dark mode support. Use Tailwind utility classes for styling.

## Examples

```bash
# Install dependencies
cd client
bun install

# Start development server
bun run dev

# Build for production
bun run build

# Preview production build
bun run preview
```
