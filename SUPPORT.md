# Support

## Getting Help

If you need help with the AI Skill System, here are the best ways to get support:

### Documentation

- Check the [README.md](README.md) for project overview
- Review [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines
- See [TEAM.md](TEAM.md) for project structure and roles

### Community

- Open an issue on GitHub for bugs or questions
- Use the `question` label for general questions
- Use the `bug` label for bug reports
- Use the `enhancement` label for feature requests

### Direct Contact

For security issues or private matters, email i.s.semernyakov@yandex.ru

## Common Issues

### Sync Issues

If IDE rules aren't syncing:

```bash
# Run sync manually
./.ai/scripts/sync-all.sh

# Check if .ai/ directory exists
ls -la .ai/
```

### Git Hooks

If pre-commit hooks aren't working:

```bash
# Reinstall hooks
./.ai/scripts/install-hooks.sh
```

### File Permissions

If scripts aren't executable:

```bash
chmod +x .ai/scripts/*.sh
```

## Response Time

We aim to respond to GitHub issues within 48 hours. For urgent matters, please use direct email.
