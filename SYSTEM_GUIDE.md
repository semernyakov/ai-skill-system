# AI Skill System — Полное руководство

## Что это такое

AI Skill System — это кросс-IDE платформа для управления правилами и skills для AI-assisted разработки. Система обеспечивает унифицированное поведение AI-ассистентов (Cursor, Windsurf, PyCharm) через централизованные правила, автоматическую синхронизацию и framework для создания/тестирования skills.

## Архитектура

### Основные компоненты

```
ai-skill-system/
├── .ai/                          # Источник истины (Source of Truth)
│   ├── rules/                     # Универсальные правила (*.mdc)
│   │   ├── 000-core.mdc          # Core правила (token economy)
│   │   ├── 001-agentic.mdc       # Agentic системы
│   │   ├── 002-docker.mdc        # Docker стандарты
│   │   ├── 003-team-protocol.mdc # Team protocol
│   │   ├── 004-k8s.mdc           # Kubernetes стандарты
│   │   ├── 005-cicd.mdc          # CI/CD стандарты
│   │   └── 006-api.mdc           # API стандарты
│   ├── skills/                    # Skill Creator System
│   │   ├── SKILL_CREATOR.md      # Агент для создания skills
│   │   ├── SKILL_TEMPLATE.md     # Шаблон для skills
│   │   ├── agents/               # Eval агенты
│   │   │   ├── analyzer.md       # Анализ результатов
│   │   │   ├── comparator.md     # Сравнение итераций
│   │   │   └── grader.md        # Грейдинг assertions
│   │   ├── assertions/            # Программные проверки
│   │   │   ├── check_json.py     # Валидация JSON
│   │   │   ├── check_format.py   # Валидация формата
│   │   │   └── README.md
│   │   └── schemas/               # JSON схемы для eval
│   │       └── eval_schema.json
│   ├── scripts/                   # Автоматизация
│   │   ├── sync-all.sh           # Синхронизация IDE
│   │   ├── install-hooks.sh      # Git hooks
│   │   ├── aggregate_benchmark.py # Агрегация бенчмарков
│   │   ├── run_eval.py           # Запуск eval
│   │   ├── migrate-field-names.sh # Миграция полей
│   │   └── start-mcp-gateway.sh  # Запуск MCP Gateway
│   ├── mcp/                       # MCP Gateway
│   │   ├── gateway.py            # FastAPI сервер
│   │   ├── config.json           # Конфигурация сервисов
│   │   └── services/             # Адаптеры MCP сервисов
│   │       ├── __init__.py       # Интерфейс адаптеров
│   │       └── filesystem.py     # Fileservice адаптер
│   └── prompts/                   # System prompts
├── .cursor/                      # Cursor IDE конфигурация (автогенерируемая)
├── .windsurf/                    # Windsurf IDE конфигурация (автогенерируемая)
├── .idea/                        # PyCharm IDE конфигурация (автогенерируемая)
├── evals/                        # Evaluation workspace
│   └── workspace/                # Структура для итераций
│       ├── iteration-1/
│       ├── iteration-2/
│       └── template/
├── TEAM.md                       # Team protocol (организационный слой)
└── SYSTEM_GUIDE.md               # Этот файл
```

### Как это работает

#### 1. Правила (.mdc файлы)

Файлы `.mdc` (Markdown Config) содержат правила для AI-ассистентов с метаданными:

```yaml
---
description: Core rules for AI microservices
globs: ["**/*.py", "**/*.yaml"]
alwaysApply: true
---

# CORE — AI Microservices
## Token Economy
- Answer ONLY the question asked
- Generate ONLY diff/changed blocks
```

**Ключевые поля:**
- `description` - описание правила для триггеринга
- `globs` - к каким файлам применять правило
- `alwaysApply` - применять ли всегда

#### 2. Синхронизация IDE

Скрипт `sync-all.sh` копирует правила из `.ai/rules/` в IDE-специфичные директории:

- **Cursor** → `.cursor/rules/`
- **Windsurf** → `.windsurf/rules/` + `.windsurfrules` (единый файл)
- **PyCharm** → `.idea/ai-context.txt` (plain text)

**Автоматизация:** Git pre-commit hook автоматически запускает `sync-all.sh` перед каждым коммитом.

#### 3. Skill Creator System

**Workflow создания skill:**

1. **Discovery** — сбор требований (что делает skill, когда триггерится)
2. **Requirements** — deep dive в edge cases, форматы, критерии успеха
3. **SKILL.md** — создание файла skill с "pushy" описанием
4. **Test Generation** — генерация тестовых кейсов
5. **Benchmarking** — запуск eval с assertions
6. **Optimization** — итеративное улучшение описания

**Programmatic Assertions:**
- `check_json.py` — валидация JSON
- `check_format.py` — валидация формата (json/markdown/yaml)
- Быстрее LLM-грейдинга, детерминированные, переиспользуемые

**Evaluation Workspace:**
```
workspace/iteration-1/
├── runs/
│   ├── test-1-with-skill/
│   │   ├── output.txt
│   │   └── metadata.json
│   └── test-1-baseline/
├── grading.json      # Результаты per-test
└── benchmark.json    # Агрегированные метрики
```

#### 4. Team Protocol

**Роли:**
- **Arbitr (Иван)** — final decision-maker
- **Vasya** — Principal Software Engineer (Front)
- **Yosya** — Principal AI/ML Engineer (Backend)
- **Bosya** — Principal GeoOps / MlOps / DevOps Engineer
- **Manya** — Principal UX/UI + Marketing Strategist
- **Sanya** — Behavioral Linguistics Expert
- **Kirill** — Security & Performance Auditor

**Workflow:**
1. Proposal (варианты + риски)
2. Arbitr approval (YES/NO/YES with constraints)
3. Implementation в small steps
4. Checkpoint + approval после каждого шага
5. File creation только с явным approval

## Быстрый старт

### Установка

```bash
# Клонирование репозитория
git clone https://github.com/semernyakov/ai-skill-system.git
cd ai-skill-system

# Установка git hooks (авто-синхронизация)
./.ai/scripts/install-hooks.sh

# Первичная синхронизация
./.ai/scripts/sync-all.sh
```

### Использование

#### Для Cursor

Правила автоматически загружаются из `.cursor/rules/` при открытии проекта.

#### Для Windsurf

Правила загружаются из `.windsurf/rules/` или `.windsurfrules`.

#### Для PyCharm

1. Settings → Tools → AI Assistant
2. Custom Instructions → Attach Context
3. Выбрать `.idea/ai-context.txt`

### MCP Gateway

MCP Gateway — централизованная точка входа для MCP сервисов.

#### Запуск Gateway

```bash
# Установка зависимостей
pip install fastapi uvicorn pydantic

# Запуск gateway
./.ai/scripts/start-mcp-gateway.sh
```

Gateway будет доступен на `http://localhost:8080`

#### Доступные сервисы

**Filesystem Service:**
- `POST /mcp/filesystem/invoke` — операции с файлами
  - `read_file` — чтение файла
  - `write_file` — запись файла
  - `list_dir` — список директории
  - `delete_file` — удаление файла

**API Endpoints:**
- `GET /mcp/services` — список сервисов
- `GET /mcp/health/{service_name}` — проверка здоровья
- `GET /mcp/{service_name}/capabilities` — возможности сервиса

Подробнее: см. `MCP_GATEWAY.md`

### Редактирование правил

**ВАЖНО:** Редактируйте только файлы в `.ai/rules/`!

После изменений:

```bash
# Синхронизация с IDE
./.ai/scripts/sync-all.sh

# Git add и commit (hook автоматически запустит sync)
git add .
git commit -m "Update rules"
```

### Создание нового skill

```bash
# Используйте SKILL_CREATOR.md как гайд
# Создайте SKILL.md в директории вашего проекта
```

### Запуск evaluation

```bash
# Подготовка workspace
mkdir -p evals/workspace/iteration-1/runs

# Запуск eval
python .ai/scripts/run_eval.py evals.json evals/workspace/iteration-1

# Агрегация бенчмарков
python .ai/scripts/aggregate_benchmark.py evals/workspace/iteration-1 --skill-name my-skill
```

## Ключевые концепции

### Token Economy

- Отвечать ТОЛЬКО на заданный вопрос
- Генерировать ТОЛЬКО diff/changed блоки
- Использовать `# ... existing ...` для неизмененного кода
- Пропускать docstrings кроме public API
- Inline comments только для неочевидной логики

### Pushy Descriptions

Описания skills должны быть assertive, а не passive:

**Плохо:**
```yaml
description: How to build a simple fast dashboard
```

**Хорошо:**
```yaml
description: >
  How to build a simple fast dashboard to display data.
  Use this skill whenever the user mentions dashboards, 
  data visualization, internal metrics, or wants to display 
  any kind of company data, even if they don't explicitly 
  ask for a 'dashboard.'
```

### Field Naming (Assertion Results)

Используйте точные имена полей для совместимости с viewer:

```json
{
  "text": "Output is valid JSON",
  "passed": true,
  "evidence": "Parsed 5 keys successfully"
}
```

## Troubleshooting

### Правила не синхронизируются

```bash
# Ручная синхронизация
./.ai/scripts/sync-all.sh

# Проверка .ai/ директории
ls -la .ai/
```

### Git hooks не работают

```bash
# Переустановка hooks
./.ai/scripts/install-hooks.sh

# Проверка hook файла
cat .git/hooks/pre-commit
```

### Evaluation не запускается

```bash
# Проверка Python зависимостей
python3 --version

# Проверка eval schema
python3 -m json.tool .ai/skills/schemas/eval_schema.json
```

### Markdown linting не работает

Markdown linting настроен в `.pre-commit-config.yaml` (markdownlint), но не активен из-за отсутствия зависимостей.

**Для активации требуется одна из опций:**

**Вариант A:** Установить pre-commit framework
```bash
pip install pre-commit
pre-commit install
```

**Вариант B:** Установить markdownlint-cli
```bash
npm install -g markdownlint-cli
```

Без установки этих зависимостей markdown linting не будет работать. Конфигурация готова, но требует хотя бы одной зависимости для активации.

## Дополнительные ресурсы

- **TEAM.md** — Team protocol и роли
- **CONTRIBUTING.md** — Инструкции для контрибьюторов
- **CODE_OF_CONDUCT.md** — Кодекс поведения
- **SECURITY.md** — Политика безопасности
- **SUPPORT.md** — Поддержка и FAQ
- **DISCLAIMER.md** — Отказ от ответственности
- **CHANGELOG.md** — История изменений

## Лицензия

MIT License — см. LICENSE.md

## Контакты

- Email: i.s.semernyakov@yandex.ru
- GitHub: https://github.com/semernyakov/ai-skill-system
