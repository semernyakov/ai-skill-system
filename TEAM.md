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

## TEAM architecture review mode (MVP-first)

Use this when the request is: "TEAM analyze architecture" (or similar).

### Expected output by role

1. **Dava (Frontend)**
   - Current frontend topology (routes, state, API adapters)
   - UX-critical bottlenecks affecting conversion
   - 3 concrete simplifications for MVP speed
2. **Manya (UX/Marketing)**
   - Funnel fit: entry → activation → first value
   - Copy and UX friction points
   - KPI impact assumptions (time-to-value, conversion)
3. **Sanya (Behavioral linguistics)**
   - Clarity and "human tone" audit for user-facing text
   - Risky/robotic phrasing + rewrite principles
4. **Kirill-QA (Security/Performance)**
   - P0/P1 security findings (auth, rate limits, secrets, CORS)
   - Performance risks (single points, sync calls, DB hotspots)
   - Compliance notes (RU 152-FZ / GDPR readiness)
5. **Ivan (Arbitr)**
   - Final decision: YES / NO / YES with constraints
   - Ordered execution plan for MVP only

### Architecture audit structure

- **Section A — As-is architecture (factual)**
- **Section B — Risks by severity (P0/P1/P2)**
- **Section C — MVP priorities (next 7-14 days)**
- **Section D — Deferred items (post-MVP)**
- **Section E — Explicit Arbitr decision**
