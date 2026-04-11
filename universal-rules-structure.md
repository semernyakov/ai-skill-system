# Universal Rules Structure

## Canonical structure

```text
.ai/
├── rules/
│   ├── 000-core.mdc
│   ├── 001-agentic.mdc
│   ├── 002-docker.mdc
│   ├── 003-k8s.mdc
│   ├── 003-team-protocol.mdc
│   ├── 004-cicd.mdc
│   └── 005-api.mdc
├── skills/
└── scripts/
```

## Layering model

1. `000-core.mdc` (global constraints)
2. `003-team-protocol.mdc` (workflow and approvals)
3. Domain rules (agentic/docker/k8s/cicd/api)

## Distribution

- Cursor: `.cursor/rules`, `.cursor/skills`
- Windsurf: `.windsurf/rules`, `.windsurfrules`
- PyCharm: `.idea/ai-context.txt`

Run `.ai/scripts/sync-all.sh` after rule changes.
