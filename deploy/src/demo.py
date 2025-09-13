#!/usr/bin/env python3
"""
Demo script for the AI Financial Multi-Agent System.

This script demonstrates the key capabilities of the system including:
- Agent orchestration
- Tool execution
- Workflow management
- Financial analysis
"""

import asyncio
import json
from typing import Dict, Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from ai_financial.orchestrator.orchestrator import get_orchestrator
from ai_financial.mcp.hub import get_tool_hub
from ai_financial.agents.advisory.ai_cfo_agent import AICFOAgent
from ai_financial.mcp.tools.financial_tools import (
    FinancialRatioTool,
    CashFlowAnalysisTool,
    ProfitabilityAnalysisTool,
)

console = Console()


async def setup_system():
    """Set up the AI Financial Multi-Agent System."""
    console.print(Panel.fit(
        "[bold blue]Setting up AI Financial Multi-Agent System[/bold blue]",
        title="🚀 System Initialization"
    ))
    
    # Get core components
    orchestrator = get_orchestrator()
    tool_hub = get_tool_hub()
    
    # Register agents
    console.print("📋 Registering agents...")
    ai_cfo = AICFOAgent(industry="healthcare")
    orchestrator.register_agent(ai_cfo)
    
    # Register tools
    console.print("🔧 Registering tools...")
    tool_hub.register_tool(FinancialRatioTool())
    tool_hub.register_tool(CashFlowAnalysisTool())
    tool_hub.register_tool(ProfitabilityAnalysisTool())
    
    # Start system
    console.print("⚡ Starting system...")
    await orchestrator.start()
    
    console.print("[green]✅ System ready![/green]\n")
    
    return orchestrator, tool_hub


async def demo_system_status(orchestrator, tool_hub):
    """Demonstrate system status reporting."""
    console.print(Panel.fit(
        "[bold cyan]System Status Demo[/bold cyan]",
        title="📊 Status Check"
    ))
    
    # Get status
    orch_status = orchestrator.get_orchestrator_status()
    hub_status = tool_hub.get_hub_status()
    
    # Display orchestrator status
    orch_table = Table(title="Agent Orchestrator Status")
    orch_table.add_column("Property", style="cyan")
    orch_table.add_column("Value", style="green")
    
    orch_table.add_row("Running", str(orch_status["running"]))
    orch_table.add_row("Registered Agents", str(orch_status["registered_agents"]))
    orch_table.add_row("Active Workflows", str(orch_status["active_workflows"]))
    orch_table.add_row("Agent List", ", ".join(orch_status["agent_list"]))
    
    console.print(orch_table)
    console.print()
    
    # Display tool hub status
    hub_table = Table(title="Tool Hub Status")
    hub_table.add_column("Property", style="cyan")
    hub_table.add_column("Value", style="green")
    
    hub_table.add_row("Total Tools", str(hub_status["total_tools"]))
    hub_table.add_row("Servers", str(hub_status["servers_count"]))
    hub_table.add_row("Categories", ", ".join(hub_status["enabled_tool_categories"]))
    
    console.print(hub_table)
    console.print()


async def demo_tool_execution(tool_hub):
    """Demonstrate tool execution capabilities."""
    console.print(Panel.fit(
        "[bold yellow]Tool Execution Demo[/bold yellow]",
        title="🔧 Financial Tools"
    ))
    
    # Demo 1: Financial Ratio Calculation
    console.print("[bold]Demo 1: Financial Ratio Calculation[/bold]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Calculating current ratio...", total=None)
        
        result = await tool_hub.execute_tool(
            tool_name="financial_ratio_calculator",
            parameters={
                "ratio_type": "current_ratio",
                "financial_data": {
                    "current_assets": 150000,
                    "current_liabilities": 75000
                }
            }
        )
        
        progress.remove_task(task)
    
    if result.success:
        console.print(Panel(
            f"[green]Current Ratio: {result.data['ratio']:.2f}[/green]\n"
            f"Current Assets: ${result.data['current_assets']:,.2f}\n"
            f"Current Liabilities: ${result.data['current_liabilities']:,.2f}\n"
            f"Interpretation: {result.data['interpretation']}\n"
            f"Execution Time: {result.execution_time:.3f}s",
            title="✅ Ratio Analysis Result",
            border_style="green"
        ))
    else:
        console.print(f"[red]Error: {result.error}[/red]")
    
    console.print()
    
    # Demo 2: Cash Flow Analysis
    console.print("[bold]Demo 2: Cash Flow Analysis[/bold]")
    
    sample_cash_flows = [
        {"period": "2024-01", "net_cash_flow": 25000},
        {"period": "2024-02", "net_cash_flow": 32000},
        {"period": "2024-03", "net_cash_flow": 28000},
        {"period": "2024-04", "net_cash_flow": 35000},
        {"period": "2024-05", "net_cash_flow": 30000},
        {"period": "2024-06", "net_cash_flow": 38000},
    ]
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Analyzing cash flow trends...", total=None)
        
        result = await tool_hub.execute_tool(
            tool_name="cash_flow_analyzer",
            parameters={
                "cash_flows": sample_cash_flows,
                "analysis_type": "comprehensive"
            }
        )
        
        progress.remove_task(task)
    
    if result.success:
        trend_data = result.data["trend_analysis"]
        volatility_data = result.data["volatility_analysis"]
        
        console.print(Panel(
            f"[green]Cash Flow Trend: {trend_data['trend']}[/green]\n"
            f"Average Change: {trend_data['average_change_percent']:.1f}%\n"
            f"Volatility Level: {volatility_data['volatility_level']}\n"
            f"Average Flow: ${volatility_data['mean_cash_flow']:,.2f}\n"
            f"Positive Periods: {result.data['positive_periods']}/{len(sample_cash_flows)}",
            title="📈 Cash Flow Analysis Result",
            border_style="green"
        ))
    else:
        console.print(f"[red]Error: {result.error}[/red]")
    
    console.print()


async def demo_agent_interaction(orchestrator):
    """Demonstrate agent interaction capabilities."""
    console.print(Panel.fit(
        "[bold magenta]Agent Interaction Demo[/bold magenta]",
        title="🤖 AI CFO Agent"
    ))
    
    # Demo financial analysis request
    console.print("[bold]Demo: Financial Health Analysis[/bold]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("AI CFO analyzing financial health...", total=None)
        
        # Note: This will use a mock response since we don't have real OpenAI API key
        try:
            result = await orchestrator.route_request(
                request="Analyze our company's financial health and provide recommendations for a healthcare company with $2M annual revenue",
                preferred_agent="ai_cfo_agent"
            )
            
            progress.remove_task(task)
            
            if result.get("error"):
                console.print(Panel(
                    f"[yellow]Demo Mode - OpenAI API not configured[/yellow]\n\n"
                    f"The AI CFO agent would normally provide:\n"
                    f"• Comprehensive financial health analysis\n"
                    f"• Industry-specific insights for healthcare\n"
                    f"• Risk assessment and opportunities\n"
                    f"• Strategic recommendations\n"
                    f"• Executive summary with citations\n\n"
                    f"Error: {result['error']}",
                    title="🤖 AI CFO Response (Demo Mode)",
                    border_style="yellow"
                ))
            else:
                console.print(Panel(
                    result.get("response", "Analysis completed successfully"),
                    title="🤖 AI CFO Response",
                    border_style="green"
                ))
        
        except Exception as e:
            progress.remove_task(task)
            console.print(Panel(
                f"[yellow]Demo Mode - OpenAI API not configured[/yellow]\n\n"
                f"The AI CFO agent is ready but requires OpenAI API configuration.\n"
                f"Set OPENAI_API_KEY environment variable to enable full functionality.\n\n"
                f"Expected capabilities:\n"
                f"• Financial ratio analysis\n"
                f"• Cash flow forecasting\n"
                f"• Risk assessment\n"
                f"• Industry benchmarking\n"
                f"• Strategic recommendations",
                title="🤖 AI CFO Agent (Demo Mode)",
                border_style="yellow"
            ))
    
    console.print()


async def demo_workflow_execution(orchestrator):
    """Demonstrate workflow execution capabilities."""
    console.print(Panel.fit(
        "[bold green]Workflow Execution Demo[/bold green]",
        title="⚡ Advisory Workflow"
    ))
    
    console.print("[bold]Demo: Advisory Workflow for CEO Support[/bold]")
    
    # Show workflow steps
    workflow_steps = [
        "📊 Data Synchronization",
        "🔍 Financial Analysis", 
        "📈 Forecasting",
        "⚠️ Risk Assessment",
        "📋 Executive Reporting"
    ]
    
    console.print("Workflow Steps:")
    for i, step in enumerate(workflow_steps, 1):
        console.print(f"  {i}. {step}")
    
    console.print()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Executing advisory workflow...", total=None)
        
        try:
            result = await orchestrator.route_request(
                request="Execute comprehensive advisory workflow for quarterly board meeting",
                workflow_type="advisory"
            )
            
            progress.remove_task(task)
            
            if result.get("success"):
                console.print(Panel(
                    f"[green]Workflow completed successfully![/green]\n\n"
                    f"Workflow ID: {result.get('workflow_id', 'N/A')}\n"
                    f"Completed Steps: {len(result.get('completed_steps', []))}\n"
                    f"Results Available: {len(result.get('results', {}))}\n\n"
                    f"The advisory workflow would provide:\n"
                    f"• Real-time financial health dashboard\n"
                    f"• 13-week cash flow forecast\n"
                    f"• 12-month P&L projections\n"
                    f"• Risk alerts and opportunities\n"
                    f"• Executive brief with recommendations",
                    title="✅ Advisory Workflow Complete",
                    border_style="green"
                ))
            else:
                console.print(Panel(
                    f"[yellow]Demo Mode - Limited functionality[/yellow]\n\n"
                    f"The advisory workflow is configured but requires:\n"
                    f"• OpenAI API key for AI agents\n"
                    f"• Database connections for data sync\n"
                    f"• External system integrations\n\n"
                    f"Error: {result.get('error', 'Unknown error')}",
                    title="⚡ Advisory Workflow (Demo Mode)",
                    border_style="yellow"
                ))
        
        except Exception as e:
            progress.remove_task(task)
            console.print(Panel(
                f"[yellow]Demo Mode - Configuration needed[/yellow]\n\n"
                f"The workflow system is ready but needs configuration.\n"
                f"See README.md for setup instructions.\n\n"
                f"Error: {str(e)}",
                title="⚡ Workflow Demo",
                border_style="yellow"
            ))
    
    console.print()


async def demo_system_capabilities():
    """Demonstrate overall system capabilities."""
    console.print(Panel.fit(
        "[bold blue]System Capabilities Overview[/bold blue]",
        title="🎯 AI Financial Multi-Agent System"
    ))
    
    capabilities_table = Table(title="System Capabilities")
    capabilities_table.add_column("Component", style="cyan")
    capabilities_table.add_column("Capabilities", style="green")
    
    capabilities_table.add_row(
        "AI CFO Agent",
        "Financial analysis, industry insights, risk assessment, strategic recommendations"
    )
    capabilities_table.add_row(
        "Financial Tools",
        "Ratio calculations, cash flow analysis, profitability metrics, trend analysis"
    )
    capabilities_table.add_row(
        "Workflow Engine",
        "Multi-step workflows, approval processes, error handling, state management"
    )
    capabilities_table.add_row(
        "MCP Tool Hub",
        "Centralized tool management, standardized interfaces, performance monitoring"
    )
    capabilities_table.add_row(
        "Orchestrator",
        "Agent coordination, intelligent routing, concurrent execution, context management"
    )
    
    console.print(capabilities_table)
    console.print()
    
    # Integration capabilities
    integration_table = Table(title="Integration Capabilities")
    integration_table.add_column("System Type", style="cyan")
    integration_table.add_column("Examples", style="green")
    
    integration_table.add_row("ERP Systems", "SAP, Oracle, NetSuite")
    integration_table.add_row("Accounting Software", "QuickBooks, Xero, Sage")
    integration_table.add_row("Banking APIs", "Plaid, Yodlee, Open Banking")
    integration_table.add_row("POS Systems", "Square, Shopify, Toast")
    integration_table.add_row("Industry Software", "Epic (Healthcare), DealerSocket (Auto)")
    
    console.print(integration_table)
    console.print()


async def main():
    """Main demo function."""
    console.print(Panel.fit(
        "[bold white]AI Financial Multi-Agent System Demo[/bold white]\n"
        "[italic]Comprehensive financial automation platform for SMBs[/italic]",
        title="🏦 Welcome",
        border_style="blue"
    ))
    
    try:
        # Set up system
        orchestrator, tool_hub = await setup_system()
        
        # Run demos
        await demo_system_status(orchestrator, tool_hub)
        await demo_tool_execution(tool_hub)
        await demo_agent_interaction(orchestrator)
        await demo_workflow_execution(orchestrator)
        await demo_system_capabilities()
        
        # Completion message
        console.print(Panel.fit(
            "[bold green]Demo completed successfully![/bold green]\n\n"
            "[italic]Next steps:[/italic]\n"
            "1. Configure OpenAI API key for full AI capabilities\n"
            "2. Set up database connections for data persistence\n"
            "3. Configure external system integrations\n"
            "4. Customize agents for your industry\n"
            "5. Deploy to production environment\n\n"
            "[bold]Run 'ai-financial --help' for CLI options[/bold]",
            title="🎉 Demo Complete",
            border_style="green"
        ))
        
        # Cleanup
        await orchestrator.stop()
        
    except Exception as e:
        console.print(Panel(
            f"[red]Demo failed with error:[/red]\n{str(e)}\n\n"
            f"[yellow]This is likely due to missing configuration.[/yellow]\n"
            f"Please check the README.md for setup instructions.",
            title="❌ Demo Error",
            border_style="red"
        ))


if __name__ == "__main__":
    asyncio.run(main())