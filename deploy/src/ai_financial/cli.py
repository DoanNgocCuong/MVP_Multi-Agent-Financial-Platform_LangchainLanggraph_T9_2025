"""Command-line interface for the AI Financial Multi-Agent System."""

import asyncio
import json
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from ai_financial.core.config import settings
from ai_financial.orchestrator.orchestrator import get_orchestrator
from ai_financial.mcp.hub import get_tool_hub
from ai_financial.agents.advisory.ai_cfo_agent import AICFOAgent
from ai_financial.mcp.tools.financial_tools import (
    FinancialRatioTool,
    CashFlowAnalysisTool,
    ProfitabilityAnalysisTool,
)

app = typer.Typer(
    name="ai-financial",
    help="AI Financial Multi-Agent System CLI",
    add_completion=False,
)

console = Console()


@app.command()
def start(
    host: str = typer.Option(settings.api_host, "--host", "-h", help="Host to bind to"),
    port: int = typer.Option(settings.api_port, "--port", "-p", help="Port to bind to"),
    reload: bool = typer.Option(False, "--reload", help="Enable auto-reload"),
):
    """Start the AI Financial Multi-Agent System server."""
    import uvicorn
    from ai_financial.main import app as fastapi_app
    
    console.print(Panel.fit(
        "[bold blue]AI Financial Multi-Agent System[/bold blue]\n"
        f"Starting server on {host}:{port}",
        title="🚀 Starting Server"
    ))
    
    uvicorn.run(
        "ai_financial.main:app",
        host=host,
        port=port,
        reload=reload,
        log_level=settings.monitoring.log_level.lower(),
    )


@app.command()
def status():
    """Show system status."""
    async def _get_status():
        # Initialize system
        orchestrator = get_orchestrator()
        tool_hub = get_tool_hub()
        
        # Register basic components for status check
        ai_cfo = AICFOAgent()
        orchestrator.register_agent(ai_cfo)
        
        tool_hub.register_tool(FinancialRatioTool())
        tool_hub.register_tool(CashFlowAnalysisTool())
        
        await orchestrator.start()
        
        # Get status
        orchestrator_status = orchestrator.get_orchestrator_status()
        hub_status = tool_hub.get_hub_status()
        
        await orchestrator.stop()
        
        return orchestrator_status, hub_status
    
    orchestrator_status, hub_status = asyncio.run(_get_status())
    
    # Display status
    console.print(Panel.fit(
        "[bold green]System Status[/bold green]",
        title="📊 AI Financial System"
    ))
    
    # Orchestrator status table
    orch_table = Table(title="Agent Orchestrator")
    orch_table.add_column("Property", style="cyan")
    orch_table.add_column("Value", style="green")
    
    orch_table.add_row("Running", str(orchestrator_status["running"]))
    orch_table.add_row("Registered Agents", str(orchestrator_status["registered_agents"]))
    orch_table.add_row("Active Workflows", str(orchestrator_status["active_workflows"]))
    orch_table.add_row("Max Concurrent", str(orchestrator_status["max_concurrent_agents"]))
    
    console.print(orch_table)
    console.print()
    
    # Tool hub status table
    hub_table = Table(title="Tool Hub")
    hub_table.add_column("Property", style="cyan")
    hub_table.add_column("Value", style="green")
    
    hub_table.add_row("Servers", str(hub_status["servers_count"]))
    hub_table.add_row("Total Tools", str(hub_status["total_tools"]))
    hub_table.add_row("Tool Categories", ", ".join(hub_status["enabled_tool_categories"]))
    
    console.print(hub_table)


@app.command()
def agents():
    """List available agents."""
    async def _list_agents():
        orchestrator = get_orchestrator()
        
        # Register agents
        ai_cfo = AICFOAgent()
        orchestrator.register_agent(ai_cfo)
        
        return orchestrator.get_orchestrator_status()
    
    status = asyncio.run(_list_agents())
    
    console.print(Panel.fit(
        "[bold blue]Available Agents[/bold blue]",
        title="🤖 Agents"
    ))
    
    table = Table()
    table.add_column("Agent ID", style="cyan")
    table.add_column("Status", style="green")
    
    for agent_id in status["agent_list"]:
        table.add_row(agent_id, "Available")
    
    console.print(table)


@app.command()
def tools():
    """List available tools."""
    async def _list_tools():
        tool_hub = get_tool_hub()
        
        # Register tools
        tool_hub.register_tool(FinancialRatioTool())
        tool_hub.register_tool(CashFlowAnalysisTool())
        tool_hub.register_tool(ProfitabilityAnalysisTool())
        
        return tool_hub.get_available_tools()
    
    tools_list = asyncio.run(_list_tools())
    
    console.print(Panel.fit(
        "[bold blue]Available Tools[/bold blue]",
        title="🔧 Tools"
    ))
    
    table = Table()
    table.add_column("Tool Name", style="cyan")
    table.add_column("Category", style="yellow")
    table.add_column("Description", style="green")
    
    for tool in tools_list:
        table.add_row(
            tool.name,
            tool.category,
            tool.description[:50] + "..." if len(tool.description) > 50 else tool.description
        )
    
    console.print(table)


@app.command()
def chat(
    agent: Optional[str] = typer.Option(None, "--agent", "-a", help="Specific agent to chat with"),
    workflow: Optional[str] = typer.Option(None, "--workflow", "-w", help="Workflow type (advisory/transactional)"),
):
    """Interactive chat with agents or workflows."""
    async def _setup_system():
        orchestrator = get_orchestrator()
        tool_hub = get_tool_hub()
        
        # Register components
        ai_cfo = AICFOAgent()
        orchestrator.register_agent(ai_cfo)
        
        tool_hub.register_tool(FinancialRatioTool())
        tool_hub.register_tool(CashFlowAnalysisTool())
        
        await orchestrator.start()
        return orchestrator
    
    async def _chat_session(orchestrator):
        console.print(Panel.fit(
            "[bold green]AI Financial Chat Session[/bold green]\n"
            "Type 'exit' to quit, 'help' for commands",
            title="💬 Chat"
        ))
        
        while True:
            try:
                message = typer.prompt("\n🤖 You")
                
                if message.lower() in ['exit', 'quit', 'bye']:
                    console.print("[yellow]Goodbye![/yellow]")
                    break
                
                if message.lower() == 'help':
                    console.print(Panel(
                        "Available commands:\n"
                        "• Type any financial question\n"
                        "• 'exit' - Quit chat\n"
                        "• 'help' - Show this help",
                        title="Help"
                    ))
                    continue
                
                # Process message
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    console=console,
                ) as progress:
                    task = progress.add_task("Processing...", total=None)
                    
                    result = await orchestrator.route_request(
                        request=message,
                        preferred_agent=agent,
                        workflow_type=workflow,
                    )
                    
                    progress.remove_task(task)
                
                # Display response
                if result.get("success", True):
                    response = result.get("response", "No response generated")
                    console.print(Panel(
                        response,
                        title="🤖 AI Financial Assistant",
                        border_style="green"
                    ))
                else:
                    error = result.get("error", "Unknown error")
                    console.print(Panel(
                        f"[red]Error: {error}[/red]",
                        title="❌ Error",
                        border_style="red"
                    ))
                    
            except KeyboardInterrupt:
                console.print("\n[yellow]Chat interrupted. Goodbye![/yellow]")
                break
            except Exception as e:
                console.print(f"[red]Error: {str(e)}[/red]")
    
    async def _run_chat():
        orchestrator = await _setup_system()
        try:
            await _chat_session(orchestrator)
        finally:
            await orchestrator.stop()
    
    asyncio.run(_run_chat())


@app.command()
def test_tool(
    tool_name: str = typer.Argument(..., help="Name of the tool to test"),
    parameters: str = typer.Option("{}", "--params", "-p", help="Tool parameters as JSON"),
):
    """Test a specific tool."""
    async def _test_tool():
        tool_hub = get_tool_hub()
        
        # Register tools
        tool_hub.register_tool(FinancialRatioTool())
        tool_hub.register_tool(CashFlowAnalysisTool())
        tool_hub.register_tool(ProfitabilityAnalysisTool())
        
        try:
            params = json.loads(parameters)
        except json.JSONDecodeError:
            console.print("[red]Invalid JSON parameters[/red]")
            return
        
        console.print(f"Testing tool: [cyan]{tool_name}[/cyan]")
        console.print(f"Parameters: [yellow]{parameters}[/yellow]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Executing tool...", total=None)
            
            result = await tool_hub.execute_tool(tool_name, params)
            
            progress.remove_task(task)
        
        # Display result
        if result.success:
            console.print(Panel(
                f"[green]Success![/green]\n\n"
                f"Data: {json.dumps(result.data, indent=2)}\n"
                f"Execution time: {result.execution_time:.3f}s",
                title="✅ Tool Result",
                border_style="green"
            ))
        else:
            console.print(Panel(
                f"[red]Failed![/red]\n\n"
                f"Error: {result.error}",
                title="❌ Tool Error",
                border_style="red"
            ))
    
    asyncio.run(_test_tool())


@app.command()
def config():
    """Show current configuration."""
    console.print(Panel.fit(
        "[bold blue]System Configuration[/bold blue]",
        title="⚙️ Configuration"
    ))
    
    table = Table()
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Environment", settings.environment)
    table.add_row("Debug Mode", str(settings.debug))
    table.add_row("API Host", settings.api_host)
    table.add_row("API Port", str(settings.api_port))
    table.add_row("Log Level", settings.monitoring.log_level)
    table.add_row("Max Concurrent Agents", str(settings.workflow.max_concurrent_agents))
    table.add_row("OpenAI Model", settings.llm.openai_model)
    
    console.print(table)


def main():
    """Main CLI entry point."""
    try:
        app()
    except Exception as e:
        console.print(Panel(
            f"[red]CLI Error:[/red] {str(e)}\n\n"
            f"[yellow]This might be due to missing configuration.[/yellow]\n"
            f"Try running: [bold]python run_demo.py[/bold]",
            title="❌ Error",
            border_style="red"
        ))
        return 1


if __name__ == "__main__":
    main()