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

### Two Main Workflows

#### Advisory Context (CEO Support)
- AI CFO Agent for financial analysis
- Forecasting and risk assessment
- Executive reporting and insights

#### Transactional Context (Automation)
- OCR processing for documents
- Data synchronization and standardization
- Automated accounting and reconciliation
- Compliance and audit support

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

- `GET /` - System information
- `GET /health` - Health check
- `POST /api/v1/agents/{agent_id}/invoke` - Invoke specific agent
- `POST /api/v1/workflows/{workflow_type}/execute` - Execute workflow
- `GET /api/v1/tools` - List available tools
- `POST /api/v1/tools/{tool_name}/execute` - Execute tool

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

### Monitoring

The system includes comprehensive monitoring:
- OpenTelemetry distributed tracing
- Langfuse LLM interaction tracking
- Structured logging with correlation IDs
- Health check endpoints

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