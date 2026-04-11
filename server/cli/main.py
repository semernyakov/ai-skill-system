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


if __name__ == "__main__":
    cli()
