# AI Agents

## 📁 Overview

The `agents/` directory contains all AI agent implementations for the AI Financial Multi-Agent System. These agents are specialized for different financial tasks and contexts, providing intelligent automation and analysis capabilities.

## 🏗️ Directory Structure

```
agents/
├── __init__.py                    # Package initialization
├── advisory/                      # Advisory context agents
│   ├── __init__.py
│   └── ai_cfo_agent.py           # AI CFO agent implementation
└── document_processing/           # Document processing agents
    └── __pycache__/
```

## 🤖 Agent Architecture

### Base Agent Foundation

All agents inherit from `BaseAgent` in the core package, providing:

- **LangGraph Integration**: Workflow graph-based processing
- **Async Support**: Full async/await compatibility
- **State Management**: Agent state and context handling
- **LLM Integration**: OpenAI integration with error handling
- **Tracing**: OpenTelemetry distributed tracing
- **Logging**: Structured logging with correlation IDs

### Agent Lifecycle

1. **Initialization**: Agent setup and configuration
2. **Graph Building**: Define workflow graph structure
3. **Request Processing**: Handle incoming requests
4. **State Management**: Maintain agent state across operations
5. **Response Generation**: Format and return results

## 🧩 Agent Categories

### 1. Advisory Context Agents

Agents that provide financial advisory services and strategic insights.

#### AI CFO Agent (`advisory/ai_cfo_agent.py`)

The flagship agent providing comprehensive financial analysis and strategic recommendations.

**Key Features:**
- **Industry Specialization**: Tailored analysis for specific industries
- **Comprehensive Analysis**: Multi-faceted financial health assessment
- **Risk Assessment**: Proactive risk identification and mitigation
- **Strategic Recommendations**: Actionable business insights
- **Executive Reporting**: Board-ready financial reports

**Supported Industries:**
- `general`: General business analysis
- `healthcare`: Healthcare industry specialization
- `automotive`: Automotive industry specialization
- `pharmaceutical`: Pharmaceutical industry specialization

**Workflow Steps:**
1. **Request Analysis**: Classify and understand the request
2. **Data Gathering**: Collect relevant financial data
3. **Financial Analysis**: Perform comprehensive analysis
4. **Insight Generation**: Generate insights using LLM
5. **Risk Assessment**: Evaluate risks and opportunities
6. **Recommendations**: Provide strategic recommendations
7. **Response Formatting**: Format executive-level response

**Usage Example:**
```python
from ai_financial.agents.advisory.ai_cfo_agent import AICFOAgent

# Create agent for healthcare industry
ai_cfo = AICFOAgent(industry="healthcare")

# Register with orchestrator
orchestrator.register_agent(ai_cfo)

# Execute analysis
result = await orchestrator.route_request(
    request="Analyze our company's financial health and provide strategic recommendations",
    preferred_agent="ai_cfo_agent"
)
```

**Capabilities:**
- Financial health assessment
- Industry benchmarking
- Risk assessment and mitigation
- Strategic planning support
- Cash flow analysis
- Profitability analysis
- Liquidity analysis
- Compliance monitoring
- Investment analysis
- Scenario planning

### 2. Document Processing Agents

Agents that handle document processing and data extraction.

#### OCR Processing Agent (Planned)

Agent for processing financial documents using OCR technology.

**Planned Features:**
- Receipt processing and categorization
- Invoice data extraction
- Bank statement processing
- Document validation and verification
- Data standardization

#### Data Sync Agent (Planned)

Agent for synchronizing data from multiple sources.

**Planned Features:**
- Multi-source data integration
- Data validation and cleansing
- Real-time synchronization
- Conflict resolution
- Data quality monitoring

## 🔧 Agent Development

### Creating New Agents

#### 1. Define Agent Class

```python
from ai_financial.core.base_agent import BaseAgent
from langgraph.graph import StateGraph, END
from ai_financial.models.agent_models import AgentState

class MyCustomAgent(BaseAgent):
    def __init__(self, industry: str = "general"):
        self.industry = industry
        super().__init__(
            agent_id="my_custom_agent",
            name="My Custom Agent",
            description="Custom agent for specific financial tasks"
        )
    
    def _build_graph(self) -> StateGraph:
        """Build the agent workflow graph."""
        graph = StateGraph(AgentState)
        
        # Add nodes
        graph.add_node("analyze", self._analyze_request)
        graph.add_node("process", self._process_data)
        graph.add_node("generate", self._generate_response)
        
        # Add edges
        graph.set_entry_point("analyze")
        graph.add_edge("analyze", "process")
        graph.add_edge("process", "generate")
        graph.add_edge("generate", END)
        
        return graph
    
    async def _analyze_request(self, state: AgentState) -> AgentState:
        """Analyze the incoming request."""
        # Implementation here
        return state
    
    async def _process_data(self, state: AgentState) -> AgentState:
        """Process financial data."""
        # Implementation here
        return state
    
    async def _generate_response(self, state: AgentState) -> AgentState:
        """Generate final response."""
        # Implementation here
        return state
```

#### 2. Implement Required Methods

**`_build_graph()`**: Define the agent's workflow graph
```python
def _build_graph(self) -> StateGraph:
    graph = StateGraph(AgentState)
    
    # Add workflow nodes
    graph.add_node("step1", self._step1_function)
    graph.add_node("step2", self._step2_function)
    
    # Define workflow edges
    graph.set_entry_point("step1")
    graph.add_edge("step1", "step2")
    graph.add_edge("step2", END)
    
    return graph
```

**`_process_request()`**: Implement main processing logic
```python
async def _process_request(self, state: AgentState) -> AgentState:
    """Process the incoming request."""
    try:
        # Your processing logic here
        result = await self._perform_analysis(state)
        
        # Update state
        state.messages.append(AIMessage(content=result))
        state.completed_steps.append("processing")
        
        return state
    except Exception as e:
        state.error = str(e)
        return state
```

#### 3. Define Agent Capabilities

```python
def get_capabilities(self) -> List[str]:
    """Return list of agent capabilities."""
    return [
        "financial_analysis",
        "risk_assessment",
        "strategic_planning",
        "industry_benchmarking"
    ]
```

#### 4. Register with Orchestrator

```python
from ai_financial.orchestrator.orchestrator import get_orchestrator

# Create and register agent
orchestrator = get_orchestrator()
my_agent = MyCustomAgent(industry="healthcare")
orchestrator.register_agent(my_agent)
```

### Agent Best Practices

#### 1. Error Handling

```python
async def _process_request(self, state: AgentState) -> AgentState:
    try:
        # Main processing logic
        result = await self._perform_analysis(state)
        state.messages.append(AIMessage(content=result))
    except Exception as e:
        logger.error("Agent processing failed", error=str(e))
        state.error = f"Processing failed: {str(e)}"
    finally:
        state.completed_steps.append("processing")
    
    return state
```

#### 2. State Management

```python
async def _analyze_request(self, state: AgentState) -> AgentState:
    # Store analysis results in metadata
    state.metadata["analysis_results"] = {
        "request_type": "financial_health",
        "industry": self.industry,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    # Update current step
    state.current_step = "data_gathering"
    state.completed_steps.append("request_analysis")
    
    return state
```

#### 3. Logging and Tracing

```python
from ai_financial.core.logging import get_logger, get_tracer

logger = get_logger(__name__)
tracer = get_tracer(__name__)

async def _perform_analysis(self, state: AgentState) -> AgentState:
    with tracer.start_as_current_span("agent.analysis") as span:
        span.set_attribute("agent_id", self.agent_id)
        span.set_attribute("industry", self.industry)
        
        logger.info(
            "Starting financial analysis",
            agent_id=self.agent_id,
            industry=self.industry,
            request_id=state.context.session_id
        )
        
        # Analysis logic here
        
        logger.info(
            "Analysis completed",
            agent_id=self.agent_id,
            duration=span.get_span_context().trace_id
        )
        
        return state
```

## 🎯 Agent Specialization

### Industry-Specific Agents

#### Healthcare Industry

```python
healthcare_cfo = AICFOAgent(industry="healthcare")

# Specialized metrics for healthcare:
# - Days in Accounts Receivable
# - Revenue per Patient
# - Cost per Patient
# - Regulatory compliance metrics
```

#### Automotive Industry

```python
automotive_cfo = AICFOAgent(industry="automotive")

# Specialized metrics for automotive:
# - Inventory turnover
# - Dealer performance metrics
# - Warranty costs
# - Supply chain efficiency
```

#### Pharmaceutical Industry

```python
pharma_cfo = AICFOAgent(industry="pharmaceutical")

# Specialized metrics for pharmaceutical:
# - R&D expense ratio
# - Drug development pipeline
# - Regulatory approval timelines
# - Patent portfolio value
```

### Context-Specific Agents

#### Advisory Context

Agents focused on strategic decision-making and executive support:

- **AI CFO Agent**: Comprehensive financial analysis
- **Forecasting Agent**: Financial projections and modeling
- **Risk Assessment Agent**: Risk identification and mitigation
- **Reporting Agent**: Executive reporting and dashboards

#### Transactional Context

Agents focused on operational automation and data processing:

- **OCR Processing Agent**: Document processing and data extraction
- **Data Sync Agent**: Multi-source data integration
- **Accounting Agent**: Automated accounting processes
- **Reconciliation Agent**: Bank statement reconciliation
- **Compliance Agent**: Regulatory compliance and audit support

## 🔌 Agent Integration

### Orchestrator Integration

```python
from ai_financial.orchestrator.orchestrator import get_orchestrator

orchestrator = get_orchestrator()

# Register multiple agents
orchestrator.register_agent(AICFOAgent(industry="healthcare"))
orchestrator.register_agent(ForecastingAgent())
orchestrator.register_agent(RiskAssessmentAgent())

# Route requests to appropriate agents
result = await orchestrator.route_request(
    request="Provide comprehensive financial analysis",
    preferred_agent="ai_cfo_agent"
)
```

### Tool Integration

```python
from ai_financial.mcp.hub import get_tool_hub

tool_hub = get_tool_hub()

# Agents can use tools for calculations
result = await tool_hub.execute_tool(
    tool_name="financial_ratio_calculator",
    parameters={
        "ratio_type": "current_ratio",
        "financial_data": financial_data
    }
)
```

### Workflow Integration

```python
# Agents participate in workflows
result = await orchestrator.route_request(
    request="Execute advisory workflow",
    workflow_type="advisory"
)

# Workflow steps:
# 1. Data Sync Agent
# 2. AI CFO Agent (analysis)
# 3. Forecasting Agent
# 4. Risk Assessment Agent
# 5. Reporting Agent
```

## 🧪 Testing Agents

### Unit Testing

```python
import pytest
from ai_financial.agents.advisory.ai_cfo_agent import AICFOAgent

def test_ai_cfo_agent_initialization():
    """Test AI CFO agent initialization."""
    agent = AICFOAgent(industry="healthcare")
    assert agent.agent_id == "ai_cfo_agent"
    assert agent.industry == "healthcare"
    assert "financial_analysis" in agent.get_capabilities()

@pytest.mark.asyncio
async def test_agent_workflow():
    """Test agent workflow execution."""
    agent = AICFOAgent(industry="healthcare")
    
    # Test workflow graph building
    graph = agent._build_graph()
    assert graph is not None
    
    # Test request processing
    state = AgentState(messages=[HumanMessage(content="Test request")])
    result = await agent._process_request(state)
    assert result is not None
```

### Integration Testing

```python
@pytest.mark.asyncio
async def test_agent_orchestrator_integration():
    """Test agent integration with orchestrator."""
    orchestrator = get_orchestrator()
    agent = AICFOAgent(industry="healthcare")
    
    orchestrator.register_agent(agent)
    await orchestrator.start()
    
    result = await orchestrator.route_request(
        request="Analyze financial health",
        preferred_agent="ai_cfo_agent"
    )
    
    assert result.get("success") is True
    await orchestrator.stop()
```

## 📊 Agent Performance

### Monitoring

```python
from ai_financial.core.logging import get_logger

logger = get_logger(__name__)

# Monitor agent performance
logger.info(
    "Agent performance metrics",
    agent_id="ai_cfo_agent",
    response_time=1.2,
    success_rate=0.95,
    requests_processed=1000
)
```

### Optimization

```python
# Optimize agent performance
class OptimizedAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_id="optimized_agent",
            name="Optimized Agent",
            description="Performance-optimized agent"
        )
        # Cache frequently used data
        self._cache = {}
    
    async def _process_request(self, state: AgentState) -> AgentState:
        # Use caching for repeated operations
        cache_key = self._generate_cache_key(state)
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        # Process request
        result = await self._perform_analysis(state)
        self._cache[cache_key] = result
        
        return result
```

## 🚀 Deployment

### Agent Configuration

```python
# Configure agents for different environments
if settings.environment == "production":
    # Production configuration
    agent = AICFOAgent(industry="healthcare")
    agent.llm.temperature = 0.1  # More deterministic
else:
    # Development configuration
    agent = AICFOAgent(industry="healthcare")
    agent.llm.temperature = 0.3  # More creative
```

### Scaling

```python
# Scale agents horizontally
orchestrator = get_orchestrator()

# Register multiple instances
for i in range(3):
    agent = AICFOAgent(industry="healthcare")
    agent.agent_id = f"ai_cfo_agent_{i}"
    orchestrator.register_agent(agent)
```

## 📚 Additional Resources

- **Base Agent Documentation**: See `core/base_agent.py`
- **LangGraph Documentation**: https://langchain-ai.github.io/langgraph/
- **Agent Models**: See `models/agent_models.py`
- **Orchestrator Integration**: See `orchestrator/orchestrator.py`
- **Tool Integration**: See `mcp/hub.py`

