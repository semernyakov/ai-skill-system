"""AI Skill System CLI"""

import click
from rich.console import Console
from rich.table import Table
import httpx

console = Console()
API_BASE = "http://127.0.0.1:8000/api/v1"


@click.group()
def cli():
    """AI Skill System Management CLI"""
    pass


@cli.group()
def rules():
    """Manage rules"""
    pass


@rules.command("list")
def list_rules():
    """List all rules"""
    with httpx.Client(proxy=None) as client:
        response = client.get(f"{API_BASE}/rules")
        if response.status_code == 200:
            rules = response.json()
            table = Table(title="Rules")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="magenta")
            table.add_column("Description", style="green")
            table.add_column("Always Apply", style="yellow")
            
            for rule in rules:
                table.add_row(
                    str(rule["id"]),
                    rule["name"],
                    rule["description"][:50] + "..." if len(rule["description"]) > 50 else rule["description"],
                    "Yes" if rule["always_apply"] else "No"
                )
            console.print(table)
        else:
            console.print(f"[red]Error: {response.status_code}[/red]")


@rules.command("create")
@click.option("--name", required=True, help="Rule name")
@click.option("--description", required=True, help="Rule description")
@click.option("--globs", help="File globs (comma-separated)")
@click.option("--always-apply", is_flag=True, help="Apply to all files")
def create_rule(name, description, globs, always_apply):
    """Create a new rule"""
    data = {
        "name": name,
        "description": description,
        "globs": globs.split(",") if globs else [],
        "always_apply": always_apply
    }
    with httpx.Client(proxy=None) as client:
        response = client.post(f"{API_BASE}/rules", json=data)
        if response.status_code == 201:
            rule = response.json()
            console.print(f"[green]Rule created with ID: {rule['id']}[/green]")
        else:
            console.print(f"[red]Error: {response.status_code}[/red]")


@rules.command("delete")
@click.argument("rule_id")
def delete_rule(rule_id):
    """Delete a rule"""
    with httpx.Client(proxy=None) as client:
        response = client.delete(f"{API_BASE}/rules/{rule_id}")
        if response.status_code == 204:
            console.print(f"[green]Rule {rule_id} deleted[/green]")
        else:
            console.print(f"[red]Error: {response.status_code}[/red]")


@cli.group()
def skills():
    """Manage skills"""
    pass


@skills.command("list")
def list_skills():
    """List all skills"""
    with httpx.Client(proxy=None) as client:
        response = client.get(f"{API_BASE}/skills")
        if response.status_code == 200:
            skills = response.json()
            table = Table(title="Skills")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="magenta")
            table.add_column("Description", style="green")
            
            for skill in skills:
                table.add_row(
                    str(skill["id"]),
                    skill["name"],
                    skill["description"][:50] + "..." if len(skill["description"]) > 50 else skill["description"]
                )
            console.print(table)
        else:
            console.print(f"[red]Error: {response.status_code}[/red]")


@skills.command("create")
@click.option("--name", required=True, help="Skill name")
@click.option("--description", required=True, help="Skill description")
def create_skill(name, description):
    """Create a new skill"""
    data = {
        "name": name,
        "description": description
    }
    with httpx.Client(proxy=None) as client:
        response = client.post(f"{API_BASE}/skills", json=data)
        if response.status_code == 201:
            skill = response.json()
            console.print(f"[green]Skill created with ID: {skill['id']}[/green]")
        else:
            console.print(f"[red]Error: {response.status_code}[/red]")


@skills.command("delete")
@click.argument("skill_id")
def delete_skill(skill_id):
    """Delete a skill"""
    with httpx.Client(proxy=None) as client:
        response = client.delete(f"{API_BASE}/skills/{skill_id}")
        if response.status_code == 204:
            console.print(f"[green]Skill {skill_id} deleted[/green]")
        else:
            console.print(f"[red]Error: {response.status_code}[/red]")


@cli.group()
def mcp():
    """Manage MCP Gateway services"""
    pass


@mcp.command("list")
def list_mcp_services():
    """List all MCP services"""
    with httpx.Client(proxy=None) as client:
        response = client.get(f"{API_BASE}/mcp/services")
        if response.status_code == 200:
            services = response.json()
            table = Table(title="MCP Gateway Services")
            table.add_column("Name", style="cyan")
            table.add_column("Status", style="magenta")
            table.add_column("Host", style="green")
            table.add_column("Port", style="yellow")
            
            for service in services:
                status_style = "green" if service["status"] == "running" else "red"
                table.add_row(
                    service["name"],
                    f"[{status_style}]{service['status']}[/{status_style}]",
                    service["host"],
                    str(service["port"])
                )
            console.print(table)
        else:
            console.print(f"[red]Error: {response.status_code}[/red]")


@mcp.command("start")
@click.argument("service_name")
def start_mcp_service(service_name):
    """Start an MCP service"""
    with httpx.Client(proxy=None) as client:
        response = client.post(f"{API_BASE}/mcp/services/start", json={"service_name": service_name})
        if response.status_code == 200:
            console.print(f"[green]Service {service_name} started[/green]")
        else:
            console.print(f"[red]Error: {response.status_code}[/red]")


@mcp.command("stop")
@click.argument("service_name")
def stop_mcp_service(service_name):
    """Stop an MCP service"""
    with httpx.Client(proxy=None) as client:
        response = client.post(f"{API_BASE}/mcp/services/stop", json={"service_name": service_name})
        if response.status_code == 200:
            console.print(f"[green]Service {service_name} stopped[/green]")
        else:
            console.print(f"[red]Error: {response.status_code}[/red]")


@mcp.command("health")
def check_mcp_health():
    """Check health of all MCP services"""
    with httpx.Client(proxy=None) as client:
        response = client.get(f"{API_BASE}/mcp/services/health")
        if response.status_code == 200:
            health_data = response.json()
            table = Table(title="MCP Services Health")
            table.add_column("Name", style="cyan")
            table.add_column("Status", style="magenta")
            table.add_column("Uptime", style="green")
            table.add_column("Last Check", style="yellow")
            
            for service, health in health_data.items():
                status_style = "green" if health["healthy"] else "red"
                table.add_row(
                    service,
                    f"[{status_style}]{'Healthy' if health['healthy'] else 'Unhealthy'}[/{status_style}]",
                    health.get("uptime", "N/A"),
                    health.get("last_check", "N/A")
                )
            console.print(table)
        else:
            console.print(f"[red]Error: {response.status_code}[/red]")


@cli.group()
def sync():
    """IDE synchronization"""
    pass


@sync.command("run")
@click.option("--force-all", is_flag=True, help="Force sync all IDEs")
def run_sync(force_all):
    """Trigger IDE synchronization"""
    data = {"force_all": force_all}
    with httpx.Client(proxy=None) as client:
        response = client.post(f"{API_BASE}/sync", json=data)
        if response.status_code == 200:
            result = response.json()
            console.print(f"[green]Sync completed[/green]")
            console.print(f"Status: {result['status']}")
            console.print(f"Targets: {result['targets_synced']}")
        else:
            console.print(f"[red]Error: {response.status_code}[/red]")


@cli.group()
def audit():
    """System audit"""
    pass


@audit.command("run")
@click.option("--type", "audit_type", default="security", help="Audit type: security, performance, architecture, compliance")
def run_audit(audit_type):
    """Run system audit"""
    data = {"audit_type": audit_type.upper()}
    with httpx.Client(proxy=None) as client:
        response = client.post(f"{API_BASE}/audit/run", json=data)
        if response.status_code == 200:
            result = response.json()
            console.print(f"[green]Audit completed (ID: {result['id']})[/green]")
            console.print(f"Type: {result['audit_type']}")
            console.print(f"Summary: {result['summary']}")
        else:
            console.print(f"[red]Error: {response.status_code}[/red]")


@audit.command("results")
def list_audit_results():
    """List all audit results"""
    with httpx.Client(proxy=None) as client:
        response = client.get(f"{API_BASE}/audit/results")
        if response.status_code == 200:
            results = response.json()
            table = Table(title="Audit Results")
            table.add_column("ID", style="cyan")
            table.add_column("Type", style="magenta")
            table.add_column("Status", style="green")
            table.add_column("Summary", style="yellow")
            
            for result in results:
                table.add_row(
                    str(result["id"]),
                    result["audit_type"],
                    result["status"],
                    result["summary"]
                )
            console.print(table)
        else:
            console.print(f"[red]Error: {response.status_code}[/red]")


@cli.group()
def logs():
    """System logs"""
    pass


@logs.command("view")
@click.option("--service", help="Filter by service")
@click.option("--level", help="Filter by level: DEBUG, INFO, WARNING, ERROR")
@click.option("--limit", default=50, help="Number of logs to show")
def view_logs(service, level, limit):
    """View system logs"""
    data = {"service": service, "level": level, "limit": limit}
    with httpx.Client(proxy=None) as client:
        response = client.post(f"{API_BASE}/logs", json=data)
        if response.status_code == 200:
            logs = response.json()
            table = Table(title="System Logs")
            table.add_column("Timestamp", style="cyan")
            table.add_column("Level", style="magenta")
            table.add_column("Service", style="green")
            table.add_column("Message", style="yellow")
            
            for log in logs:
                table.add_row(
                    str(log["timestamp"]),
                    log["level"],
                    log["service"],
                    log["message"][:50] + "..." if len(log["message"]) > 50 else log["message"]
                )
            console.print(table)
        else:
            console.print(f"[red]Error: {response.status_code}[/red]")


if __name__ == "__main__":
    cli()
