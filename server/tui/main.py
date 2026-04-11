"""AI Skill System TUI"""

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Static, Button, DataTable, Input, Label
from textual.containers import Container
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
            Container(Static(id="content")),
        )
        yield Footer()

    def action_show_dashboard(self) -> None:
        self.query_one("#title").update("AI Skill System Dashboard")
        content = self.query_one("#content")
        try:
            with httpx.Client(proxy=None) as client:
                rules_resp = client.get(f"{API_BASE}/rules")
                skills_resp = client.get(f"{API_BASE}/skills")
                mcp_resp = client.get(f"{API_BASE}/mcp/services")
                
                rules_count = len(rules_resp.json()) if rules_resp.status_code == 200 else 0
                skills_count = len(skills_resp.json()) if skills_resp.status_code == 200 else 0
                mcp_count = len(mcp_resp.json()) if mcp_resp.status_code == 200 else 0
                
                content.update(
                    f"System Overview:\n\n"
                    f"Rules: {rules_count}\n"
                    f"Skills: {skills_count}\n"
                    f"MCP Services: {mcp_count}\n"
                    f"Server: http://127.0.0.1:8000"
                )
        except Exception as e:
            content.update(f"Error: {e}")

    def action_show_rules(self) -> None:
        self.query_one("#title").update("Rules Manager")
        content = self.query_one("#content")
        try:
            with httpx.Client(proxy=None) as client:
                response = client.get(f"{API_BASE}/rules")
                if response.status_code == 200:
                    rules = response.json()
                    if rules:
                        text = "\n".join([f"• {r['name']}: {r['description'][:40]}..." for r in rules])
                        content.update(f"Rules ({len(rules)}):\n\n{text}")
                    else:
                        content.update("No rules found")
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
                    if skills:
                        text = "\n".join([f"• {s['name']}: {s['description'][:40]}..." for s in skills])
                        content.update(f"Skills ({len(skills)}):\n\n{text}")
                    else:
                        content.update("No skills found")
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
                    if services:
                        text = "\n".join([f"• {s['name']}: {s['status']} ({s['host']}:{s['port']})" for s in services])
                        content.update(f"MCP Services ({len(services)}):\n\n{text}")
                    else:
                        content.update("No MCP services found")
                else:
                    content.update("Failed to load MCP services")
        except Exception as e:
            content.update(f"Error: {e}")

    def action_show_audit(self) -> None:
        self.query_one("#title").update("System Audit")
        content = self.query_one("#content")
        try:
            with httpx.Client(proxy=None) as client:
                response = client.get(f"{API_BASE}/audit/results")
                if response.status_code == 200:
                    results = response.json()
                    if results:
                        text = "\n".join([f"• #{r['id']} - {r['audit_type']}: {r['summary']}" for r in results])
                        content.update(f"Audit Results ({len(results)}):\n\n{text}")
                    else:
                        content.update("No audit results found. Use CLI to run audits.")
                else:
                    content.update("Failed to load audit results")
        except Exception as e:
            content.update(f"Error: {e}")

    def action_quit(self) -> None:
        self.exit()


if __name__ == "__main__":
    app = SkillSystemTUI()
    app.run()
