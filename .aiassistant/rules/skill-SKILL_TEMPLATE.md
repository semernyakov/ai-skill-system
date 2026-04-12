<!-- PyCharm AI Skill Reference -->
<!-- Source: .ai/skills/SKILL_TEMPLATE.md -->
<!-- Synced: Sun Apr 12 20:32:53 MSK 2026 -->
<!-- Rule type: Manually (trigger by name) -->

---
name: example-skill
description: >
  How to [specific outcome] for [user/job-to-be-done].
  Use this skill whenever the user mentions [domain keywords], [synonyms],
  or describes [implicit intent], even if they do not use exact terms.
  Trigger on phrases like "[phrase 1]", "[phrase 2]", "[phrase 3]".
  Do not wait for perfect wording; prefer activation over misses.
  Stay bounded by explicit non-trigger conditions below.
---

## Purpose

One sentence: what does this skill enable Claude to do?

## When to Use

Trigger conditions:
- User asks to [specific action]
- Query contains keywords: "X", "Y", "Z"
- Context suggests [specific scenario]

Do NOT trigger when:
- [Similar but different intent]
- [Out of scope scenarios]

## Instructions

Step-by-step, imperative style:

1. **Validate Input**
   - Check for required fields: X, Y, Z
   - If missing, ask user: "I need [specific info] to proceed"
   - Handle edge cases: empty input, malformed data

2. **Process**
   - Do [concrete action]
   - Use [specific format/tool]
   - Apply [specific logic]

   **Why this matters:** [brief context on intent]

3. **Generate Output**
   - Format as [json|markdown|svg|etc]
   - Include [required elements]
   - Structure like:
   ```
   [show exact template or example]
   ```

## Output Format

**Example output:**
```
[Paste exact example of good output]
```

**Required elements:**
- Element A: [purpose]
- Element B: [purpose]
- Element C: [purpose]

**Formatting rules:**
- Use [specific syntax]
- Avoid [anti-patterns]
- Prefer [best practice] because [reason]

## Edge Cases

Handle gracefully:
- **Empty input:** Return helpful error message
- **Invalid format:** Suggest correction
- **Missing dependencies:** Check for [X], fail fast if unavailable
- **Partial data:** Work with what's available, note limitations

## Token Optimization

- Load heavy references from `references/` only if needed
- Use cached prompts for repeated patterns
- Prefer structured outputs (JSON schema) over free text
- Stream long responses (>500 tokens)

## Examples

### Example 1: [Scenario]
**Input:** [realistic user query]
**Output:** [expected result]

### Example 2: [Edge case]
**Input:** [tricky query]
**Output:** [how to handle]

## References

External resources (loaded on-demand):
- `references/schema.json` — Data format specification
- `references/examples.md` — Additional examples
- `scripts/helper.py` — Executable utility (if deterministic logic)

## Styling with Tailwind CSS

All HTML templates in this project use Tailwind CSS for consistent styling.

### HTML Template Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        p0: '#ef4444',
                        p1: '#f59e0b',
                        p2: '#3b82f6',
                        p3: '#10b981',
                    }
                }
            }
        }
    </script>
</head>
<body class="bg-gray-100 font-sans">
    <!-- Your content using Tailwind utility classes -->
</body>
</html>
```

### Using Centralized CSS Components

Reference centralized components from `.ai/skills/styles/main.css`:
- `.report-container` - Main container
- `.report-header` - Gradient header
- `.severity-badge` - Severity indicators
- `.finding-card` - Finding cards with severity colors

### Severity Color System

- **P0 (Critical):** `text-red-500`, `bg-red-500`
- **P1 (High):** `text-amber-500`, `bg-amber-500`
- **P2 (Medium):** `text-blue-500`, `bg-blue-500`
- **P3 (Low):** `text-emerald-500`, `bg-emerald-500`

### Base Template

Use `.ai/skills/templates/base.html` as starting point for new HTML templates.

See `.ai/skills/templates/README.md` for complete styling documentation.

## Testing Assertions

When evaluating this skill, check:
- [ ] Output contains [required element]
- [ ] Format is valid [json|markdown|etc]
- [ ] No hallucinated data (only use provided context)
- [ ] Handles edge case: [specific scenario]
- [ ] Token usage ≤ [budget]

## Iteration Notes

**v1.0:** Initial version
**v1.1:** Added handling for [edge case] after test failures
**v1.2:** Optimized description for better triggering on [phrase type]

## Pushy description checklist

- Include direct trigger verbs ("use", "trigger", "apply")
- Include synonyms and implicit intents
- Include at least 3 realistic phrase examples
- Include explicit non-trigger cases
