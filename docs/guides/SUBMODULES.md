# Submodules Guide

This guide explains how to work with Git submodules in the AI Skill System.

## Overview

Git submodules allow this project to include external repositories while keeping them as separate Git repositories. This is useful for integrating third-party libraries, shared components, or external resources.

## Current Submodules

The project currently uses one submodule:

### agentskills

- **Path:** `external/agentskills`
- **Repository:** https://github.com/agentskills/agentskills.git
- **Purpose:** External skill library and reference implementations

## Initial Setup

### Cloning with Submodules

When cloning the repository for the first time, use the `--recursive` flag:

```bash
git clone --recursive https://github.com/semernyakov/ai-skill-system.git
```

### Initializing Existing Clone

If you already cloned without `--recursive`, initialize submodules:

```bash
cd ai-skill-system
git submodule update --init --recursive
```

## Common Operations

### Updating Submodules

To update all submodules to their latest commits:

```bash
git submodule update --remote
```

To update a specific submodule:

```bash
cd external/agentskills
git pull origin main
cd ../..
git add external/agentskills
git commit -m "Update agentskills submodule"
```

### Checking Submodule Status

```bash
git submodule status
```

Output shows:
- Commit hash of submodule
- Branch name (if detached)
- Status indicators:
  - ` ` (space): submodule is at correct commit
  - `+`: submodule has new commits
  - `-`: submodule is not initialized

### Navigating to Submodule

```bash
cd external/agentskills
```

### Checking Out Specific Branch

To work on a specific branch in a submodule:

```bash
cd external/agentskills
git checkout main
```

## Workflow

### Making Changes to Submodule

If you need to modify the submodule:

1. Navigate to submodule directory:
   ```bash
   cd external/agentskills
   ```

2. Make your changes and commit:
   ```bash
   git add .
   git commit -m "Your changes"
   ```

3. Push to the submodule's repository:
   ```bash
   git push origin main
   ```

4. Update the parent project to reference the new commit:
   ```bash
   cd ../..
   git add external/agentskills
   git commit -m "Update agentskills to latest commit"
   ```

### Removing a Submodule

To remove a submodule completely:

```bash
# 1. Remove from .gitmodules
git config -f .gitmodules --remove-section submodule.external/agentskills
git add .gitmodules

# 2. Remove from git index
git rm --cached external/agentskills

# 3. Remove files
rm -rf external/agentskills
git commit -m "Remove agentskills submodule"
```

## Troubleshooting

### Submodule Directory is Empty

If the submodule directory exists but is empty:

```bash
git submodule update --init --recursive
```

### Detached HEAD State

Submodules are typically in detached HEAD state. This is normal. To work on a specific branch:

```bash
cd external/agentskills
git checkout main
```

### Submodule Shows as Modified

If the submodule shows as modified but you haven't changed it:

```bash
# Check what changed
cd external/agentskills
git status

# Reset to expected commit
git checkout <expected-commit-hash>
```

## Adding a New Submodule

To add a new submodule:

```bash
git submodule add https://github.com/user/repo.git external/new-submodule
git commit -m "Add new-submodule"
```

## CI/CD Considerations

When setting up CI/CD pipelines, ensure:

1. Clone with `--recursive` flag
2. Or run `git submodule update --init --recursive` after clone
3. Submodule changes are properly tracked in commits

## References

- [Git Submodules Documentation](https://git-scm.com/book/en/v2/Git-Tools-Submodules)
- [System Guide](SYSTEM_GUIDE.md) - Overall system architecture
