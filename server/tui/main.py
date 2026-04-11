"""AI Skill System TUI"""

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Static, Button, DataTable, ListView, ListItem
import httpx

API_BASE = "http://127.0.0.1:8000/api/v1"


class SkillSystemTUI(App):
    """AI Skill System Terminal UI"""

    BINDINGS = [
        ("d", "show_dashboard", "Dashboard"),
        ("r", "show_rules", "Rules"),
        ("s", "show_skills", "Skills"),
        ("m", "show_mcp", "MCP Gateway"),
        ("a", "show_audit", "Audit"),
        ("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            Static("AI Skill System Dashboard", id="title"),
            Horizontal(
                Vertical(Static("Press keys to navigate:", id="help")),
                Vertical(Static("[d] Dashboard  [r] Rules  [s] Skills  [m] MCP  [a] Audit  [q] Quit", id="shortcuts")),
            ),
            Static(id="content"),
        )
        yield Footer()

    def action_show_dashboard(self) -> None:
        self.query_one("#title").update("AI Skill System Dashboard")
        self.query_one("#content").update("Dashboard view - System overview")

    def action_show_rules(self) -> None:
        self.query_one("#title").update("Rules Manager")
        content = self.query_one("#content")
        try:
            with httpx.Client(proxy=None) as client:
                response = client.get(f"{API_BASE}/rules")
                if response.status_code == 200:
                    rules = response.json()
                    text = "\n".join([f"- {r['name']}: {r['description'][:30]}..." for r in rules])
                    content.update(f"Rules:\n{text}")
                else:
                    content.update("Failed to load rules")
        except Exception as e:
            content.update(f"Error: {e}")

    def action_show_skills(self) -> None:
        self.query_one("#title").update("Skills Manager")
        content = self.query_one("#content")
        try:
            with httpx.Client(proxy=None) as client:
                response = client.get(f"{API_BASE}/skills")
                if response.status_code == 200:
                    skills = response.json()
                    text = "\n".join([f"- {s['name']}: {s['description'][:30]}..." for s in skills])
                    content.update(f"Skills:\n{text}")
                else:
                    content.update("Failed to load skills")
        except Exception as e:
            content.update(f"Error: {e}")

    def action_show_mcp(self) -> None:
        self.query_one("#title").update("MCP Gateway")
        content = self.query_one("#content")
        try:
            with httpx.Client(proxy=None) as client:
                response = client.get(f"{API_BASE}/mcp/services")
                if response.status_code == 200:
                    services = response.json()
                    text = "\n".join([f"- {s['name']}: {s['status']}" for s in services])
                    content.update(f"MCP Services:\n{text}")
                else:
                    content.update("Failed to load MCP services")
        except Exception as e:
            content.update(f"Error: {e}")

    def action_show_audit(self) -> None:
        self.query_one("#title").update("System Audit")
        content = self.query_one("#content")
        content.update("Audit view - Run system audits")

    def action_quit(self) -> None:
        self.exit()


if __name__ == "__main__":
    app = SkillSystemTUI()
    app.run()
