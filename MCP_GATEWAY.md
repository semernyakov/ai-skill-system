# MCP Gateway — Unified Entry Point for MCP Services

## Problem Statement

AI Skill System currently has no centralized mechanism for managing MCP (Model Context Protocol) services. Each MCP server connection is handled individually, making it difficult to:
- Discover available services
- Manage service configuration
- Monitor service health
- Scale service deployments
- Handle service lifecycle

## Proposed Architecture

### Central MCP Gateway

```
.ai/
├── mcp/
│   ├── gateway.py              # Main MCP gateway server
│   ├── config.json             # Service configuration
│   ├── services/               # MCP service adapters
│   │   ├── __init__.py
│   │   ├── filesystem.py       # Filesystem operations
│   │   ├── git.py              # Git operations
│   │   ├── github.py           # GitHub API
│   │   └── database.py         # Database operations
│   ├── registry.json            # Service registry
│   └── health.py               # Health monitoring
└── scripts/
    ├── start-mcp-gateway.sh    # Start gateway
    └── register-service.sh    # Register new service
```

### Key Components

#### 1. MCP Gateway Server (`gateway.py`)

**Purpose:** Central entry point for all MCP service requests

**Responsibilities:**
- Route requests to appropriate MCP services
- Service discovery and load balancing
- Authentication and authorization
- Request/response logging
- Error handling and retry logic
- Service health monitoring

**API Endpoints:**
```python
POST /mcp/{service_name}/invoke   # Invoke MCP service
GET  /mcp/services                 # List available services
GET  /mcp/health/{service_name}    # Check service health
POST /mcp/register                 # Register new service
DELETE /mcp/{service_name}         # Unregister service
```

#### 2. Service Configuration (`config.json`)

```json
{
  "gateway": {
    "host": "localhost",
    "port": 8080,
    "log_level": "info"
  },
  "services": {
    "filesystem": {
      "enabled": true,
      "adapter": "filesystem",
      "config": {
        "allowed_paths": [".ai/", "evals/"],
        "read_only": false
      }
    },
    "git": {
      "enabled": true,
      "adapter": "git",
      "config": {
        "repo_path": "."
      }
    },
    "github": {
      "enabled": true,
      "adapter": "github",
      "config": {
        "api_token": "${GITHUB_TOKEN}",
        "default_owner": "semernyakov"
      }
    }
  }
}
```

#### 3. Service Adapters (`services/`)

Each MCP service has an adapter that implements a common interface:

```python
class MCPServiceAdapter:
    def __init__(self, config: dict):
        self.config = config
    
    async def invoke(self, method: str, params: dict) -> dict:
        """Invoke MCP service method"""
        pass
    
    async def health(self) -> bool:
        """Check service health"""
        pass
    
    async def capabilities(self) -> dict:
        """Return service capabilities"""
        pass
```

#### 4. Service Registry (`registry.json`)

Dynamic registry of available services:

```json
{
  "services": {
    "filesystem": {
      "status": "active",
      "last_heartbeat": "2026-04-11T18:30:00Z",
      "capabilities": ["read_file", "write_file", "list_dir"],
      "version": "1.0.0"
    },
    "git": {
      "status": "active",
      "last_heartbeat": "2026-04-11T18:30:00Z",
      "capabilities": ["commit", "push", "pull", "status"],
      "version": "1.0.0"
    }
  }
}
```

## Integration with AI Skill System

### Usage in Skills

Skills can reference MCP services through the gateway:

```yaml
---
name: file-manager
description: >
  Manage project files through MCP gateway.
  Use when user needs to read, write, or organize files.
---

# This skill automatically routes to MCP gateway
# Service: filesystem
# Methods: read_file, write_file, list_dir, delete_file
```

### Integration with IDEs

Update `.ai/rules/000-core.mdc` to include MCP gateway usage:

```yaml
---
description: Core rules including MCP gateway access
---

## MCP Gateway Usage

All file operations should go through MCP gateway:
- Use MCP filesystem service for file operations
- Use MCP git service for git operations
- Use MCP github service for GitHub API calls

Gateway endpoint: http://localhost:8080/mcp
```

## Implementation Plan

### Phase 1: Core Gateway (Week 1)

**Deliverables:**
- Basic gateway server (`gateway.py`)
- Service adapter interface
- Filesystem service adapter
- Configuration structure
- Basic health monitoring

**Files to create:**
- `.ai/mcp/gateway.py`
- `.ai/mcp/config.json`
- `.ai/mcp/services/__init__.py`
- `.ai/mcp/services/filesystem.py`
- `.ai/scripts/start-mcp-gateway.sh`

### Phase 2: Service Adapters (Week 2)

**Deliverables:**
- Git service adapter
- GitHub service adapter
- Database service adapter (optional)
- Service registry implementation
- Service discovery mechanism

**Files to create:**
- `.ai/mcp/services/git.py`
- `.ai/mcp/services/github.py`
- `.ai/mcp/services/database.py`
- `.ai/mcp/registry.json`
- `.ai/scripts/register-service.sh`

### Phase 3: Advanced Features (Week 3)

**Deliverables:**
- Authentication and authorization
- Request logging and monitoring
- Load balancing
- Service health monitoring dashboard
- Auto-restart for failed services

**Files to create:**
- `.ai/mcp/auth.py`
- `.ai/mcp/monitoring.py`
- `.ai/mcp/health.py`

## Benefits

1. **Centralized Management:** Single point for all MCP service configuration
2. **Service Discovery:** Easy to discover available services and capabilities
3. **Health Monitoring:** Track service health and availability
4. **Scalability:** Easy to add new services without modifying core system
5. **Security:** Centralized authentication and authorization
6. **Observability:** Unified logging and monitoring

## Migration Path

### Current State
- MCP services used directly through individual connections
- No centralized configuration
- No service discovery mechanism

### Target State
- All MCP requests routed through gateway
- Centralized configuration in `config.json`
- Service registry for discovery
- Health monitoring for all services

### Migration Steps

1. **Phase 1:** Deploy gateway alongside existing direct connections
2. **Phase 2:** Migrate skills to use gateway endpoints
3. **Phase 3:** Deprecate direct connections
4. **Phase 4:** Remove direct connection code

## Decision Required

**Arbitr:** Which phase should we implement first?

**Options:**
- **A)** Phase 1 only (Core gateway + filesystem adapter)
- **B)** Phase 1 + 2 (Core gateway + Git/GitHub adapters)
- **C)** Full implementation (All phases)

**Recommendation:** **Option B** — Core gateway + Git/GitHub adapters provide essential functionality for AI Skill System workflow.

## Technical Considerations

### Technology Stack
- **Gateway:** FastAPI (async, high performance)
- **Configuration:** JSON with environment variable support
- **Service Discovery:** In-memory registry (can migrate to etcd/consul later)
- **Monitoring:** Prometheus metrics + Grafana dashboard (optional)
- **Logging:** Structlog for structured JSON logging

### Performance
- Async I/O for concurrent request handling
- Connection pooling for external services
- Caching for frequently accessed data
- Rate limiting to prevent abuse

### Security
- API token authentication
- Service-level authorization
- Request validation
- Audit logging

## Success Metrics

### Before Implementation
- No centralized MCP management
- Manual service configuration
- No health monitoring
- Difficult to add new services

### After Implementation
- Centralized gateway for all MCP services
- Declarative configuration
- Real-time health monitoring
- Easy service addition through adapters
- 90% reduction in service integration time
