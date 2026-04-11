# API Documentation

## Base URL

```
http://127.0.0.1:8000/api/v1
```

## Authentication

Currently no authentication is implemented. This is a security consideration for production deployment.

## Endpoints

### Rules

#### List Rules
```
GET /api/v1/rules
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "example-rule",
    "description": "Example rule description",
    "globs": ["**/*.py"],
    "always_apply": false,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": null
  }
]
```

#### Create Rule
```
POST /api/v1/rules
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "new-rule",
  "description": "Rule description",
  "globs": ["**/*.ts"],
  "always_apply": false
}
```

**Response:** 201 Created with rule object

#### Get Rule
```
GET /api/v1/rules/{id}
```

#### Update Rule
```
PUT /api/v1/rules/{id}
Content-Type: application/json
```

#### Delete Rule
```
DELETE /api/v1/rules/{id}
```

### Skills

#### List Skills
```
GET /api/v1/skills
```

#### Create Skill
```
POST /api/v1/skills
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "new-skill",
  "description": "Skill description"
}
```

#### Get Skill
```
GET /api/v1/skills/{id}
```

#### Update Skill
```
PUT /api/v1/skills/{id}
Content-Type: application/json
```

#### Delete Skill
```
DELETE /api/v1/skills/{id}
```

### MCP Gateway

#### List Services
```
GET /api/v1/mcp/services
```

#### Start Service
```
POST /api/v1/mcp/services/start
Content-Type: application/json
```

**Request Body:**
```json
{
  "service_name": "example-service"
}
```

#### Stop Service
```
POST /api/v1/mcp/services/stop
Content-Type: application/json
```

#### Check Service Health
```
GET /api/v1/mcp/services/{service_name}/health
```

#### Check All Services Health
```
GET /api/v1/mcp/services/health
```

### Sync

#### Run Sync
```
POST /api/v1/sync
Content-Type: application/json
```

**Request Body:**
```json
{
  "force_all": false
}
```

#### Get Sync Status
```
GET /api/v1/sync/status
```

### Audit

#### Run Audit
```
POST /api/v1/audit/run
Content-Type: application/json
```

**Request Body:**
```json
{
  "audit_type": "security"
}
```

#### Get Audit Results
```
GET /api/v1/audit/results
```

#### Get Audit Result
```
GET /api/v1/audit/results/{audit_id}
```

### Logs

#### View Logs
```
GET /api/v1/logs?service={service}&level={level}&limit={limit}
```

**Query Parameters:**
- `service` (optional): Filter by service name
- `level` (optional): Filter by log level (DEBUG, INFO, WARN, ERROR)
- `limit` (optional): Maximum number of log entries (default: 50)

#### Stream Logs
```
GET /api/v1/logs/stream?service={service}
```

## Error Responses

All endpoints may return error responses:

```json
{
  "detail": "Error message"
}
```

Common HTTP status codes:
- 400: Bad Request
- 404: Not Found
- 422: Validation Error
- 500: Internal Server Error
