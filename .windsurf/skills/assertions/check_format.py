#!/usr/bin/env python3
import json
import sys


def check(output: str, expected: str = "markdown") -> dict:
    text = output.strip()
    fmt = expected.lower()

    if fmt == "json":
        try:
            json.loads(text)
            return {"passed": True, "evidence": "Output parses as JSON"}
        except Exception as exc:
            return {"passed": False, "evidence": f"JSON parse failed: {exc}"}

    if fmt == "markdown":
        has_markdown = any(token in text for token in ("#", "- ", "* ", "```"))
        return {"passed": has_markdown, "evidence": "Markdown markers found" if has_markdown else "No markdown markers found"}

    if fmt == "yaml":
        looks_yaml = ":" in text and "{" not in text
        return {"passed": looks_yaml, "evidence": "Looks like YAML" if looks_yaml else "Does not resemble YAML"}

    return {"passed": False, "evidence": f"Unsupported expected format: {expected}"}


if __name__ == "__main__":
    expected = sys.argv[1] if len(sys.argv) > 1 else "markdown"
    print(json.dumps(check(sys.stdin.read(), expected)))
