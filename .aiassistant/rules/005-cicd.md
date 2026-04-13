<!-- PyCharm AI Project Rule -->
<!-- Source: .ai/rules/005-cicd.mdc -->
<!-- Synced: Mon Apr 13 08:40:58 MSK 2026 -->
<!-- Rule type: Always (apply to all files) -->

---
description: GitHub Actions CI/CD patterns for AI microservices.
globs: ["**/.github/workflows/*.yml", "**/.github/workflows/*.yaml"]
alwaysApply: false
---

# CI/CD — GITHUB ACTIONS

## Pipeline Structure (mandatory order)
1. `lint` — ruff + mypy (fail fast)
2. `test` — pytest with coverage ≥ 80%
3. `build` — Docker build + push to registry
4. `deploy` — kubectl apply / helm upgrade

## Reusable Workflow Template
```yaml
name: CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/ruff-action@v1
      - run: mypy app/ --ignore-missing-imports

  test:
    needs: lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install uv && uv sync
      - run: pytest tests/ --cov=app --cov-fail-under=80

  build:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    outputs:
      image-tag: ${{ steps.meta.outputs.tags }}
    steps:
      - uses: actions/checkout@v4
      - uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=sha,prefix=,suffix=,format=short
      - uses: docker/build-push-action@v5
        with:
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: azure/k8s-set-context@v3
        with:
          kubeconfig: ${{ secrets.KUBECONFIG }}
      - run: |
          helm upgrade --install ${{ env.IMAGE_NAME }} ./helm \
            --set image.tag=${{ needs.build.outputs.image-tag }} \
            --namespace production \
            --wait
```

## Rules
- Cache Docker layers with `cache-from: type=gha`
- Use `GITHUB_TOKEN` for GHCR — no personal tokens
- Secrets: only in GitHub Environments, not repo-level for production
- Matrix strategy for multi-service monorepo: `matrix.service: [agent-a, agent-b]`
