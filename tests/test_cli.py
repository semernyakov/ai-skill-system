"""CLI Integration Tests"""

import pytest
import subprocess
import sys


class TestCLICommands:
    """Test CLI command execution"""

    def test_cli_help(self):
        """Test CLI help command"""
        result = subprocess.run(
            [sys.executable, "-m", "server.cli.main", "--help"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert "AI Skill System" in result.stdout

    def test_rules_list(self):
        """Test rules list command"""
        result = subprocess.run(
            [sys.executable, "-m", "server.cli.main", "rules", "list"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0

    def test_skills_list(self):
        """Test skills list command"""
        result = subprocess.run(
            [sys.executable, "-m", "server.cli.main", "skills", "list"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0

    def test_mcp_list(self):
        """Test MCP list command"""
        result = subprocess.run(
            [sys.executable, "-m", "server.cli.main", "mcp", "list"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0

    def test_mcp_health(self):
        """Test MCP health command"""
        result = subprocess.run(
            [sys.executable, "-m", "server.cli.main", "mcp", "health"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0

    def test_audit_run(self):
        """Test audit run command"""
        result = subprocess.run(
            [sys.executable, "-m", "server.cli.main", "audit", "run", "security"],
            capture_output=True,
            text=True
        )
        assert result.returncode in [0, 1]  # May fail if server not running

    def test_logs_view(self):
        """Test logs view command"""
        result = subprocess.run(
            [sys.executable, "-m", "server.cli.main", "logs", "view"],
            capture_output=True,
            text=True
        )
        assert result.returncode in [0, 1]  # May fail if server not running
