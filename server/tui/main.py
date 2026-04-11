"""AI Skill System TUI"""

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, Container
from textual.widgets import Header, Footer, Static, Button, DataTable, Input, Label, ListView, ListItem
from textual.screen import ModalScreen
from textual import on
import httpx
import json
import os

API_BASE = "http://127.0.0.1:8000/api/v1"
TOKEN_FILE = os.path.expanduser("~/.ai-skill-system-token.json")


def get_token():
    """Get stored JWT token"""
    try:
        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, "r") as f:
                data = json.load(f)
                return data.get("token")
    except Exception:
        pass
    return None


def get_auth_headers():
    """Get authentication headers with JWT token"""
    token = get_token()
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}


class CreateRuleScreen(ModalScreen):
    """Modal screen for creating a new rule"""

    def compose(self) -> ComposeResult:
        yield Container(
            Static("Create New Rule", id="modal-title"),
            Label("Name:"),
            Input(placeholder="Rule name", id="rule-name"),
            Label("Description:"),
            Input(placeholder="Rule description", id="rule-description"),
            Horizontal(
                Button("Create", id="create-btn", variant="primary"),
                Button("Cancel", id="cancel-btn"),
            )
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "create-btn":
            name = self.query_one("#rule-name").value
            description = self.query_one("#rule-description").value
            if name and description:
                try:
                    with httpx.Client(proxy=None) as client:
                        response = client.post(f"{API_BASE}/rules", json={
                            "name": name,
                            "description": description,
                            "globs": [],
                            "always_apply": False
                        }, headers=get_auth_headers())
                        if response.status_code == 200:
                            self.dismiss("created")
                        elif response.status_code == 401:
                            self.dismiss("Authentication required")
                        else:
                            self.dismiss(f"Error: {response.status_code}")
                except Exception as e:
                    self.dismiss(f"Error: {e}")
            else:
                self.dismiss("Please fill all fields")
        else:
            self.dismiss("cancelled")


class CreateSkillScreen(ModalScreen):
    """Modal screen for creating a new skill"""

    def compose(self) -> ComposeResult:
        yield Container(
            Static("Create New Skill", id="modal-title"),
            Label("Name:"),
            Input(placeholder="Skill name", id="skill-name"),
            Label("Description:"),
            Input(placeholder="Skill description", id="skill-description"),
            Horizontal(
                Button("Create", id="create-btn", variant="primary"),
                Button("Cancel", id="cancel-btn"),
            )
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "create-btn":
            name = self.query_one("#skill-name").value
            description = self.query_one("#skill-description").value
            if name and description:
                try:
                    with httpx.Client(proxy=None) as client:
                        response = client.post(f"{API_BASE}/skills", json={
                            "name": name,
                            "description": description
                        }, headers=get_auth_headers())
                        if response.status_code == 200:
                            self.dismiss("created")
                        elif response.status_code == 401:
                            self.dismiss("Authentication required")
                        else:
                            self.dismiss(f"Error: {response.status_code}")
                except Exception as e:
                    self.dismiss(f"Error: {e}")
            else:
                self.dismiss("Please fill all fields")
        else:
            self.dismiss("cancelled")


class SkillSystemTUI(App):
    """AI Skill System Terminal UI"""

    BINDINGS = [
        ("d", "show_dashboard", "Dashboard"),
        ("r", "show_rules", "Rules"),
        ("s", "show_skills", "Skills"),
        ("m", "show_mcp", "MCP Gateway"),
        ("a", "show_audit", "Audit"),
        ("l", "show_logs", "Logs"),
        ("c", "create_item", "Create"),
        ("q", "quit", "Quit"),
    ]

    CSS = """
    #content {
        height: 1fr;
    }
    #modal-title {
        text-align: center;
        text-style: bold;
        margin-bottom: 1;
    }
    Container {
        padding: 2;
    }
    """

    def __init__(self):
        super().__init__()
        self.current_screen = "dashboard"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            Static("AI Skill System Dashboard", id="title"),
            Horizontal(
                Vertical(Static("Keys:", id="help")),
                Vertical(Static("[d] Dashboard  [r] Rules  [s] Skills  [m] MCP  [a] Audit  [l] Logs  [c] Create  [q] Quit", id="shortcuts")),
            ),
            Container(Static(id="content")),
            Horizontal(
                Button("Create New", id="create-btn"),
                Button("Refresh", id="refresh-btn"),
            ),
        )
        yield Footer()

    def action_show_dashboard(self) -> None:
        self.current_screen = "dashboard"
        self.query_one("#title").update("AI Skill System Dashboard")
        self.query_one("#create-btn").display = False
        self._load_dashboard()

    def action_show_rules(self) -> None:
        self.current_screen = "rules"
        self.query_one("#title").update("Rules Manager")
        self.query_one("#create-btn").display = True
        self._load_rules()

    def action_show_skills(self) -> None:
        self.current_screen = "skills"
        self.query_one("#title").update("Skills Manager")
        self.query_one("#create-btn").display = True
        self._load_skills()

    def action_show_mcp(self) -> None:
        self.current_screen = "mcp"
        self.query_one("#title").update("MCP Gateway")
        self.query_one("#create-btn").display = False
        self._load_mcp()

    def action_show_audit(self) -> None:
        self.current_screen = "audit"
        self.query_one("#title").update("System Audit")
        self.query_one("#create-btn").display = False
        self._load_audit()

    def action_show_logs(self) -> None:
        self.current_screen = "logs"
        self.query_one("#title").update("System Logs")
        self.query_one("#create-btn").display = False
        self._load_logs()

    def action_create_item(self) -> None:
        if self.current_screen == "rules":
            self.push_screen(CreateRuleScreen(), self._on_create_rule_closed)
        elif self.current_screen == "skills":
            self.push_screen(CreateSkillScreen(), self._on_create_skill_closed)

    def _on_create_rule_closed(self, result) -> None:
        if result == "created":
            self._load_rules()
        elif result != "cancelled":
            self.query_one("#content").update(f"Error: {result}")

    def _on_create_skill_closed(self, result) -> None:
        if result == "created":
            self._load_skills()
        elif result != "cancelled":
            self.query_one("#content").update(f"Error: {result}")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "create-btn":
            self.action_create_item()
        elif event.button.id == "refresh-btn":
            if self.current_screen == "dashboard":
                self._load_dashboard()
            elif self.current_screen == "rules":
                self._load_rules()
            elif self.current_screen == "skills":
                self._load_skills()
            elif self.current_screen == "mcp":
                self._load_mcp()
            elif self.current_screen == "audit":
                self._load_audit()
            elif self.current_screen == "logs":
                self._load_logs()

    def _load_dashboard(self) -> None:
        content = self.query_one("#content")
        try:
            with httpx.Client(proxy=None) as client:
                rules_resp = client.get(f"{API_BASE}/rules", headers=get_auth_headers())
                skills_resp = client.get(f"{API_BASE}/skills", headers=get_auth_headers())
                mcp_resp = client.get(f"{API_BASE}/mcp/services", headers=get_auth_headers())

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

    def _load_rules(self) -> None:
        content = self.query_one("#content")
        try:
            with httpx.Client(proxy=None) as client:
                response = client.get(f"{API_BASE}/rules", headers=get_auth_headers())
                if response.status_code == 200:
                    rules = response.json()
                    if rules:
                        text = "\n".join([f"• [{r['id']}] {r['name']}: {r['description'][:50]}..." for r in rules])
                        content.update(f"Rules ({len(rules)}):\n\n{text}\n\nPress [c] to create new rule")
                    else:
                        content.update("No rules found. Press [c] to create one.")
                elif response.status_code == 401:
                    content.update("Authentication required. Use CLI to login: ai-skill-system auth login")
                else:
                    content.update("Failed to load rules")
        except Exception as e:
            content.update(f"Error: {e}")

    def _load_skills(self) -> None:
        content = self.query_one("#content")
        try:
            with httpx.Client(proxy=None) as client:
                response = client.get(f"{API_BASE}/skills", headers=get_auth_headers())
                if response.status_code == 200:
                    skills = response.json()
                    if skills:
                        text = "\n".join([f"• [{s['id']}] {s['name']}: {s['description'][:50]}..." for s in skills])
                        content.update(f"Skills ({len(skills)}):\n\n{text}\n\nPress [c] to create new skill")
                    else:
                        content.update("No skills found. Press [c] to create one.")
                elif response.status_code == 401:
                    content.update("Authentication required. Use CLI to login: ai-skill-system auth login")
                else:
                    content.update("Failed to load skills")
        except Exception as e:
            content.update(f"Error: {e}")

    def _load_mcp(self) -> None:
        content = self.query_one("#content")
        try:
            with httpx.Client(proxy=None) as client:
                response = client.get(f"{API_BASE}/mcp/services", headers=get_auth_headers())
                if response.status_code == 200:
                    services = response.json()
                    if services:
                        text = "\n".join([f"• {s['name']}: {s['status']} ({s['host']}:{s['port']})" for s in services])
                        content.update(f"MCP Services ({len(services)}):\n\n{text}")
                    else:
                        content.update("No MCP services found")
                elif response.status_code == 401:
                    content.update("Authentication required. Use CLI to login: ai-skill-system auth login")
                else:
                    content.update("Failed to load MCP services")
        except Exception as e:
            content.update(f"Error: {e}")

    def _load_audit(self) -> None:
        content = self.query_one("#content")
        try:
            with httpx.Client(proxy=None) as client:
                response = client.get(f"{API_BASE}/audit/results", headers=get_auth_headers())
                if response.status_code == 200:
                    results = response.json()
                    if results:
                        text = "\n".join([f"• #{r['id']} - {r['audit_type']}: {r['summary']}" for r in results])
                        content.update(f"Audit Results ({len(results)}):\n\n{text}\n\nUse CLI to run audits")
                    else:
                        content.update("No audit results found. Use CLI to run audits.")
                elif response.status_code == 401:
                    content.update("Authentication required. Use CLI to login: ai-skill-system auth login")
                else:
                    content.update("Failed to load audit results")
        except Exception as e:
            content.update(f"Error: {e}")

    def _load_logs(self) -> None:
        content = self.query_one("#content")
        try:
            with httpx.Client(proxy=None) as client:
                response = client.post(f"{API_BASE}/logs", json={"limit": 20}, headers=get_auth_headers())
                if response.status_code == 200:
                    logs = response.json()
                    if logs:
                        text = "\n".join([f"[{log['level']}] {log['service']}: {log['message'][:60]}..." for log in logs])
                        content.update(f"Recent Logs:\n\n{text}")
                    else:
                        content.update("No logs found")
                elif response.status_code == 401:
                    content.update("Authentication required. Use CLI to login: ai-skill-system auth login")
                else:
                    content.update("Failed to load logs")
        except Exception as e:
            content.update(f"Error: {e}")

    def action_quit(self) -> None:
        self.exit()


def main():
    """Entry point for package script"""
    app = SkillSystemTUI()
    app.run()


if __name__ == "__main__":
    main()
