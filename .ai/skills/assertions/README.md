# Programmatic Assertions

Use scripts in this folder to perform deterministic evaluation checks.

## Conventions

- Read model output from stdin.
- Print a JSON object with:
  - `passed` (boolean)
  - `evidence` (string)

## Available Scripts

- `check_json.py` — validates output parses as JSON.
- `check_format.py` — validates simple output format expectations (json/markdown/yaml).

## Example

```bash
cat output.txt | python .ai/skills/assertions/check_json.py
cat output.txt | python .ai/skills/assertions/check_format.py json
```
