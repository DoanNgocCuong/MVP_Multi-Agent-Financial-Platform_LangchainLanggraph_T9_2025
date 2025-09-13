```
(.venv) PS D:\GIT\MVP_Multi-Agent-Financial-Platform_LangchainLanggraph_T9_2025\New folder\src> python run_demo.py
🏦 AI Financial Multi-Agent System
==================================================
WARNING: Using auto-generated SECRET_KEY for development. Set SECRET_KEY environment variable for production.
🔧 Environment: development
🔧 Debug mode: True
🔧 API endpoint: http://0.0.0.0:8000
⚠️  OpenAI API key not configured (demo mode)

What would you like to do?
1. Run interactive demo
2. Start web server
3. Run CLI chat
4. Show system status
5. Exit

Enter your choice (1-5): 1

🚀 Starting interactive demo...
D:\GIT\MVP_Multi-Agent-Financial-Platform_LangchainLanggraph_T9_2025\New folder\.venv\Lib\site-packages\pydantic\_internal\_config.py:373: UserWarning: Valid config keys have changed in V2:
* 'schema_extra' has been renamed to 'json_schema_extra'
  warnings.warn(message, UserWarning)
D:\GIT\MVP_Multi-Agent-Financial-Platform_LangchainLanggraph_T9_2025\New folder\.venv\Lib\site-packages\pydantic\_internal\_config.py:373: UserWarning: Valid config keys have changed in V2:
* 'schema_extra' has been renamed to 'json_schema_extra'
  warnings.warn(message, UserWarning)
D:\GIT\MVP_Multi-Agent-Financial-Platform_LangchainLanggraph_T9_2025\New folder\.venv\Lib\site-packages\pydantic\_internal\_config.py:373: UserWarning: Valid config keys have changed in V2:
* 'schema_extra' has been renamed to 'json_schema_extra'
  warnings.warn(message, UserWarning)
{"server_id": "default", "name": "Default MCP Server", "host": "localhost", "port": 8001, "event": "MCP Server initialized", "timestamp": "2025-09-13T13:31:25.929592Z", "level": "info"}
{"default_server_host": "localhost", "default_server_port": 8001, "event": "Tool Hub initialized", "timestamp": "2025-09-13T13:31:25.930591Z", "level": "info"}
{"event": "Workflow Engine initialized", "timestamp": "2025-09-13T13:31:25.933601Z", "level": "info"}
{"event": "Context Manager initialized", "timestamp": "2025-09-13T13:31:25.934601Z", "level": "info"}
{"max_concurrent_agents": 10, "event": "Agent Orchestrator initialized", "timestamp": "2025-09-13T13:31:25.934601Z", "level": "info"}
D:\GIT\MVP_Multi-Agent-Financial-Platform_LangchainLanggraph_T9_2025\New folder\.venv\Lib\site-packages\pydantic\_internal\_config.py:373: UserWarning: Valid config keys have changed in V2:
* 'schema_extra' has been renamed to 'json_schema_extra'
  warnings.warn(message, UserWarning)
╭───────────────────── 🏦 Welcome ─────────────────────╮
│ AI Financial Multi-Agent System Demo                 │
│ Comprehensive financial automation platform for SMBs │
╰──────────────────────────────────────────────────────╯
╭───────── 🚀 System Initialization ─────────╮
│ Setting up AI Financial Multi-Agent System │
╰────────────────────────────────────────────╯
📋 Registering agents...
{"agent_id": "ai_cfo_agent", "event": "OpenAI API key not configured, using mock LLM for development", "timestamp": "2025-09-13T13:31:26.016076Z", "level": "warning"}    
{"agent_id": "ai_cfo_agent", "name": "AI CFO", "model": "gpt-4-turbo-preview", "event": "Agent initialized", "timestamp": "2025-09-13T13:31:26.031121Z", "level": "info"}   
{"industry": "healthcare", "metrics_count": 4, "event": "AI CFO Agent initialized", "timestamp": "2025-09-13T13:31:26.031121Z", "level": "info"}
{"agent_id": "ai_cfo_agent", "agent_name": "AI CFO", "capabilities": 10, "event": "Agent registered", "timestamp": "2025-09-13T13:31:26.032122Z", "level": "info"}
🔧 Registering tools...
{"tool_name": "financial_ratio_calculator", "category": "financial_analysis", "version": "1.0.0", "event": "Tool initialized", "timestamp": "2025-09-13T13:31:26.033151Z", "level": "info"}
{"tool_name": "financial_ratio_calculator", "server_id": "default", "category": "financial_analysis", "event": "Tool registered", "timestamp": "2025-09-13T13:31:26.033151Z", "level": "info"}
{"tool_name": "financial_ratio_calculator", "server_id": "default", "category": "financial_analysis", "event": "Tool registered with hub", "timestamp": "2025-09-13T13:31:26.034144Z", "level": "info"}
{"tool_name": "cash_flow_analyzer", "category": "financial_analysis", "version": "1.0.0", "event": "Tool initialized", "timestamp": "2025-09-13T13:31:26.034144Z", "level": "info"}
{"tool_name": "cash_flow_analyzer", "server_id": "default", "category": "financial_analysis", "event": "Tool registered", "timestamp": "2025-09-13T13:31:26.035120Z", "level": "info"}
{"tool_name": "cash_flow_analyzer", "server_id": "default", "category": "financial_analysis", "event": "Tool registered with hub", "timestamp": "2025-09-13T13:31:26.035120Z", "level": "info"}
{"tool_name": "profitability_analyzer", "category": "financial_analysis", "version": "1.0.0", "event": "Tool initialized", "timestamp": "2025-09-13T13:31:26.035120Z", "level": "info"}
{"tool_name": "profitability_analyzer", "server_id": "default", "category": "financial_analysis", "event": "Tool registered", "timestamp": "2025-09-13T13:31:26.035120Z", "level": "info"}
{"tool_name": "profitability_analyzer", "server_id": "default", "category": "financial_analysis", "event": "Tool registered with hub", "timestamp": "2025-09-13T13:31:26.036153Z", "level": "info"}
⚡ Starting system...
{"server_id": "default", "host": "localhost", "port": 8001, "tools_count": 3, "event": "MCP Server started", "timestamp": "2025-09-13T13:31:26.037150Z", "level": "info"}   
{"server_id": "default", "event": "Server started", "timestamp": "2025-09-13T13:31:26.037150Z", "level": "info"}
{"registered_agents": 1, "event": "Agent Orchestrator started", "timestamp": "2025-09-13T13:31:26.037150Z", "level": "info"}
✅ System ready!

╭─ 📊 Status Check ──╮
│ System Status Demo │
╰────────────────────╯
     Agent Orchestrator Status    
┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┓
┃ Property          ┃ Value        ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━┩
│ Running           │ True         │
│ Registered Agents │ 1            │
│ Active Workflows  │ 0            │
│ Agent List        │ ai_cfo_agent │
└───────────────────┴──────────────┘

          Tool Hub Status
┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┓
┃ Property    ┃ Value              ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━┩
│ Total Tools │ 3                  │
│ Servers     │ 1                  │
│ Categories  │ financial_analysis │
└─────────────┴────────────────────┘

╭─ 🔧 Financial Tools ─╮
│ Tool Execution Demo  │
╰──────────────────────╯
Demo 1: Financial Ratio Calculation
⠋ Calculating current ratio...{"tool_name": "financial_ratio_calculator", "server_id": "default", "execution_time": 0.0, "success": true, "event": "Tool executed successfully", "timestamp": "2025-09-13T13:31:26.051907Z", "level": "info"}

╭───────────────────────────── ✅ Ratio Analysis Result ─────────────────────────────╮
│ Current Ratio: 2.00                                                                │
│ Current Assets: $150,000.00                                                        │
│ Current Liabilities: $75,000.00                                                    │
│ Interpretation: Strong liquidity position                                          │
│ Execution Time: 0.000s                                                             │
╰────────────────────────────────────────────────────────────────────────────────────╯

Demo 2: Cash Flow Analysis
⠋ Analyzing cash flow trends...{"tool_name": "cash_flow_analyzer", "server_id": "default", "execution_time": 0.0, "success": true, "event": "Tool executed successfully", "timestamp": "2025-09-13T13:31:26.059937Z", "level": "info"}

╭─────────────────────────── 📈 Cash Flow Analysis Result ───────────────────────────╮
│ Cash Flow Trend: Strong Positive                                                   │
│ Average Change: 10.6%                                                              │
│ Volatility Level: Low                                                              │
│ Average Flow: $31,333.33                                                           │
│ Positive Periods: 6/6                                                              │
╰────────────────────────────────────────────────────────────────────────────────────╯

╭─── 🤖 AI CFO Agent ────╮
│ Agent Interaction Demo │
╰────────────────────────╯
Demo: Financial Health Analysis
⠋ AI CFO analyzing financial health...{"agent_id": "ai_cfo_agent", "request_length": 115, "event": "Request analyzed", "timestamp": "2025-09-13T13:31:26.078458Z", "level": "info"}
{"agent_id": "ai_cfo_agent", "company_id": "default", "data_points": 5, "event": "Financial data gathered", "timestamp": "2025-09-13T13:31:26.079993Z", "level": "info"}  
{"agent_id": "ai_cfo_agent", "analysis_types": ["liquidity_analysis", "profitability_analysis", "efficiency_analysis", "leverage_analysis", "industry_comparison"], "event": "Financial analysis completed", "timestamp": "2025-09-13T13:31:26.080990Z", "level": "info"}
{"agent_id": "ai_cfo_agent", "insights_length": 0, "event": "Insights generated", "timestamp": "2025-09-13T13:31:26.081990Z", "level": "info"}
{"agent_id": "ai_cfo_agent", "risk_categories": 5, "event": "Risk assessment completed", "timestamp": "2025-09-13T13:31:26.084021Z", "level": "info"}
{"agent_id": "ai_cfo_agent", "recommendations_length": 0, "event": "Recommendations generated", "timestamp": "2025-09-13T13:31:26.084988Z", "level": "info"}
{"agent_id": "ai_cfo_agent", "report_length": 565, "event": "CFO analysis completed", "timestamp": "2025-09-13T13:31:26.086991Z", "level": "info"}
{"agent_id": "ai_cfo_agent", "session_id": "0d683ddd-5c9f-4265-8978-2d74c1473321", "trace_id": 177786821065587325143714912750204168013, "event": "Agent request processed successfully", "timestamp": "2025-09-13T13:31:26.087988Z", "level": "info"}
{"error": "'coroutine' object has no attribute 'get'", "session_id": "0d683ddd-5c9f-4265-8978-2d74c1473321", "event": "Request routing failed", "timestamp": "2025-09-13T13:31:26.091989Z", "level": "error"}
D:\GIT\MVP_Multi-Agent-Financial-Platform_LangchainLanggraph_T9_2025\New
folder\src\ai_financial\orchestrator\orchestrator.py:142: RuntimeWarning: coroutine   
'AICFOAgent._format_response' was never awaited
  return {
RuntimeWarning: Enable tracemalloc to get the object allocation traceback
╭────────────────────────── 🤖 AI CFO Response (Demo Mode) ──────────────────────────╮
│ Demo Mode - OpenAI API not configured                                              │
│                                                                                    │
│ The AI CFO agent would normally provide:                                           │
│ • Comprehensive financial health analysis                                          │
│ • Industry-specific insights for healthcare                                        │
│ • Risk assessment and opportunities                                                │
│ • Strategic recommendations                                                        │
│ • Executive summary with citations                                                 │
│                                                                                    │
│ Error: Routing failed: 'coroutine' object has no attribute 'get'                   │
╰────────────────────────────────────────────────────────────────────────────────────╯


╭─ ⚡ Advisory Workflow ──╮
│ Workflow Execution Demo │
╰─────────────────────────╯
Demo: Advisory Workflow for CEO Support
Workflow Steps:
  1. 📊 Data Synchronization
  2. 🔍 Financial Analysis
  3. 📈 Forecasting
  4. ⚠️ Risk Assessment
  5. 📋 Executive Reporting

⠋ Executing advisory workflow...{"agent_id": "ai_cfo_agent", "request_length": 67, "event": "Request analyzed", "timestamp": "2025-09-13T13:31:26.114082Z", "level": "info"}
{"agent_id": "ai_cfo_agent", "company_id": "default", "data_points": 5, "event": "Financial data gathered", "timestamp": "2025-09-13T13:31:26.115049Z", "level": "info"}  
{"agent_id": "ai_cfo_agent", "analysis_types": ["liquidity_analysis", "profitability_analysis", "efficiency_analysis", "leverage_analysis", "industry_comparison"], "event": "Financial analysis completed", "timestamp": "2025-09-13T13:31:26.116045Z", "level": "info"}
{"agent_id": "ai_cfo_agent", "insights_length": 0, "event": "Insights generated", "timestamp": "2025-09-13T13:31:26.117046Z", "level": "info"}
{"agent_id": "ai_cfo_agent", "risk_categories": 5, "event": "Risk assessment completed", "timestamp": "2025-09-13T13:31:26.118047Z", "level": "info"}
{"agent_id": "ai_cfo_agent", "recommendations_length": 0, "event": "Recommendations generated", "timestamp": "2025-09-13T13:31:26.119051Z", "level": "info"}
{"agent_id": "ai_cfo_agent", "report_length": 565, "event": "CFO analysis completed", "timestamp": "2025-09-13T13:31:26.120051Z", "level": "info"}
{"agent_id": "ai_cfo_agent", "session_id": "74dffffc-ac77-47b4-9545-bdf430692b8b", "trace_id": 66030045462428017218947792823702500766, "event": "Agent request processed successfully", "timestamp": "2025-09-13T13:31:26.121050Z", "level": "info"}
╭────────────────────────── ✅ Advisory Workflow Complete ───────────────────────────╮
│ Workflow completed successfully!                                                   │
│                                                                                    │
│ Workflow ID: 3761c959-5d42-4a72-89d2-affa2cef64b2                                  │
│ Completed Steps: 1                                                                 │
│ Results Available: 1                                                               │
│                                                                                    │
│ The advisory workflow would provide:                                               │
│ • Real-time financial health dashboard                                             │
│ • 13-week cash flow forecast                                                       │
│ • 12-month P&L projections                                                         │
│ • Risk alerts and opportunities                                                    │
│ • Executive brief with recommendations                                             │
╰────────────────────────────────────────────────────────────────────────────────────╯


D:\GIT\MVP_Multi-Agent-Financial-Platform_LangchainLanggraph_T9_2025\New folder\src\demo.py:406: RuntimeWarning: coroutine 'AICFOAgent._format_response' was never awaited  
  await demo_workflow_execution(orchestrator)
RuntimeWarning: Enable tracemalloc to get the object allocation traceback
╭─ 🎯 AI Financial Multi-Agent System ─╮
│ System Capabilities Overview         │
╰──────────────────────────────────────╯
                                 System Capabilities
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Component       ┃ Capabilities                                                     ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ AI CFO Agent    │ Financial analysis, industry insights, risk assessment,          │
│                 │ strategic recommendations                                        │
│ Financial Tools │ Ratio calculations, cash flow analysis, profitability metrics,   │
│                 │ trend analysis                                                   │
│ Workflow Engine │ Multi-step workflows, approval processes, error handling, state  │
│                 │ management                                                       │
│ MCP Tool Hub    │ Centralized tool management, standardized interfaces,            │
│                 │ performance monitoring                                           │
│ Orchestrator    │ Agent coordination, intelligent routing, concurrent execution,   │
│                 │ context management                                               │
└─────────────────┴──────────────────────────────────────────────────────────────────┘

                    Integration Capabilities
┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ System Type         ┃ Examples                               ┃
┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ ERP Systems         │ SAP, Oracle, NetSuite                  │
│ Accounting Software │ QuickBooks, Xero, Sage                 │
│ Banking APIs        │ Plaid, Yodlee, Open Banking            │
│ POS Systems         │ Square, Shopify, Toast                 │
│ Industry Software   │ Epic (Healthcare), DealerSocket (Auto) │
└─────────────────────┴────────────────────────────────────────┘

╭────────────────── 🎉 Demo Complete ──────────────────╮
│ Demo completed successfully!                         │
│                                                      │
│ Next steps:                                          │
│ 1. Configure OpenAI API key for full AI capabilities │
│ 2. Set up database connections for data persistence  │
│ 3. Configure external system integrations            │
│ 4. Customize agents for your industry                │
│ 5. Deploy to production environment                  │
│                                                      │
│ Run 'ai-financial --help' for CLI options            │
╰──────────────────────────────────────────────────────╯
{"server_id": "default", "event": "MCP Server stopped", "timestamp": "2025-09-13T13:31:26.138099Z", "level": "info"}
{"server_id": "default", "event": "Server stopped", "timestamp": "2025-09-13T13:31:26.139207Z", "level": "info"}
{"event": "Agent Orchestrator stopped", "timestamp": "2025-09-13T13:31:26.139207Z", "level": "info"}
Transient error StatusCode.UNAVAILABLE encountered while exporting traces to localhost:4317, retrying in 1.15s.
Failed to export traces to localhost:4317, error code: StatusCode.UNAVAILABLE
(.venv) PS D:\GIT\MVP_Multi-Agent-Financial-Platform_LangchainLanggraph_T9_2025\New folder\src>
```
