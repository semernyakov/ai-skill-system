#!/usr/bin/env python3
import json
import sys


def check(output: str) -> dict:
    try:
        data = json.loads(output)
        size = len(data) if isinstance(data, dict) else len(data) if isinstance(data, list) else 1
        return {"passed": True, "evidence": f"Valid JSON ({type(data).__name__}, size={size})"}
    except Exception as exc:
        return {"passed": False, "evidence": f"Invalid JSON: {exc}"}


if __name__ == "__main__":
    print(json.dumps(check(sys.stdin.read())))
