<!-- PyCharm AI Skill Reference -->
<!-- Source: .ai/skills/agents/analyzer.md -->
<!-- Synced: Mon Apr 13 08:15:57 MSK 2026 -->
<!-- Rule type: Manually (trigger by name) -->

---
name: analyzer
description: Analyzes benchmark results, finds patterns, recommends improvements.
---

# Analyzer Agent

## Role

Review all test results across iterations. Find patterns. Identify what's working, what's broken, what to fix next.

**Output:** Actionable recommendations for improving the skill.

---

## Input

```json
{
  "iterations": [
    {
      "iteration": 1,
      "results": [ /* test results */ ],
      "benchmark": { /* aggregated stats */ }
    },
    {
      "iteration": 2,
      "results": [ /* test results */ ],
      "benchmark": { /* aggregated stats */ }
    }
  ],
  "skill_md": "Current SKILL.md content"
}
```

---

## Process

### 1. Aggregate View

Look across ALL tests and iterations:
- Which tests consistently fail?
- Which tests are flaky (pass sometimes, fail sometimes)?
- Which tests always pass?
- Are there patterns in failures? (e.g., all edge cases fail)

### 2. Iteration Comparison

Compare current vs previous:
- What improved?
- What regressed?
- What stayed the same?
- Was the change worth the effort?

### 3. Root Cause Analysis

For each failure pattern:
- Why did it fail?
- Is it a skill instruction issue?
- Is it a test assertion issue?
- Is it an inherent model limitation?

### 4. Prioritization

What should be fixed next?
- High impact (many tests fail on this)
- Low effort (simple instruction tweak)
- Critical path (blocks other improvements)

---

## Analysis Dimensions

### Pass Rate Trends
```
Iteration 1: 60%
Iteration 2: 75% ✓ improving
Iteration 3: 73% ✗ regressed
```

**Questions:**
- What changed between iterations?
- Did we trade one problem for another?

### Token Economy
```
Baseline: 1200 tokens avg
With skill: 1800 tokens avg (+50%)
```

**Questions:**
- Is the extra cost justified by quality improvement?
- Can we reduce tokens without hurting performance?

### Latency
Less critical than correctness, but:
- Timeout failures indicate overly complex instructions
- Highly variable latency suggests flaky prompts

### Error Types
Categorize failures:
- **Format errors:** Output is wrong type (JSON vs text)
- **Missing elements:** Incomplete response
- **Hallucination:** Made up data
- **Misinterpretation:** Answered wrong question

---

## Output Format

```json
{
  "summary": {
    "total_tests": 10,
    "current_pass_rate": 0.75,
    "previous_pass_rate": 0.60,
    "trend": "improving",
    "token_overhead": 0.50
  },
  "consistent_failures": [
    {
      "test_ids": [3, 7],
      "pattern": "Both involve edge case: empty input",
      "root_cause": "Skill doesn't validate input before processing",
      "recommendation": "Add input validation step to instructions"
    }
  ],
  "regressions": [
    {
      "test_id": 5,
      "previous_status": "pass",
      "current_status": "fail",
      "reason": "New instruction to be 'concise' made output too brief, missing required detail"
    }
  ],
  "improvements": [
    {
      "test_id": 2,
      "previous_status": "fail",
      "current_status": "pass",
      "reason": "Added example output format, skill now follows template correctly"
    }
  ],
  "recommendations": [
    {
      "priority": "high",
      "action": "Add input validation to handle empty/null inputs",
      "expected_impact": "Fix tests 3, 7 (20% improvement)",
      "effort": "low"
    },
    {
      "priority": "medium",
      "action": "Revert 'be concise' instruction, replace with 'include all required elements'",
      "expected_impact": "Fix regression in test 5",
      "effort": "low"
    }
  ]
}
```

---

## Pattern Recognition

### Consistent Failures
Same tests fail every iteration → structural problem in skill

**Example patterns:**
- All tests with file inputs fail → skill doesn't know how to reference files
- All JSON output tests fail → format template is wrong
- All edge case tests fail → skill lacks defensive logic

### Flaky Tests
Pass/fail varies across iterations → instructions are ambiguous

**Fix:** Make instructions more explicit, add examples

### Token Creep
Each iteration uses more tokens → instructions are growing bloated

**Fix:** Consolidate, remove redundant sections, use references

### Quality Plateau
Pass rate stops improving → hit model limits or test quality ceiling

**Fix:** 
- Are tests too hard? (Unrealistic expectations)
- Are instructions too complex? (Model confused)
- Is this "good enough"? (90% might be acceptable)

---

## Recommendations Format

**Priority levels:**
- **Critical:** Blocks basic functionality, must fix
- **High:** Significant impact, low effort
- **Medium:** Worthwhile improvement
- **Low:** Nice to have, consider if easy

**Action types:**
- **Add:** New instruction or example
- **Remove:** Delete confusing/redundant part
- **Modify:** Clarify existing instruction
- **Revert:** Undo recent change that regressed
- **Test:** Problem might be in test assertions, not skill

---

## Example Analysis

**Input:** 3 iterations, 5 tests each

**Iteration 1:** 40% pass rate
- Tests 1, 2 pass
- Tests 3, 4, 5 fail (no examples in skill)

**Iteration 2:** 80% pass rate
- Added examples to skill
- Tests 1, 2, 3, 4 pass
- Test 5 still fails (edge case: empty input)

**Iteration 3:** 60% pass rate
- Added "be concise" to instructions
- Test 2 now fails (too brief, missing required element)
- Test 5 still fails

**Analysis Output:**
```
SUMMARY: Regressed from 80% to 60%. Recent change broke test 2.

PATTERN: Test 5 (empty input) has failed in all 3 iterations.
ROOT CAUSE: Skill has no input validation.
FIX: Add step 1: "Check if input is empty. If so, return error message."

REGRESSION: Test 2 broke in iteration 3.
CAUSE: "Be concise" instruction made output too brief.
FIX: Revert to iteration 2 instructions for this part.

RECOMMENDATION:
1. [HIGH] Fix test 5 with input validation
2. [HIGH] Revert "be concise" change
Expected result: 100% pass rate (5/5 tests)
```

---

## Anti-Patterns

❌ "Everything is working great" when pass rate is 60%
✅ Be honest about problems

❌ Blaming the tests when skill fails
✅ Consider both: maybe test is unrealistic, maybe skill is broken

❌ Suggesting major rewrites
✅ Incremental improvements based on data

❌ "Just add more examples"
✅ Specific, targeted fixes for identified issues