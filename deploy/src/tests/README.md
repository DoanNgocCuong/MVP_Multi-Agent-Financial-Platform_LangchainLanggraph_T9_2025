# Tests Directory

## 📁 Overview

The `tests/` directory contains the comprehensive test suite for the AI Financial Multi-Agent System. It includes unit tests, integration tests, and system tests to ensure the reliability and correctness of all system components.

## 🏗️ Test Structure

```
tests/
├── __init__.py                    # Test package initialization
├── test_system_integration.py     # System integration tests
├── unit/                          # Unit tests (to be added)
│   ├── test_agents.py            # Agent unit tests
│   ├── test_tools.py             # Tool unit tests
│   ├── test_orchestrator.py      # Orchestrator unit tests
│   └── test_models.py            # Model unit tests
├── integration/                   # Integration tests (to be added)
│   ├── test_workflows.py         # Workflow integration tests
│   ├── test_api_endpoints.py     # API endpoint tests
│   └── test_database.py          # Database integration tests
├── fixtures/                      # Test fixtures and data (to be added)
│   ├── sample_data.py            # Sample financial data
│   ├── mock_responses.py         # Mock API responses
│   └── test_config.py            # Test configuration
└── conftest.py                   # Pytest configuration (to be added)
```

## 🧪 Test Categories

### 1. Unit Tests

Test individual components in isolation:

- **Agent Tests**: Test individual agent functionality
- **Tool Tests**: Test financial calculation tools
- **Model Tests**: Test data models and validation
- **Core Tests**: Test core infrastructure components

### 2. Integration Tests

Test component interactions:

- **Workflow Tests**: Test multi-step workflows
- **API Tests**: Test REST API endpoints
- **Database Tests**: Test database operations
- **Tool Hub Tests**: Test tool execution and management

### 3. System Tests

Test complete system functionality:

- **End-to-End Tests**: Test complete user workflows
- **Performance Tests**: Test system performance and scalability
- **Load Tests**: Test system under load
- **Security Tests**: Test security measures

## 🚀 Running Tests

### Prerequisites

```bash
# Install test dependencies
pip install -e ".[test]"

# Or install pytest directly
pip install pytest pytest-asyncio pytest-cov
```

### Basic Test Execution

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=ai_financial

# Run specific test file
pytest tests/test_system_integration.py

# Run specific test function
pytest tests/test_system_integration.py::test_basic_system_initialization
```

### Test Categories

```bash
# Run only unit tests
pytest tests/unit/

# Run only integration tests
pytest tests/integration/

# Run tests with specific markers
pytest -m "not slow"
pytest -m "integration"
```

### Coverage Reports

```bash
# Generate HTML coverage report
pytest --cov=ai_financial --cov-report=html

# Generate XML coverage report
pytest --cov=ai_financial --cov-report=xml

# Show coverage in terminal
pytest --cov=ai_financial --cov-report=term-missing
```

## 📝 Test Examples

### System Integration Test

```python
import pytest
import asyncio
from ai_financial.orchestrator.orchestrator import get_orchestrator
from ai_financial.agents.advisory.ai_cfo_agent import AICFOAgent
from ai_financial.mcp.tools.financial_tools import FinancialRatioTool

@pytest.mark.asyncio
async def test_basic_system_initialization():
    """Test basic system initialization and component registration."""
    # Initialize orchestrator
    orchestrator = get_orchestrator()
    
    # Register AI CFO agent
    ai_cfo = AICFOAgent(industry="healthcare")
    orchestrator.register_agent(ai_cfo)
    
    # Start system
    await orchestrator.start()
    
    # Verify system is running
    status = orchestrator.get_orchestrator_status()
    assert status["running"] is True
    assert "ai_cfo_agent" in status["agent_list"]
    
    # Cleanup
    await orchestrator.stop()
```

### Agent Unit Test

```python
import pytest
from ai_financial.agents.advisory.ai_cfo_agent import AICFOAgent

def test_ai_cfo_agent_initialization():
    """Test AI CFO agent initialization with different industries."""
    # Test healthcare industry
    agent = AICFOAgent(industry="healthcare")
    assert agent.agent_id == "ai_cfo_agent"
    assert agent.industry == "healthcare"
    assert "financial_analysis" in agent.get_capabilities()
    
    # Test automotive industry
    agent = AICFOAgent(industry="automotive")
    assert agent.industry == "automotive"
    
    # Test default industry
    agent = AICFOAgent()
    assert agent.industry == "general"
```

### Tool Unit Test

```python
import pytest
from ai_financial.mcp.tools.financial_tools import FinancialRatioTool

@pytest.mark.asyncio
async def test_financial_ratio_calculator():
    """Test financial ratio calculation tool."""
    tool = FinancialRatioTool()
    
    # Test current ratio calculation
    result = await tool.execute({
        "ratio_type": "current_ratio",
        "financial_data": {
            "current_assets": 150000,
            "current_liabilities": 75000
        }
    })
    
    assert result.success is True
    assert result.data["ratio"] == 2.0
    assert result.data["interpretation"] == "Strong liquidity position"
```

### API Integration Test

```python
import pytest
from fastapi.testclient import TestClient
from ai_financial.main import app

@pytest.fixture
def client():
    """Create test client for API testing."""
    return TestClient(app)

def test_health_endpoint(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_tool_execution_endpoint(client):
    """Test tool execution endpoint."""
    response = client.post(
        "/api/v1/tools/financial_ratio_calculator/execute",
        json={
            "parameters": {
                "ratio_type": "current_ratio",
                "financial_data": {
                    "current_assets": 100000,
                    "current_liabilities": 50000
                }
            }
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["ratio"] == 2.0
```

## 🔧 Test Configuration

### Pytest Configuration (`conftest.py`)

```python
import pytest
import asyncio
from ai_financial.core.config import settings

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def test_config():
    """Provide test configuration."""
    return {
        "environment": "test",
        "debug": True,
        "api_host": "127.0.0.1",
        "api_port": 8001,
        "llm": {
            "openai_model": "gpt-3.5-turbo",  # Use cheaper model for tests
            "openai_temperature": 0.0
        }
    }

@pytest.fixture
async def test_orchestrator():
    """Provide test orchestrator instance."""
    from ai_financial.orchestrator.orchestrator import get_orchestrator
    
    orchestrator = get_orchestrator()
    await orchestrator.start()
    yield orchestrator
    await orchestrator.stop()
```

### Test Fixtures

```python
# fixtures/sample_data.py
SAMPLE_FINANCIAL_DATA = {
    "current_assets": 150000,
    "current_liabilities": 75000,
    "total_assets": 500000,
    "total_equity": 300000,
    "revenue": 1000000,
    "net_income": 100000
}

SAMPLE_CASH_FLOWS = [
    {"period": "2024-01", "net_cash_flow": 25000},
    {"period": "2024-02", "net_cash_flow": 32000},
    {"period": "2024-03", "net_cash_flow": 28000}
]
```

## 📊 Test Data Management

### Sample Data

Create realistic test data for financial scenarios:

```python
# fixtures/sample_data.py
HEALTHCARE_COMPANY_DATA = {
    "industry": "healthcare",
    "revenue": 2000000,
    "current_ratio": 2.5,
    "debt_to_equity": 0.3,
    "gross_margin": 0.5
}

AUTOMOTIVE_COMPANY_DATA = {
    "industry": "automotive", 
    "revenue": 5000000,
    "current_ratio": 1.5,
    "debt_to_equity": 0.6,
    "inventory_turnover": 12
}
```

### Mock Responses

Mock external API responses for testing:

```python
# fixtures/mock_responses.py
MOCK_OPENAI_RESPONSE = {
    "choices": [{
        "message": {
            "content": "Based on the financial analysis, the company shows strong liquidity..."
        }
    }]
}

MOCK_DATABASE_RESPONSE = {
    "transactions": [
        {"amount": 15000, "type": "income", "date": "2024-01-01"},
        {"amount": 5000, "type": "expense", "date": "2024-01-02"}
    ]
}
```

## 🎯 Test Strategies

### 1. Test-Driven Development (TDD)

Write tests before implementing features:

```python
def test_new_financial_metric():
    """Test new financial metric calculation."""
    # Write test first
    tool = NewFinancialTool()
    result = tool.calculate_metric(sample_data)
    assert result["metric_value"] == expected_value
```

### 2. Behavior-Driven Development (BDD)

Use descriptive test names and scenarios:

```python
def test_ai_cfo_agent_provides_healthcare_insights():
    """Given a healthcare company with $2M revenue,
    When the AI CFO agent analyzes the financial health,
    Then it should provide industry-specific insights and recommendations."""
    pass
```

### 3. Property-Based Testing

Test with generated data:

```python
from hypothesis import given, strategies as st

@given(st.floats(min_value=0, max_value=1000000))
def test_financial_ratio_calculation(assets):
    """Test ratio calculation with various asset values."""
    tool = FinancialRatioTool()
    result = tool.calculate_current_ratio(assets, 50000)
    assert result >= 0
```

## 🔍 Test Debugging

### Debugging Failed Tests

```bash
# Run with debug output
pytest -v -s tests/test_system_integration.py

# Run with pdb debugger
pytest --pdb tests/test_system_integration.py

# Run specific test with debug
pytest -v -s --pdb tests/test_system_integration.py::test_basic_system_initialization
```

### Test Logging

```python
import logging

def test_with_logging():
    """Test with detailed logging."""
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    
    logger.info("Starting test")
    # Test logic here
    logger.info("Test completed")
```

## 📈 Performance Testing

### Load Testing

```python
import pytest
import asyncio
import time

@pytest.mark.asyncio
async def test_system_performance():
    """Test system performance under load."""
    orchestrator = get_orchestrator()
    await orchestrator.start()
    
    start_time = time.time()
    
    # Execute multiple requests concurrently
    tasks = []
    for i in range(10):
        task = orchestrator.route_request(f"Request {i}")
        tasks.append(task)
    
    results = await asyncio.gather(*tasks)
    
    end_time = time.time()
    duration = end_time - start_time
    
    assert duration < 5.0  # Should complete within 5 seconds
    assert all(result.get("success") for result in results)
    
    await orchestrator.stop()
```

### Memory Testing

```python
import pytest
import psutil
import os

def test_memory_usage():
    """Test memory usage during operations."""
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss
    
    # Perform memory-intensive operations
    # ...
    
    final_memory = process.memory_info().rss
    memory_increase = final_memory - initial_memory
    
    # Assert memory increase is reasonable
    assert memory_increase < 100 * 1024 * 1024  # Less than 100MB
```

## 🛡️ Security Testing

### Input Validation Testing

```python
def test_malicious_input_handling():
    """Test system handles malicious input safely."""
    tool = FinancialRatioTool()
    
    # Test with malicious input
    malicious_input = {
        "ratio_type": "<script>alert('xss')</script>",
        "financial_data": {"current_assets": "'; DROP TABLE users; --"}
    }
    
    result = tool.execute(malicious_input)
    # Should handle gracefully without executing malicious code
    assert result.success is False
    assert "error" in result
```

### Authentication Testing

```python
def test_authentication_required():
    """Test that protected endpoints require authentication."""
    client = TestClient(app)
    
    response = client.post(
        "/api/v1/agents/ai_cfo_agent/invoke",
        json={"message": "test"}
    )
    
    # Should require authentication
    assert response.status_code == 401
```

## 📋 Test Checklist

### Before Committing

- [ ] All tests pass
- [ ] Coverage is above 80%
- [ ] No flaky tests
- [ ] Performance tests pass
- [ ] Security tests pass
- [ ] Documentation is updated

### Test Quality

- [ ] Tests are readable and maintainable
- [ ] Tests cover edge cases
- [ ] Tests use appropriate fixtures
- [ ] Tests are isolated and independent
- [ ] Tests have descriptive names

## 🚀 Continuous Integration

### GitHub Actions Example

```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.11
    - name: Install dependencies
      run: |
        pip install -e ".[test]"
    - name: Run tests
      run: |
        pytest --cov=ai_financial --cov-report=xml
    - name: Upload coverage
      uses: codecov/codecov-action@v1
```

## 📚 Additional Resources

- **Pytest Documentation**: https://docs.pytest.org/
- **Testing Best Practices**: See project wiki
- **Coverage Reports**: Available in `htmlcov/` after running with coverage
- **Test Examples**: See existing test files for patterns
- **Mocking Guide**: See `fixtures/mock_responses.py` for examples

