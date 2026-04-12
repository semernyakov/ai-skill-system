# Deployment Guide

## Prerequisites

- Python 3.13+
- Node.js v22+
- Bun 1.3+
- System Bun installation (not Node.js Bun)

## Backend Deployment

### Using uv

```bash
# Install dependencies
uv sync

# Run server
uv run uvicorn server.main:app --host 0.0.0.0 --port 8000
```

### Using Docker

```bash
# Build image
docker build -t ai-skill-system .

# Run container
docker run -p 8000:8000 ai-skill-system
```

### Environment Variables

Create `.env` file:

```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_BASE_URL=http://127.0.0.1:8000/api/v1

# Database (if using external database)
DATABASE_URL=sqlite:///./ai_skill_system.db

# Logging
LOG_LEVEL=INFO
```

## Frontend Deployment

### Development

```bash
cd client

# Clear cache (MANDATORY before install)
bun pm cache rm

# Install dependencies
bun install

# Run dev server
bun run dev
```

### Production Build

```bash
cd client

# Build
bun run build

# Preview
bun run preview
```

### Using Nginx

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        root /path/to/client/dist;
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## CLI Deployment

### Install as System Command

```bash
# Create entry point
uv run pip install -e .

# Or use directly
uv run python -m server.cli.main --help
```

### Using pip

```bash
pip install -e .
ai-skill-system --help
```

## Production Considerations

### Security

- Add authentication/authorization
- Enable HTTPS/TLS
- Implement rate limiting
- Add input validation
- Use environment variables for secrets
- Enable CORS properly
- Add security headers

### Performance

- Use a production ASGI server (Gunicorn + Uvicorn workers)
- Enable caching
- Use CDN for static assets
- Optimize database queries
- Add connection pooling

### Monitoring

- Add health check endpoint
- Implement logging aggregation
- Add metrics collection
- Set up alerting

### Backup

- Regular database backups
- Backup configuration files
- Version control for rules and skills

## CI/CD

### GitHub Actions Example

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.13'
      - run: uv sync
      - run: uv run pytest tests/
      - run: docker build -t ai-skill-system .
      - run: docker push your-registry/ai-skill-system
```
