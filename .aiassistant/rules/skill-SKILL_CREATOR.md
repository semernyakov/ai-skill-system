<!-- PyCharm AI Skill Reference -->
<!-- Source: .ai/skills/SKILL_CREATOR.md -->
<!-- Synced: Sun Apr 12 20:31:06 MSK 2026 -->
<!-- Rule type: Manually (trigger by name) -->

---
name: skill-creator
description: >
  Creates, tests, and optimizes Claude skills for AI microservices.
  Use when the user wants to build a new skill, evaluate existing skills,
  or improve skill triggering accuracy. Handles the full lifecycle:
  requirements gathering, SKILL.md creation, test generation, 
  benchmarking, and iterative optimization.
---

# Skill Creator Agent

## Purpose

Build production-ready Claude skills with automated testing and optimization. Focus on token economy and accurate triggering.

---

## Workflow

### 1. Discovery Phase

Ask user:
- What should the skill enable Claude to do?
- When should it trigger? (example phrases)
- What output format is expected?
- Are test cases needed?

**Do NOT write code yet.** Gather complete requirements first.

### 2. Requirements Deep Dive

Explore:
- Edge cases and failure modes
- Input/output formats and examples
- Success criteria (what makes a good output?)
- Token budget constraints

### 3. Create SKILL.md

Structure:
```markdown
---
name: skill-name
description: >
  Concise description for triggering logic.
  Include when to use: "Use when user asks to...", 
  "Trigger on phrases like...", etc.
  Aim for 80-120 words. Balance precision vs coverage.
---

## Instructions

Imperative style: "Do this", "Check that", "Use X format".
Concrete examples over abstract rules.
Explain WHY when non-obvious.

## Output Format

Show exact template or example output.
Claude copies patterns better than interpreting descriptions.

## Edge Cases

Handle: empty inputs, missing data, API failures, etc.
```

**Token Economy Rules:**
- Metadata (name + description): ~100 words max
- Main body: ideally < 500 lines
- External resources (scripts/, references/): no limit

### 4. Generate Test Cases

Create `evals/evals.json`:
```json
{
  "skill_name": "my-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "Realistic user request that should trigger skill",
      "assertions": [
        {
          "type": "contains",
          "value": "expected substring in output"
        },
        {
          "type": "format",
          "value": "json|markdown|svg|etc"
        }
      ],
      "files": []
    }
  ]
}
```

**Test Quality:**
- 2-5 realistic prompts (what real users actually type)
- Include: typos, slang, implicit requests, edge cases
- Each test gets assertions (checkable claims about output)

### 5. Run Evaluation

Execute two parallel sub-agents per test:
- **with-skill**: Uses the new skill
- **baseline**: No skill (or old version)

Isolated contexts. No cross-contamination.

Save results to `evals/results/{iteration}/`

### 6. Grading

For each test output:
- Check each assertion: pass/fail + evidence
- Aggregate: pass rate, tokens used, latency
- Compare with-skill vs baseline

Schema:
```json
{
  "test_id": 1,
  "with_skill": {
    "output": "...",
    "assertions": [
      {"text": "...", "passed": true, "evidence": "..."}
    ],
    "tokens": 1234,
    "latency_ms": 567
  },
  "baseline": { /* same structure */ }
}
```

### 7. Analysis

Agent reviews all test results and identifies:
- Consistent failures (same tests fail across iterations)
- Where new version regressed
- Where new version improved
- What to prioritize next

Output: actionable recommendations for next iteration.

### 8. Iteration Loop

User provides feedback. If empty → done. If not:
1. Update SKILL.md based on feedback
2. Re-run all tests (new iteration folder)
3. Compare with previous iteration
4. Analyze diffs
5. Get feedback → repeat

---


## Programmatic Assertions (Preferred)

When an assertion can be checked with code, use a script in `.ai/skills/assertions/` and execute it against output.

Examples:
- JSON validity checks
- Length/format checks
- Structural checks

Prefer script-based grading over subjective LLM-only checks for speed and determinism.

## Description Optimization

The `description` field is CRITICAL. It controls skill triggering.

**Two error types:**
- False negative: skill didn't trigger when it should → user doesn't get help
- False positive: skill triggered incorrectly → wasted context

**Strategy: Be "pushy"**
Better to trigger extra than miss. User can ignore irrelevant activations, but can't invoke what didn't activate.

**Automated Optimization:**
1. Generate 20 test queries:
   - 10 SHOULD trigger (varied phrasing, typos, implicit)
   - 10 SHOULD NOT trigger (similar but different intent)
2. Test current description
3. Adjust based on false positives/negatives
4. Repeat until accuracy threshold met (e.g., 90%+)

---

## File Structure

```
my-skill/
├── SKILL.md              # Main skill definition
├── scripts/              # Executable code (optional)
├── references/           # External docs loaded on-demand
├── assets/               # Templates, icons, fonts
└── evals/
    ├── evals.json        # Test definitions
    └── results/
        ├── iteration-1/  # First run
        ├── iteration-2/  # After changes
        └── ...
```

---

## Output to User

After each evaluation:
1. Open results in viewer (HTML report)
2. Show pass rates: with-skill vs baseline
3. Highlight regressions and improvements
4. Wait for feedback

**Feedback format:**
- Empty = satisfied, stop iterating
- Specific issues = incorporate into next iteration

---

## Example Session

**User:** "Create a skill for generating API documentation from OpenAPI specs"

**Skill Creator:**
1. "What format for output? Markdown, HTML, or custom?"
2. "Should it handle YAML and JSON specs?"
3. "Any specific sections to emphasize? (auth, rate limits, etc.)"

[After gathering requirements]

4. Creates `SKILL.md` with clear triggering description
5. Generates 3 test cases with realistic OpenAPI specs
6. Runs evaluation
7. Shows results: "With skill: 100% pass rate. Baseline: 33% (missing auth docs)"
8. Waits for feedback
9. User: "Add examples to each endpoint"
10. Updates skill, re-runs tests, shows diff

---

## Critical Principles

- **Token first**: Every word in SKILL.md costs context
- **Concrete over abstract**: Show examples, not rules
- **Test realistic inputs**: What users actually type, not idealized prompts
- **Iterate based on data**: Benchmark-driven improvements
- **Pushy descriptions**: Better false positive than false negative

---

## Anti-Patterns

❌ Vague descriptions: "Helps with documentation"
✅ Specific: "Generates API docs from OpenAPI/Swagger YAML/JSON specs. Trigger on: 'document my API', 'create API reference', 'OpenAPI to markdown'"

❌ Abstract instructions: "Maintain code quality"
✅ Concrete: "Run `make lint`. All tests in tests/ must pass."

❌ Over-constrained: "MUST use exactly 3 paragraphs, 150 words, formal tone"
✅ Flexible: "Clear, concise explanation. Show code examples where helpful."

❌ Test prompts: "Generate documentation for the following spec:"
✅ Realistic: "hey can you make docs for my api? here's the swagger file"

---

## Success Metrics

- Pass rate ≥ 90% on realistic tests
- Token usage ≤ baseline + 20% (skill shouldn't bloat context)
- False negative rate < 5% (catches intended use cases)
- User satisfaction (feedback loop converges to empty)

---

## Integration with AI Microservices

Skills live in `.cursor/skills/` or `src/skills/` depending on usage:
- Cursor IDE skills → `.cursor/skills/`
- Runtime agent skills → `src/skills/`

Both follow same SKILL.md format. Evaluation framework works for both.