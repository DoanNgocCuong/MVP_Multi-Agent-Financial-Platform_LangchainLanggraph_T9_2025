# AI Financial Multi-Agent System - Source Code

## 📁 Directory Structure

This directory contains the complete source code for the AI Financial Multi-Agent System, a comprehensive financial automation platform for SMBs.

```
src/
├── ai_financial/                    # Main package
│   ├── __init__.py                 # Package initialization
│   ├── main.py                     # FastAPI application entry point
│   ├── cli.py                      # Command-line interface
│   ├── core/                       # Core infrastructure components
│   ├── models/                     # Data models and schemas
│   ├── agents/                     # AI agent implementations
│   ├── mcp/                        # Model Context Protocol integration
│   └── orchestrator/               # Agent orchestration and workflows
├── tests/                          # Test suite
├── ai_financial_multi_agent_system.egg-info/  # Package metadata
├── demo.py                         # Interactive demo script
├── run_demo.py                     # Demo startup script
├── pyproject.toml                  # Project configuration
├── requirements.txt                # Python dependencies
├── README.md                       # This file
└── QUICKSTART.md                   # Quick start guide
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip or poetry
- OpenAI API key (optional for demo mode)

### Installation

```bash
# Navigate to src directory
cd src

# Install in development mode
pip install -e .

# Or install with all dependencies
pip install -e ".[dev]"
```

### Running the System

#### Option 1: Interactive Demo
```bash
python run_demo.py
```

#### Option 2: CLI Interface
```bash
# Start server
ai-financial start

# Interactive chat
ai-financial chat

# Check status
ai-financial status
```

#### Option 3: Direct Python
```bash
python -m ai_financial.main
```

## 📦 Package Components

### Core Package (`ai_financial/`)

The main package containing all system components:

- **`main.py`**: FastAPI application with REST API endpoints
- **`cli.py`**: Command-line interface for system management
- **`core/`**: Infrastructure components (config, logging, base classes)
- **`models/`**: Data models for agents, financial data, and workflows
- **`agents/`**: AI agent implementations for different financial tasks
- **`mcp/`**: Model Context Protocol integration for tool management
- **`orchestrator/`**: Multi-agent coordination and workflow management

### Test Suite (`tests/`)

Comprehensive test coverage including:
- Unit tests for individual components
- Integration tests for system workflows
- Performance and load testing
- API endpoint testing

### Demo Scripts

- **`demo.py`**: Interactive demonstration of system capabilities
- **`run_demo.py`**: Startup script with configuration management

## 🔧 Configuration

### Environment Setup

Create a `.env` file in the src directory:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4-turbo-preview

# Database Configuration
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=ai_financial
POSTGRES_PASSWORD=your_password
POSTGRES_DB=ai_financial

# Redis Configuration
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your_secret_key_here_at_least_32_characters_long

# Monitoring
LANGFUSE_SECRET_KEY=your_langfuse_secret_key
LANGFUSE_PUBLIC_KEY=your_langfuse_public_key
```

### Development Mode

The system can run in demo mode without full configuration:

```bash
# Run without OpenAI API key (limited functionality)
python run_demo.py
```

## 🏗️ Architecture Overview

### Multi-Agent System
- **Agent Orchestrator**: Central coordination of all agents
- **Workflow Engine**: Complex multi-step process management
- **Context Manager**: Shared state and execution context
- **Tool Hub**: Centralized financial calculation tools

## 🔄 Main System Flow

### 1. System Startup Flow
```
Application Start → Setup Logging & Tracing → Initialize Orchestrator → 
Initialize Tool Hub → Register Agents → Register Tools → Start Orchestrator → System Ready
```

**Key Components Initialized:**
- **7 Agents Registered:**
  - Advisory: AI CFO, Forecasting, Alert, Reporting
  - Processing: OCR, Data Sync, Reconciliation
- **Financial Tools:** Ratio Analysis, Cash Flow, Profitability
- **Monitoring:** OpenTelemetry tracing, Langfuse integration

### 2. Request Processing Flow
```
API Request → FastAPI Endpoint → Request Type Analysis → 
┌─ Direct Agent Routing ─→ Single Agent Processing ─┐
├─ Workflow Execution ─→ Multi-Agent Workflow ─────┤ → Return Result
└─ Intelligent Routing ─→ Keyword Analysis ─→ Route to Best Agent ─┘
```

### 3. Two Main Workflow Types

#### A. Advisory Workflow (CEO Support)
```
Data Sync → Analysis → Forecasting → Alerts → Reporting
```
**Purpose:** Comprehensive financial insights for executive decision-making
- **Data Sync:** Latest financial data collection
- **Analysis:** AI CFO deep financial analysis
- **Forecasting:** Future projections and trends
- **Alerts:** Risk and opportunity detection
- **Reporting:** Executive summary generation

#### B. Transactional Workflow (Automation)
```
OCR → Standardization → Accounting → Reconciliation → Compliance
```
**Purpose:** Automated transaction processing pipeline
- **OCR:** Document processing and data extraction
- **Standardization:** Data validation and normalization
- **Accounting:** Automated journal entries
- **Reconciliation:** Bank statement matching
- **Compliance:** Audit trail and regulatory checks

### 4. AI CFO Agent - Internal Workflow (7-Step Process)
```
User Input → analyze_request → gather_data → perform_analysis → 
generate_insights → assess_risks → provide_recommendations → format_response → Final Report
```

**Detailed Steps:**
1. **analyze_request:** Parse user intent and create analysis plan
2. **gather_data:** Collect financial data (transactions, accounts, invoices)
3. **perform_analysis:** Calculate ratios, benchmarks, and comparisons
4. **generate_insights:** AI-powered insights and trend identification
5. **assess_risks:** 5-category risk analysis (liquidity, credit, operational, market, compliance)
6. **provide_recommendations:** Strategic recommendations with timeline classification
7. **format_response:** Professional financial report in Markdown format

### 5. Intelligent Routing System
**Keyword-based automatic routing:**
- `"forecast/predict"` → Forecasting Agent
- `"alert/risk/warning"` → Alert Agent
- `"report/summary"` → Reporting Agent
- `"ocr/scan/document"` → OCR Agent
- `"sync/integration"` → Data Sync Agent
- `"reconcile/balance"` → Reconciliation Agent
- **Default** → AI CFO Agent

### 6. Streaming & Real-time Updates
- **Workflow Streaming:** Real-time progress updates during execution
- **Step-by-step Monitoring:** Track individual workflow steps
- **Performance Metrics:** Execution time and success rates
- **Error Handling:** Graceful failure recovery and reporting

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=ai_financial

# Run specific test categories
pytest tests/unit/
pytest tests/integration/
pytest tests/api/
```

## 📊 API Endpoints

When running the server, the following endpoints are available:

### Core System Endpoints
- `GET /` - System information
- `GET /health` - Health check
- `GET /api/v1/status` - Comprehensive system status

### Agent Management
- `POST /api/v1/agents/{agent_id}/invoke` - Invoke specific agent directly

### Intelligent Routing (NEW!)
- `POST /api/v1/intelligent/route` - **Intelligent routing - automatically determine best agent**
- `POST /api/v1/intelligent/analyze` - **Analyze what agent would be selected**
- `GET /api/v1/intelligent/stream` - **Stream intelligent routing execution**

### Workflow Management
- `POST /api/v1/workflows/{workflow_type}/execute` - Execute workflow (advisory/transactional)
- `GET /api/v1/workflows/{workflow_type}/stream` - Stream workflow execution

### Tool Management
- `GET /api/v1/tools` - List available tools
- `POST /api/v1/tools/{tool_name}/execute` - Execute specific tool

### Development & Testing
- `GET /api/v1/trace-test` - Test OpenTelemetry tracing

## 🧠 Intelligent Routing APIs

### Overview
The Intelligent Routing system automatically analyzes incoming requests and routes them to the most appropriate agent based on keyword analysis and context.

### Available Endpoints

#### 1. Intelligent Route Execution
```bash
# Automatically route and execute
curl -X POST http://localhost:8000/api/v1/intelligent/route \
  -H "Content-Type: application/json" \
  -d '{"message": "Analyze our financial health", "context": {"company_id": "abc123"}}'
```

#### 2. Routing Analysis (Preview)
```bash
# Analyze what agent would be selected without executing
curl -X POST http://localhost:8000/api/v1/intelligent/analyze \
  -H "Content-Type: application/json" \
  -d '{"message": "Forecast our revenue for next quarter"}'
```

#### 3. Streaming Intelligent Routing
```bash
# Stream the routing and execution process
curl "http://localhost:8000/api/v1/intelligent/stream?message=Generate%20a%20financial%20report"
```

### Routing Logic

The system uses keyword-based analysis to determine the best agent:

| Keywords | Agent | Confidence | Use Case |
|----------|-------|------------|----------|
| `forecast`, `predict`, `projection`, `trend`, `future` | Forecasting Agent | 90% | Financial forecasting |
| `alert`, `warning`, `risk`, `threshold`, `monitor` | Alert Agent | 90% | Risk monitoring |
| `report`, `summary`, `brief`, `dashboard`, `analysis` | Reporting Agent | 80% | Report generation |
| `ocr`, `scan`, `receipt`, `invoice`, `document` | OCR Agent | 90% | Document processing |
| `sync`, `integration`, `import`, `export`, `data` | Data Sync Agent | 80% | Data management |
| `reconcile`, `match`, `balance`, `statement` | Reconciliation Agent | 90% | Bank reconciliation |
| *Default* | AI CFO Agent | 70% | General financial queries |

### Response Format

#### Routing Analysis Response
```json
{
  "input_message": "Forecast our revenue for next quarter",
  "recommended_agent": "forecasting_agent",
  "confidence": 0.9,
  "keywords_found": ["forecast"],
  "analysis": {
    "type": "forecasting"
  },
  "available_agents": ["ai_cfo_agent", "forecasting_agent", "alert_agent", ...]
}
```

#### Streaming Response Format
```json
{"type": "analysis_started", "timestamp": "2024-01-01T12:00:00Z", "message": "Analyzing request..."}
{"type": "routing_analysis", "decision": "forecasting_agent", "confidence": 0.9, "keywords": ["forecast"]}
{"type": "execution_started", "agent": "forecasting_agent", "timestamp": "2024-01-01T12:00:01Z"}
{"type": "execution_completed", "agent": "forecasting_agent", "success": true, "timestamp": "2024-01-01T12:00:05Z"}
{"type": "final_result", "result": {...}, "timestamp": "2024-01-01T12:00:05Z"}
```

### Testing Scripts

Use the provided test scripts to verify the APIs:

```bash
# Python test script
python ai_financial/agents/advisory/test_intelligent_routing_api.py

# Bash test script
bash ai_financial/agents/advisory/curl_test_intelligent_routing.sh
```

## 🔍 Development

### Adding New Agents

1. Create agent class inheriting from `BaseAgent`
2. Implement required methods
3. Register with orchestrator

### Adding New Tools

1. Create tool class inheriting from `BaseTool`
2. Implement execution logic
3. Register with tool hub

### Code Quality

```bash
# Format code
black ai_financial/

# Sort imports
isort ai_financial/

# Lint code
flake8 ai_financial/

# Type checking
mypy ai_financial/
```

## 📚 Documentation

- **`QUICKSTART.md`**: Quick start guide
- **`ai_financial/README.md`**: Detailed package documentation
- **`tests/README.md`**: Testing documentation
- **API Documentation**: Available at `/docs` when server is running

## 🚨 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure package is installed with `pip install -e .`
2. **Configuration Errors**: Check `.env` file format and values
3. **API Key Issues**: Verify OpenAI API key is valid and has sufficient credits
4. **Database Connection**: Ensure PostgreSQL and Redis are running

### Debug Mode

Enable debug mode for detailed logging:

```bash
DEBUG=true ai-financial start
```

## 📈 Performance

### Optimization Tips

1. Use Redis for caching frequently accessed data
2. Configure appropriate concurrency limits
3. Monitor memory usage with large datasets
4. Use connection pooling for database access

### Monitoring & Observability

The system includes comprehensive monitoring and observability:

#### Distributed Tracing
- **OpenTelemetry Integration:** Full request tracing across agents
- **Span Correlation:** Track requests through multiple agent interactions
- **Performance Metrics:** Execution time and resource usage monitoring
- **Error Tracking:** Detailed error context and stack traces

#### Langfuse Integration
- **Workflow Visualization:** Visual representation of agent workflows
- **Node Execution Tracking:** Monitor individual workflow steps
- **LLM Interaction Monitoring:** Track AI model calls and responses
- **Debug Capabilities:** Interactive debugging of agent workflows

#### Logging & Health Monitoring
- **Structured Logging:** JSON-formatted logs with correlation IDs
- **Health Check Endpoints:** System status and component health
- **Real-time Metrics:** Performance and usage statistics
- **Alert Integration:** Proactive issue detection and notification

#### Demo vs Production Modes
- **Demo Mode:** Mock data, simulated responses for testing
- **Production Mode:** Real LLM integration, actual data processing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run quality checks
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the test cases for usage examples
- Contact the development team