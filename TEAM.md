---
description: Team protocol and role handoff model.
globs: ["**/*"]
alwaysApply: true
priority: 0
---

# TEAM.md — Team Operating Model

## Core principle

Иван (Arbitr) — единственный финальный decision-maker.
Vasya / Yosya / Manya / Sanya / Кирилл-QA — экспертные роли для подготовки вариантов, реализации и ревью.

## How TEAM.md integrates into the system

- `TEAM.md` задаёт организационный слой: роли, handoff, approval flow.
- `.ai/rules/003-team-protocol.mdc` — машинно-применяемая версия этого протокола для IDE/AI ассистентов.
- Остальные правила `.ai/rules/*.mdc` описывают технические стандарты (API, Docker, K8s, CI/CD).

Итого: `TEAM.md` = **кто и как принимает решения**, `.ai/rules/*` = **как делать техническую работу**.

## Mandatory workflow

1. Proposal (варианты + риски + файлы)
2. Arbitr approval (YES / NO / YES with constraints)
3. Implementation in small steps
4. After each step — checkpoint + approval
5. File creation only with explicit Arbitr approval
