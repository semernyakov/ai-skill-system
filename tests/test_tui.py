"""TUI Integration Tests"""

import pytest
import subprocess
import sys


class TestTUICommands:
    """Test TUI command execution"""

    def test_tui_help(self):
        """Test TUI help command"""
        result = subprocess.run(
            [sys.executable, "-m", "server.tui.main", "--help"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0

    def test_tui_imports(self):
        """Test TUI module imports"""
        try:
            from server.tui.main import SkillSystemTUI
            assert SkillSystemTUI is not None
        except ImportError as e:
            pytest.skip(f"TUI module not available: {e}")
