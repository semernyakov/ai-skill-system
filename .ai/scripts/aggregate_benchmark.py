#!/usr/bin/env python3
import argparse
import json
import statistics
from datetime import datetime, timezone
from pathlib import Path


def _safe_mean(values):
    return float(statistics.mean(values)) if values else 0.0


def _safe_std(values):
    return float(statistics.stdev(values)) if len(values) > 1 else 0.0


def summarize(results):
    total = len(results)
    passed = sum(1 for r in results if r.get("passed"))
    tokens = [r.get("tokens", 0) for r in results]
    times = [r.get("latency_ms", 0) for r in results]
    return {
        "pass_rate": (passed / total) if total else 0.0,
        "avg_tokens": _safe_mean(tokens),
        "avg_time_ms": _safe_mean(times),
        "stddev_tokens": _safe_std(tokens),
        "stddev_time_ms": _safe_std(times),
        "total_tests": total,
        "passed_tests": passed,
    }


def load_runs(runs_dir: Path):
    with_skill, baseline = [], []
    for run_dir in sorted(p for p in runs_dir.iterdir() if p.is_dir()):
        meta_file = run_dir / "metadata.json"
        if not meta_file.exists():
            continue
        data = json.loads(meta_file.read_text())
        if "with_skill" in data:
            with_skill.append(data["with_skill"])
        if "baseline" in data:
            baseline.append(data["baseline"])
    return with_skill, baseline


def main():
    parser = argparse.ArgumentParser(description="Aggregate benchmark metrics from workspace runs")
    parser.add_argument("workspace", type=Path, help="Path to iteration workspace")
    parser.add_argument("--skill-name", required=True)
    parser.add_argument("--iteration", type=int, default=1)
    args = parser.parse_args()

    runs_dir = args.workspace / "runs"
    with_skill_runs, baseline_runs = load_runs(runs_dir)

    ws = summarize(with_skill_runs)
    bs = summarize(baseline_runs)

    benchmark = {
        "skill_name": args.skill_name,
        "iteration": args.iteration,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "with_skill": ws,
        "baseline": bs,
        "delta": {
            "pass_rate": f"{ws['pass_rate'] - bs['pass_rate']:+.2f}",
            "tokens": f"{ws['avg_tokens'] - bs['avg_tokens']:+.0f}",
            "time_ms": f"{ws['avg_time_ms'] - bs['avg_time_ms']:+.0f}",
        },
    }

    out_file = args.workspace / "benchmark.json"
    out_file.write_text(json.dumps(benchmark, indent=2) + "\n")
    print(f"Wrote {out_file}")


if __name__ == "__main__":
    main()
