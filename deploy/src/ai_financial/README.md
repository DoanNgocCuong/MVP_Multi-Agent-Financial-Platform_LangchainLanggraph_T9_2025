# AI Financial Package

## 📦 Package Overview

The `ai_financial` package is the core of the AI Financial Multi-Agent System, providing a comprehensive financial automation platform for SMBs. It implements a multi-agent architecture using LangChain and LangGraph for intelligent financial analysis and automation.

## 🏗️ Package Structure

```
ai_financial/
├── __init__.py                 # Package initialization and exports
├── main.py                     # FastAPI application entry point
├── cli.py                      # Command-line interface
├── core/                       # Core infrastructure
│   ├── __init__.py
│   ├── base_agent.py          # Base agent class with LangGraph integration
│   ├── config.py              # Configuration management
│   ├── database.py            # Database connection management
│   └── logging.py             # Logging and tracing setup
├── models/                     # Data models and schemas
│   ├── __init__.py
│   ├── agent_models.py        # Agent-related data models
│   ├── agent.py               # Agent state and context models
│   ├── enums.py               # System enumerations
│   ├── financial_models.py    # Financial data models
│   ├── financial.py           # Financial domain models
│   └── integration.py         # External integration models
├── agents/                     # AI agent implementations
│   ├── __init__.py
│   ├── advisory/              # Advisory context agents
│   │   ├── __init__.py
│   │   └── ai_cfo_agent.py    # AI CFO agent implementation
│   └── document_processing/   # Document processing agents
│       └── __pycache__/
├── mcp/                        # Model Context Protocol integration
│   ├── __init__.py
│   ├── hub.py                 # Tool hub for MCP tools
│   ├── server.py              # MCP server implementation
│   └── tools/                 # MCP tool implementations
│       ├── __init__.py
│       ├── base_tool.py       # Base tool class
│       └── financial_tools.py # Financial calculation tools
├── orchestrator/               # Agent orchestration
│   ├── __init__.py
│   ├── context_manager.py     # Context management
│   ├── orchestrator.py        # Main orchestrator
│   └── workflow_engine.py     # Workflow management
└── api/                        # API layer (if exists)
    └── __pycache__/
```

## 🚀 Quick Start

### Basic Usage

```python
from ai_financial.orchestrator.orchestrator import get_orchestrator
from ai_financial.agents.advisory.ai_cfo_agent import AICFOAgent

# Initialize system
orchestrator = get_orchestrator()
ai_cfo = AICFOAgent(industry="healthcare")
orchestrator.register_agent(ai_cfo)

# Start system
await orchestrator.start()

# Execute request
result = await orchestrator.route_request(
    request="Analyze our company's financial health",
    preferred_agent="ai_cfo_agent"
)

# Stop system
await orchestrator.stop()
```

### CLI Usage

```bash
# Start server
ai-financial start

# Interactive chat
ai-financial chat

# Check system status
ai-financial status

# List available agents
ai-financial agents

# List available tools
ai-financial tools
```

## 🧩 Core Components

### 1. Base Agent (`core/base_agent.py`)

Foundation class for all AI agents with LangGraph integration:

```python
from ai_financial.core.base_agent import BaseAgent
from langgraph.graph import StateGraph, END

class MyAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_id="my_agent",
            name="My Agent",
            description="Custom agent description"
        )
    
    def _build_graph(self) -> StateGraph:
        # Define agent workflow graph
        pass
    
    async def _process_request(self, state: AgentState) -> AgentState:
        # Implement agent logic
        pass
```

### 2. Configuration (`core/config.py`)

Centralized configuration management with environment variable support:

```python
from ai_financial.core.config import settings

# Access configuration
print(settings.api_host)
print(settings.llm.openai_model)
print(settings.database.postgres_url)
```

### 3. Orchestrator (`orchestrator/orchestrator.py`)

Central coordination system for multi-agent workflows:

```python
from ai_financial.orchestrator.orchestrator import get_orchestrator

orchestrator = get_orchestrator()

# Register agents
orchestrator.register_agent(my_agent)

# Route requests
result = await orchestrator.route_request(
    request="Your request here",
    preferred_agent="agent_id",
    workflow_type="advisory"
)
```

### 4. Tool Hub (`mcp/hub.py`)

Centralized tool management following MCP standards:

```python
from ai_financial.mcp.hub import get_tool_hub

tool_hub = get_tool_hub()

# Register tools
tool_hub.register_tool(my_tool)

# Execute tools
result = await tool_hub.execute_tool(
    tool_name="tool_name",
    parameters={"param": "value"}
)
```

## 🤖 Agent System

### AI CFO Agent

Industry-specific financial advisory agent:

```python
from ai_financial.agents.advisory.ai_cfo_agent import AICFOAgent

# Create agent for specific industry
ai_cfo = AICFOAgent(industry="healthcare")

# Supported industries
industries = ["general", "healthcare", "automotive", "pharmaceutical"]
```

**Capabilities:**
- Financial health analysis
- Industry benchmarking
- Risk assessment
- Strategic recommendations
- Cash flow analysis
- Profitability analysis
- Liquidity analysis
- Compliance monitoring

### Agent Workflow

Each agent follows a structured workflow:

1. **Request Analysis**: Understand and classify the request
2. **Data Gathering**: Collect relevant financial data
3. **Analysis**: Perform financial calculations and analysis
4. **Insight Generation**: Generate insights using LLM
5. **Risk Assessment**: Evaluate risks and opportunities
6. **Recommendations**: Provide actionable recommendations
7. **Response Formatting**: Format final response

## 🔧 Financial Tools

### Available Tools

1. **Financial Ratio Calculator** (`financial_ratio_calculator`)
   - Current ratio, quick ratio
   - Debt-to-equity ratio
   - Return on equity/assets
   - Gross/net margin
   - Asset turnover

2. **Cash Flow Analyzer** (`cash_flow_analyzer`)
   - Trend analysis
   - Seasonal patterns
   - Volatility assessment
   - Comprehensive analysis

3. **Profitability Analyzer** (`profitability_analyzer`)
   - Margin analysis
   - Return metrics
   - Efficiency analysis
   - Comprehensive profitability

### Tool Usage

```python
# Execute financial ratio calculation
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
```

## ⚡ Workflows

### Advisory Workflow

Multi-step process for CEO support:

```
Data Sync → Financial Analysis → Forecasting → Risk Assessment → Executive Reporting
```

### Transactional Workflow

Automated accounting process:

```
OCR Processing → Standardization → Accounting → Reconciliation → Compliance
```

### Workflow Execution

```python
# Execute advisory workflow
result = await orchestrator.route_request(
    request="Provide comprehensive financial analysis",
    workflow_type="advisory"
)

# Stream workflow execution
async for update in orchestrator.stream_workflow("advisory", "analyze"):
    print(update)
```

## 📊 Data Models

### Agent Models (`models/agent_models.py`)

- `AgentContext`: Execution context for agents
- `AgentState`: State management for agent workflows
- `WorkflowState`: Multi-step workflow state
- `AgentStatus`: Agent status enumeration

### Financial Models (`models/financial_models.py`)

- `Transaction`: Financial transaction data
- `Account`: Account information
- `Invoice`: Invoice data
- `Forecast`: Financial forecasting models

### Integration Models (`models/integration.py`)

- External system integration schemas
- API response models
- Data synchronization models

## 🔌 API Integration

### FastAPI Application (`main.py`)

RESTful API with the following endpoints:

- `GET /` - System information
- `GET /health` - Health check
- `POST /api/v1/agents/{agent_id}/invoke` - Invoke agent
- `POST /api/v1/workflows/{workflow_type}/execute` - Execute workflow
- `GET /api/v1/workflows/{workflow_type}/stream` - Stream workflow
- `GET /api/v1/tools` - List tools
- `POST /api/v1/tools/{tool_name}/execute` - Execute tool
- `GET /api/v1/status` - System status
- `GET /api/v1/trace-test` - Tracing test

### API Usage Examples

```bash
# Health check
curl http://localhost:8000/health

# Invoke AI CFO agent
curl -X POST http://localhost:8000/api/v1/agents/ai_cfo_agent/invoke \
  -H "Content-Type: application/json" \
  -d '{"message": "Analyze our financial health"}'

# Execute tool
curl -X POST http://localhost:8000/api/v1/tools/financial_ratio_calculator/execute \
  -H "Content-Type: application/json" \
  -d '{
    "parameters": {
      "ratio_type": "current_ratio",
      "financial_data": {
        "current_assets": 100000,
        "current_liabilities": 50000
      }
    }
  }'
```

## 🔍 Monitoring and Logging

### Structured Logging

All components use structured logging with correlation IDs:

```python
from ai_financial.core.logging import get_logger

logger = get_logger(__name__)
logger.info("Operation completed", 
           agent_id="ai_cfo_agent", 
           duration=1.5,
           success=True)
```

### Distributed Tracing

OpenTelemetry integration for request tracing:

```python
from ai_financial.core.logging import get_tracer

tracer = get_tracer(__name__)
with tracer.start_as_current_span("operation_name") as span:
    span.set_attribute("key", "value")
    # Your operation here
```

### Langfuse Integration

LLM interaction monitoring and token usage tracking:

```python
# Automatic tracking of LLM calls
response = await self.llm.ainvoke(messages)
```

## 🛡️ Security

### Authentication and Authorization

- JWT token-based authentication
- Role-based access control
- API key management
- Request validation

### Data Protection

- Environment-based configuration
- Encrypted data storage
- Secure API endpoints
- Audit logging

## 🧪 Testing

### Unit Testing

```python
import pytest
from ai_financial.agents.advisory.ai_cfo_agent import AICFOAgent

def test_ai_cfo_agent_initialization():
    agent = AICFOAgent(industry="healthcare")
    assert agent.agent_id == "ai_cfo_agent"
    assert agent.industry == "healthcare"
```

### Integration Testing

```python
import pytest
from ai_financial.orchestrator.orchestrator import get_orchestrator

@pytest.mark.asyncio
async def test_orchestrator_workflow():
    orchestrator = get_orchestrator()
    # Test workflow execution
```

## 📈 Performance Optimization

### Caching

- Redis-based caching for frequently accessed data
- Agent response caching
- Tool result caching

### Concurrency

- Configurable concurrent agent limits
- Async/await throughout the system
- Connection pooling for database access

### Monitoring

- Performance metrics collection
- Memory usage monitoring
- Response time tracking

## 🔧 Configuration

### Environment Variables

Key configuration options:

```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# LLM Configuration
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4-turbo-preview

# Database Configuration
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=ai_financial
POSTGRES_PASSWORD=password
POSTGRES_DB=ai_financial

# Redis Configuration
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your_secret_key_here

# Monitoring
LANGFUSE_SECRET_KEY=your_langfuse_key
LANGFUSE_PUBLIC_KEY=your_langfuse_public_key
```

### Industry Specialization

Configure agents for specific industries:

```python
# Healthcare industry
ai_cfo = AICFOAgent(industry="healthcare")

# Automotive industry
ai_cfo = AICFOAgent(industry="automotive")

# Pharmaceutical industry
ai_cfo = AICFOAgent(industry="pharmaceutical")
```

## 🚀 Deployment

### Development

```bash
# Install in development mode
pip install -e .

# Run with auto-reload
ai-financial start --reload
```

### Production

```bash
# Install production dependencies
pip install -e ".[prod]"

# Run with production settings
ENVIRONMENT=production ai-financial start
```

## 🤝 Contributing

### Adding New Agents

1. Create agent class inheriting from `BaseAgent`
2. Implement required methods
3. Add tests
4. Update documentation

### Adding New Tools

1. Create tool class inheriting from `BaseTool`
2. Implement execution logic
3. Add parameter validation
4. Register with tool hub

### Code Standards

- Follow PEP 8 style guidelines
- Use type hints throughout
- Add comprehensive docstrings
- Include unit tests
- Update documentation

## 📚 Additional Resources

- **CLI Documentation**: See `cli.py` for command-line options
- **API Documentation**: Available at `/docs` when server is running
- **Configuration Reference**: See `core/config.py` for all options
- **Model Schemas**: See `models/` directory for data structures
- **Test Examples**: See `tests/` directory for usage examples

