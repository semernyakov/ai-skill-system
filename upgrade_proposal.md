# AI Skill System — Upgrade Proposal

Based on official Anthropic Skill Creator  
Date: 2026-04-11

---

## Current System Analysis

### ✅ What We Have (Strong)
- Universal IDE support (Cursor, Windsurf, PyCharm)
- Team protocol with role-based workflows
- Basic skill structure (SKILL.md, agents, schemas)
- Token economy focus
- Core rules for Python, FastAPI, AI/ML

### ⚠️ Gaps vs. Anthropic Official

| Feature | Our System | Anthropic Official | Priority |
|---------|-----------|-------------------|----------|
| **Evaluation Framework** | Basic schema | Full eval runner + grading | 🔴 HIGH |
| **Benchmark Aggregation** | Missing | Python scripts | 🔴 HIGH |
| **HTML Viewer** | Missing | eval-viewer/ | 🟡 MEDIUM |
| **Description Optimizer** | Basic guidance | Auto-optimization loop | 🟡 MEDIUM |
| **Grader Agent** | Conceptual | Concrete implementation | 🔴 HIGH |
| **Programmatic Assertions** | Missing | Script-based checks | 🔴 HIGH |
| **Iteration Tracking** | Missing | Workspace structure | 🟡 MEDIUM |
| **Variance Analysis** | Missing | Mean ± stddev reporting | 🟢 LOW |

---

## Key Findings from Anthropic Skill Creator

### 1. **"Pushy" Descriptions** (Critical!)
Anthropic recommends making skill descriptions assertive rather than passive, explicitly listing trigger conditions to reduce false negatives

**Before:**
```yaml
description: How to build a simple fast dashboard
```

**After (Anthropic style):**
```yaml
description: >
  How to build a simple fast dashboard to display data.
  Use this skill whenever the user mentions dashboards, 
  data visualization, internal metrics, or wants to display 
  any kind of company data, even if they don't explicitly 
  ask for a 'dashboard.'
```

**Action:** Update SKILL_TEMPLATE.md with pushy description examples

---

### 2. **Programmatic Assertions** (Game Changer)
For assertions that can be checked programmatically, Anthropic recommends writing and running scripts rather than manual inspection

**Current approach:**
```json
{
  "type": "contains",
  "value": "expected text"
}
```

**Anthropic approach:**
```python
# evals/assertions/check_json_valid.py
import json
import sys

def check(output: str) -> dict:
    try:
        data = json.loads(output)
        return {
            "passed": True,
            "evidence": f"Valid JSON with {len(data)} keys"
        }
    except json.JSONDecodeError as e:
        return {
            "passed": False,
            "evidence": f"Invalid JSON: {e}"
        }

if __name__ == "__main__":
    result = check(sys.stdin.read())
    print(json.dumps(result))
```

**Benefits:**
- Faster than LLM grading
- Deterministic (no variance)
- Reusable across iterations

**Action:** Add `evals/assertions/` directory with script examples

---

### 3. **Iteration Workspace Structure** (Essential)
Anthropic uses structured workspace directories to track iterations and enable comparison

**Recommended structure:**
```
workspace/
├── iteration-1/
│   ├── runs/
│   │   ├── test-1-with-skill/
│   │   │   ├── output.txt
│   │   │   └── metadata.json
│   │   ├── test-1-baseline/
│   │   └── test-2-with-skill/
│   ├── grading.json          # Per-test results
│   └── benchmark.json        # Aggregated stats
├── iteration-2/
│   ├── runs/
│   ├── grading.json
│   └── benchmark.json
└── comparison.json           # Iteration diffs
```

**Why:**
- Clear version history
- Easy rollback
- Enables `--previous-workspace` comparisons

**Action:** Update eval schema to support workspace structure

---

### 4. **Field Name Standardization** (Breaking!)
The grading.json expectations array must use exact field names: text, passed, and evidence—the viewer depends on these specific names

**Current (wrong):**
```json
{
  "claim": "Output is valid JSON",
  "passed": true,
  "evidence": "..."
}
```

**Anthropic standard (correct):**
```json
{
  "text": "Output is valid JSON",
  "passed": true,
  "evidence": "..."
}
```

**Action:** 
- Update `eval_schema.json`
- Update `grader.md`
- **BREAKING CHANGE** — document migration

---

### 5. **Aggregate Benchmark Script** (Must-have)
Anthropic provides scripts to aggregate results into benchmark.json with pass_rate, time, tokens, including mean ± stddev and deltas

**Output format:**
```json
{
  "iteration": 2,
  "timestamp": "2026-04-11T10:30:00Z",
  "with_skill": {
    "pass_rate": 0.85,
    "avg_tokens": 1234,
    "avg_time_ms": 567,
    "stddev_tokens": 123,
    "stddev_time_ms": 45
  },
  "baseline": {
    "pass_rate": 0.60,
    "avg_tokens": 1100,
    "avg_time_ms": 500
  },
  "delta": {
    "pass_rate": "+0.25",
    "tokens": "+134",
    "time_ms": "+67"
  }
}
```

**Action:** Create `scripts/aggregate_benchmark.py`

---

### 6. **HTML Viewer** (Nice-to-have)
Anthropic provides an eval-viewer that generates interactive HTML to browse outputs and benchmarks

**Features:**
- Side-by-side output comparison
- Filter by pass/fail
- Iteration timeline
- Variance charts

**Implementation:**
```python
# eval-viewer/generate_review.py
python generate_review.py \
  workspace/iteration-2 \
  --skill-name "my-skill" \
  --benchmark workspace/iteration-2/benchmark.json \
  --previous-workspace workspace/iteration-1
```

**Action:** Low priority — can use CLI output for MVP

---

### 7. **User Adaptation** (UX)
Skill Creator adapts language complexity based on user's technical level, avoiding jargon like "JSON" or "assertion" without context cues

**Guidelines:**
- "evaluation" and "benchmark" — borderline, OK
- "JSON" and "assertion" — need context cues
- Explain terms briefly if in doubt

**Action:** Add to team protocol (Maya/Alex roles)

---

## Recommended Upgrades (Prioritized)

### Phase 1: Critical Fixes (Week 1)

#### 1.1 Fix Field Names (Breaking)
```bash
# Update schemas
sed -i 's/"claim":/"text":/g' .ai/skills/schemas/eval_schema.json
sed -i 's/claim/text/g' .ai/skills/agents/grader.md
```

**Files affected:**
- `.ai/skills/schemas/eval_schema.json`
- `.ai/skills/agents/grader.md`

---

#### 1.2 Add Programmatic Assertions
```
.ai/skills/
└── assertions/
    ├── __init__.py
    ├── check_json_valid.py
    ├── check_format.py
    ├── check_length.py
    └── README.md
```

**Example assertion:**
```python
# assertions/check_json_valid.py
import json
import sys

def check(output: str) -> dict:
    try:
        json.loads(output)
        return {"passed": True, "evidence": "Valid JSON"}
    except Exception as e:
        return {"passed": False, "evidence": str(e)}

if __name__ == "__main__":
    print(json.dumps(check(sys.stdin.read())))
```

---

#### 1.3 Add Workspace Structure
```
# Create workspace template
mkdir -p evals/workspace/iteration-1/{runs,grading,benchmark}

# Update eval schema to support workspace
```

---

### Phase 2: Core Scripts (Week 2)

#### 2.1 Aggregate Benchmark Script
```python
# scripts/aggregate_benchmark.py
import json
from pathlib import Path
import statistics

def aggregate(workspace: Path, skill_name: str):
    results = []
    for run_dir in (workspace / "runs").iterdir():
        with open(run_dir / "metadata.json") as f:
            results.append(json.load(f))
    
    # Calculate stats
    pass_rate = sum(r["passed"] for r in results) / len(results)
    avg_tokens = statistics.mean(r["tokens"] for r in results)
    stddev_tokens = statistics.stdev(r["tokens"] for r in results)
    
    # ... (see full implementation below)
```

---

#### 2.2 Run Eval Script
```python
# scripts/run_eval.py
import subprocess
import json
from pathlib import Path

def run_test(test_case, workspace, with_skill=True):
    """Run single test case in isolated context"""
    output_dir = workspace / f"test-{test_case['id']}-{'with-skill' if with_skill else 'baseline'}"
    output_dir.mkdir(parents=True)
    
    # Execute test via subprocess
    # Save output, metadata, timing
    # Return result
```

---

### Phase 3: Enhancements (Week 3+)

#### 3.1 Description Optimizer Loop
```python
# scripts/improve_description.py
# Uses LLM to optimize description for better triggering
```

#### 3.2 HTML Viewer (optional)
```python
# eval-viewer/generate_review.py
# Static HTML generation for headless environments
```

#### 3.3 Variance Analysis Agent
```python
# Update analyzer.md to include stddev analysis
```

---

## Proposed New File Structure

```
ai-skill-system/
├── .ai/
│   ├── rules/
│   ├── skills/
│   │   ├── agents/
│   │   │   ├── analyzer.md         ← UPDATE (variance)
│   │   │   ├── comparator.md       
│   │   │   └── grader.md           ← UPDATE (field names)
│   │   ├── assertions/             ← NEW
│   │   │   ├── check_json.py
│   │   │   ├── check_format.py
│   │   │   └── README.md
│   │   ├── schemas/
│   │   │   └── eval_schema.json    ← UPDATE (field names)
│   │   ├── SKILL_CREATOR.md        ← UPDATE (pushy descriptions)
│   │   └── SKILL_TEMPLATE.md       ← UPDATE
│   ├── scripts/
│   │   ├── aggregate_benchmark.py  ← NEW
│   │   ├── run_eval.py             ← NEW
│   │   ├── improve_description.py  ← NEW (optional)
│   │   └── sync-all.sh
│   └── prompts/
├── evals/
│   └── workspace/                  ← NEW
│       ├── iteration-1/
│       ├── iteration-2/
│       └── template/
└── [existing files]
```

---

## Migration Path

### Step 1: Backup
```bash
git commit -am "Pre-upgrade checkpoint"
git tag v1.0-pre-anthropic
```

### Step 2: Breaking Changes
```bash
# Fix field names
./ai/scripts/migrate-field-names.sh

# Update all skills using old schema
find . -name "evals.json" -exec sed -i 's/"claim":/"text":/g' {} \;
```

### Step 3: Add New Features
```bash
# Copy new scripts
cp -r new-scripts/* .ai/scripts/

# Create assertions directory
mkdir -p .ai/skills/assertions
```

### Step 4: Test
```bash
# Run validation
python .ai/scripts/quick_validate.py

# Test aggregate script
python .ai/scripts/aggregate_benchmark.py evals/workspace/iteration-1 --skill-name test
```

---

## Compatibility Notes

### Backwards Compatibility
- ❌ **eval_schema.json** — BREAKING (field rename)
- ✅ **SKILL.md structure** — Compatible
- ✅ **Team protocol** — Compatible
- ✅ **IDE configs** — Compatible

### Forward Compatibility
- All new features are additive
- Old skills work with new system (after field migration)
- Workspace structure optional (gradual adoption)

---

## Success Metrics

### Before Upgrade
- Manual evaluation
- No iteration tracking
- Qualitative feedback only
- ~60% confidence in skill quality

### After Upgrade
- Automated evaluation with scripts
- Full iteration history
- Quantitative benchmarks (pass rate, tokens, time)
- ~90% confidence (data-driven)

---

## Decision Required

**Arbitr**: Which phase should we implement?

**Options:**
- **A)** Phase 1 only (critical fixes, ~1 day)
- **B)** Phase 1 + 2 (critical + scripts, ~3 days)
- **C)** Full upgrade (all phases, ~1 week)

**Recommendation:** **Option B** — Critical fixes + core scripts give 80% of value with 30% of effort.

**Files to create (Phase 1 + 2):**
- `.ai/skills/assertions/check_json.py`
- `.ai/skills/assertions/check_format.py`
- `.ai/skills/assertions/README.md`
- `.ai/scripts/aggregate_benchmark.py`
- `.ai/scripts/run_eval.py`
- `.ai/scripts/migrate-field-names.sh`
- `evals/workspace/template/` (directory structure)

**Files to modify:**
- `.ai/skills/schemas/eval_schema.json` (field rename)
- `.ai/skills/agents/grader.md` (field rename)
- `.ai/skills/SKILL_CREATOR.md` (pushy descriptions)
- `.ai/skills/SKILL_TEMPLATE.md` (examples)

**Request:** Permission to proceed with Option B?