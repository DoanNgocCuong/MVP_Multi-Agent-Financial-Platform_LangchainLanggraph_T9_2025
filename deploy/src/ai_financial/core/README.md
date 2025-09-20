# Core Infrastructure

## 📁 Overview

The `core/` directory contains the fundamental infrastructure components that provide the foundation for the entire AI Financial Multi-Agent System. These components handle configuration, logging, database connections, and provide the base classes for all agents.

## 🏗️ Directory Structure

```
core/
├── __init__.py           # Package initialization
├── base_agent.py         # Base agent class with LangGraph integration
├── config.py             # Configuration management with environment variables
├── database.py           # Database connection and management
└── logging.py            # Logging, tracing, and observability setup
```

## 🧩 Core Components

### 1. Base Agent (`base_agent.py`)

The foundation class for all AI agents in the system, providing LangGraph integration and common functionality.

#### Key Features:
- **LangGraph Integration**: Built-in workflow graph support
- **Async Support**: Full async/await compatibility
- **State Management**: Agent state and context handling
- **LLM Integration**: OpenAI integration with error handling
- **Tracing**: OpenTelemetry distributed tracing
- **Logging**: Structured logging with correlation IDs

#### Usage Example:
```python
from ai_financial.core.base_agent import BaseAgent
from langgraph.graph import StateGraph, END
from ai_financial.models.agent_models import AgentState

class MyCustomAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_id="my_agent",
            name="My Custom Agent",
            description="Custom agent for specific tasks"
        )
    
    def _build_graph(self) -> StateGraph:
        """Build the agent workflow graph."""
        graph = StateGraph(AgentState)
        
        # Add nodes
        graph.add_node("process", self._process_request)
        graph.add_node("validate", self._validate_input)
        
        # Add edges
        graph.set_entry_point("validate")
        graph.add_edge("validate", "process")
        graph.add_edge("process", END)
        
        return graph
    
    async def _process_request(self, state: AgentState) -> AgentState:
        """Process the incoming request."""
        # Your agent logic here
        state.messages.append(AIMessage(content="Response"))
        return state
```

#### Abstract Methods:
- `_build_graph()`: Define the agent's workflow graph
- `_process_request()`: Implement the main processing logic

#### Properties:
- `agent_id`: Unique identifier for the agent
- `name`: Human-readable agent name
- `description`: Agent description and capabilities
- `llm`: OpenAI LLM instance
- `graph`: LangGraph workflow graph

### 2. Configuration (`config.py`)

Centralized configuration management using Pydantic settings with environment variable support.

#### Configuration Classes:

##### `DatabaseSettings`
```python
class DatabaseSettings(BaseSettings):
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "ai_financial"
    postgres_password: str = ""
    postgres_db: str = "ai_financial"
    mongodb_url: str = "mongodb://localhost:27017"
    redis_url: str = "redis://localhost:6379"
```

##### `LLMSettings`
```python
class LLMSettings(BaseSettings):
    openai_api_key: str = ""
    openai_model: str = "gpt-4-turbo-preview"
    openai_temperature: float = 0.1
    openai_max_tokens: int = 4000
    langfuse_secret_key: str = ""
    langfuse_public_key: str = ""
```

##### `SecuritySettings`
```python
class SecuritySettings(BaseSettings):
    secret_key: str = ""  # Auto-generated if not provided
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    encryption_key: str = ""
```

##### `MonitoringSettings`
```python
class MonitoringSettings(BaseSettings):
    otel_service_name: str = "ai-financial-system"
    otel_exporter_otlp_endpoint: str = ""
    log_level: str = "INFO"
    log_format: str = "json"
    enable_metrics: bool = True
```

#### Usage Example:
```python
from ai_financial.core.config import settings

# Access configuration
print(f"API Host: {settings.api_host}")
print(f"API Port: {settings.api_port}")
print(f"OpenAI Model: {settings.llm.openai_model}")
print(f"Database URL: {settings.database.postgres_url}")

# Check if OpenAI is configured
if settings.llm.has_openai_key:
    print("OpenAI API key is configured")
else:
    print("Running in demo mode")

# Get database URL by type
postgres_url = settings.get_database_url("postgres")
mongodb_url = settings.get_database_url("mongodb")
redis_url = settings.get_database_url("redis")
```

#### Environment Variables:
```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
ENVIRONMENT=development
DEBUG=true

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4-turbo-preview
OPENAI_TEMPERATURE=0.1

# Database Configuration
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=ai_financial
POSTGRES_PASSWORD=your_password
POSTGRES_DB=ai_financial

# Security
SECRET_KEY=your_secret_key_here_at_least_32_characters_long

# Monitoring
LOG_LEVEL=INFO
LANGFUSE_SECRET_KEY=your_langfuse_secret_key
```

### 3. Database (`database.py`)

Database connection management and utilities for PostgreSQL, MongoDB, and Redis.

#### Features:
- **Connection Pooling**: Efficient database connections
- **Async Support**: Async database operations
- **Multiple Databases**: PostgreSQL, MongoDB, Redis support
- **Health Checks**: Database connectivity monitoring
- **Error Handling**: Robust error handling and retry logic

#### Usage Example:
```python
from ai_financial.core.database import get_database_connection

# Get database connection
async with get_database_connection("postgres") as conn:
    # Execute queries
    result = await conn.fetch("SELECT * FROM transactions")
    
# Health check
health_status = await check_database_health()
print(f"Database health: {health_status}")
```

### 4. Logging (`logging.py`)

Comprehensive logging and observability setup with OpenTelemetry integration.

#### Features:
- **Structured Logging**: JSON-formatted logs with correlation IDs
- **OpenTelemetry**: Distributed tracing across services
- **Langfuse Integration**: LLM interaction monitoring
- **Log Levels**: Configurable log levels and formatting
- **Correlation IDs**: Request tracing across components

#### Usage Example:
```python
from ai_financial.core.logging import get_logger, get_tracer

# Get logger
logger = get_logger(__name__)

# Structured logging
logger.info(
    "Operation completed",
    agent_id="ai_cfo_agent",
    duration=1.5,
    success=True,
    user_id="user123"
)

# Distributed tracing
tracer = get_tracer(__name__)
with tracer.start_as_current_span("operation_name") as span:
    span.set_attribute("key", "value")
    span.add_event("operation_started")
    
    # Your operation here
    
    span.add_event("operation_completed")
```

#### Logging Configuration:
```python
# Setup logging
setup_logging()

# Setup tracing
setup_tracing()

# Get logger with context
logger = get_logger(__name__)

# Log with structured data
logger.info(
    "Agent processing started",
    agent_id="ai_cfo_agent",
    request_id="req_123",
    user_id="user_456"
)
```

## 🔧 Configuration Management

### Environment-Based Configuration

The system supports multiple environments:

```python
# Development
ENVIRONMENT=development
DEBUG=true

# Staging
ENVIRONMENT=staging
DEBUG=false

# Production
ENVIRONMENT=production
DEBUG=false
```

### Configuration Validation

All configuration is validated using Pydantic:

```python
from ai_financial.core.config import settings

# Validate configuration
try:
    # Configuration is automatically validated on import
    print("Configuration is valid")
except ValidationError as e:
    print(f"Configuration error: {e}")
```

### Secret Management

Sensitive configuration is handled securely:

```python
# Auto-generated secret key for development
if not settings.security.secret_key:
    # System generates a secure key automatically
    print("Using auto-generated secret key for development")

# Production secret key
SECRET_KEY=your_production_secret_key_here
```

## 🚀 Initialization

### System Setup

Initialize the core components:

```python
from ai_financial.core.config import settings
from ai_financial.core.logging import setup_logging, setup_tracing
from ai_financial.core.database import initialize_databases

# Setup logging and tracing
setup_logging()
setup_tracing()

# Initialize databases
await initialize_databases()

# Verify configuration
if not settings.llm.has_openai_key:
    logger.warning("OpenAI API key not configured - running in demo mode")
```

### Agent Initialization

Create agents using the base class:

```python
from ai_financial.core.base_agent import BaseAgent

# Initialize agent
agent = MyCustomAgent()

# Check agent capabilities
capabilities = agent.get_capabilities()
print(f"Agent capabilities: {capabilities}")

# Get agent information
print(f"Agent ID: {agent.agent_id}")
print(f"Agent Name: {agent.name}")
print(f"Agent Description: {agent.description}")
```

## 🔍 Monitoring and Observability

### Logging Levels

Configure logging levels:

```env
# Development
LOG_LEVEL=DEBUG

# Production
LOG_LEVEL=INFO
```

### Tracing Configuration

Setup distributed tracing:

```env
# OpenTelemetry
OTEL_SERVICE_NAME=ai-financial-system
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# Langfuse
LANGFUSE_SECRET_KEY=your_secret_key
LANGFUSE_PUBLIC_KEY=your_public_key
LANGFUSE_HOST=https://cloud.langfuse.com
```

### Health Monitoring

Monitor system health:

```python
from ai_financial.core.database import check_database_health
from ai_financial.core.logging import get_logger

logger = get_logger(__name__)

# Check database health
db_health = await check_database_health()
logger.info("Database health check", status=db_health)

# Monitor agent performance
logger.info(
    "Agent performance",
    agent_id="ai_cfo_agent",
    response_time=1.2,
    success_rate=0.95
)
```

## 🛡️ Security

### Secret Management

Handle sensitive data securely:

```python
from ai_financial.core.config import settings

# Check if secrets are configured
if settings.security.secret_key:
    print("Secret key is configured")
else:
    print("Using auto-generated secret key")

# Validate secret key strength
if len(settings.security.secret_key) < 32:
    raise ValueError("Secret key must be at least 32 characters")
```

### Database Security

Secure database connections:

```python
# Use environment variables for credentials
POSTGRES_PASSWORD=secure_password_here
REDIS_URL=redis://localhost:6379
```

## 🧪 Testing

### Unit Testing

Test core components:

```python
import pytest
from ai_financial.core.config import settings
from ai_financial.core.base_agent import BaseAgent

def test_configuration_loading():
    """Test configuration loading."""
    assert settings.api_host == "0.0.0.0"
    assert settings.api_port == 8000

def test_base_agent_initialization():
    """Test base agent initialization."""
    agent = BaseAgent(
        agent_id="test_agent",
        name="Test Agent",
        description="Test agent for unit testing"
    )
    assert agent.agent_id == "test_agent"
    assert agent.name == "Test Agent"
```

### Integration Testing

Test component integration:

```python
@pytest.mark.asyncio
async def test_database_connection():
    """Test database connection."""
    from ai_financial.core.database import get_database_connection
    
    async with get_database_connection("postgres") as conn:
        result = await conn.fetch("SELECT 1")
        assert result[0][0] == 1
```

## 📚 Additional Resources

- **Pydantic Settings**: https://pydantic-docs.helpmanual.io/usage/settings/
- **OpenTelemetry**: https://opentelemetry.io/
- **Langfuse**: https://langfuse.com/
- **LangGraph**: https://langchain-ai.github.io/langgraph/
- **FastAPI**: https://fastapi.tiangolo.com/

