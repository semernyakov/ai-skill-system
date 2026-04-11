# AI Skill System

Cross-IDE система правил и skills для AI-assisted разработки с MCP Gateway для унифицированного доступа к сервисам.

## Что внутри

- `.ai/rules/` — универсальные правила
- `.ai/skills/` — шаблоны и агенты для skill workflow
- `.ai/scripts/` — синхронизация, миграции, eval scripts
- `.ai/mcp/` — MCP Gateway для централизованного доступа к сервисам
- IDE mirrors: `.cursor/`, `.windsurf/`, `.idea/`

## Быстрый старт

### Синхронизация правил

```bash
.ai/scripts/sync-all.sh
```

### Запуск MCP Gateway

```bash
.ai/scripts/start-mcp-gateway.sh
```

Gateway будет доступен на `http://localhost:8080`

## Командная модель

Solo Founder + Expert Roles:
Arbitr (Ivan), Vasya, Yosya, Bosya, Manya, Sanya, Kirill.

## MCP Gateway

Централизованная точка входа для MCP сервисов:

- **Filesystem Service** — операции с файлами через безопасный API
- **Git Service** (в разработке) — операции с git
- **GitHub Service** (в разработке) — интеграция с GitHub API

Подробнее: см. `MCP_GATEWAY_PROPOSAL.md`
