# IDE Compatibility Guide

## Source of truth

- Rules: `.ai/rules/*.mdc`
- Skills: `.ai/skills/**`
- Sync: `.ai/scripts/sync-all.sh`

## Matrix

| Capability | Cursor | Windsurf | PyCharm AI |
|---|---|---|---|
| Native `.mdc` | ✅ | ✅ | ❌ |
| Skills support | ✅ | ✅ | ⚠️ via context |
| Auto-reload | ✅ | ✅ | ❌ |

## Setup notes

### Cursor
- Mirrors: `.cursor/rules/`, `.cursor/skills/`
- Verify: Command Palette → “Cursor: Show Rules”

### Windsurf
- Mirrors: `.windsurf/rules/` + `.windsurfrules`
- Verify: Settings → AI Rules

### PyCharm
- Attach `.idea/ai-context.txt` manually
- Re-attach after rule updates

## Team integration check

`TEAM.md` and `.ai/rules/003-team-protocol.mdc` must stay aligned.
