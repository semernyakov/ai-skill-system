#!/usr/bin/env python3
import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path


def run_test(test_case: dict, workspace: Path, with_skill: bool) -> dict:
    run_name = f"test-{test_case['id']}-{'with-skill' if with_skill else 'baseline'}"
    out_dir = workspace / "runs" / run_name
    out_dir.mkdir(parents=True, exist_ok=True)

    started = time.perf_counter()
    output = f"Simulated {'with skill' if with_skill else 'baseline'} output for test {test_case['id']}"
    latency_ms = int((time.perf_counter() - started) * 1000)

    assertions = []
    for a in test_case.get("assertions", []):
        text = a.get("description") or f"Assertion {a.get('type')}"
        passed = bool(a.get("value"))
        assertions.append({"text": text, "passed": passed, "evidence": "Simulated grading result"})

    passed = all(a["passed"] for a in assertions) if assertions else True
    record = {
        "output": output,
        "assertions": assertions,
        "tokens": len(output.split()),
        "latency_ms": latency_ms,
        "passed": passed,
    }

    (out_dir / "output.txt").write_text(output + "\n")
    (out_dir / "result.json").write_text(json.dumps(record, indent=2) + "\n")
    return record


def main():
    parser = argparse.ArgumentParser(description="Run eval cases into workspace iteration structure")
    parser.add_argument("evals_file", type=Path)
    parser.add_argument("workspace", type=Path)
    args = parser.parse_args()

    data = json.loads(args.evals_file.read_text())
    args.workspace.mkdir(parents=True, exist_ok=True)
    (args.workspace / "runs").mkdir(exist_ok=True)

    grading = []
    for test_case in data.get("evals", []):
        ws = run_test(test_case, args.workspace, with_skill=True)
        bs = run_test(test_case, args.workspace, with_skill=False)
        metadata = {
            "test_id": test_case["id"],
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "with_skill": ws,
            "baseline": bs,
        }
        run_dir = args.workspace / "runs" / f"test-{test_case['id']}"
        run_dir.mkdir(exist_ok=True)
        (run_dir / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
        grading.append(metadata)

    (args.workspace / "grading.json").write_text(json.dumps(grading, indent=2) + "\n")
    print(f"Wrote {args.workspace / 'grading.json'}")


if __name__ == "__main__":
    main()
