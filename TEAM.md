---
description: Team protocol and role handoff model.
globs: ["**/*"]
alwaysApply: true
priority: 0
---

# TEAM.md — Team Operating Model

## Core principle

Ivan (Arbitr) — the sole final decision-maker.
Vasya / Yosya / Bosya / Manya / Sanya / Kirill — expert roles for preparing options, implementation, and review.

## How TEAM.md integrates into the system

- `TEAM.md` defines the organizational layer: roles, handoff, approval flow.
- `.ai/rules/003-team-protocol.mdc` — machine-applicable version of this protocol for IDE/AI assistants.
- Other rules in `.ai/rules/*.mdc` describe technical standards (API, Docker, K8s, CI/CD).

Summary: `TEAM.md` = **who and how decisions are made**, `.ai/rules/*` = **how to do technical work**.

## Mandatory workflow

1. Proposal (options + risks + files)
2. Arbitr approval (YES / NO / YES with constraints)
3. Implementation in small steps
4. After each step — checkpoint + approval
5. File creation only with explicit Arbitr approval
