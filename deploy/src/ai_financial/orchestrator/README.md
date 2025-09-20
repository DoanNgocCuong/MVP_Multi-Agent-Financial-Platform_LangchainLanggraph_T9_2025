# Agent Orchestrator

## 📁 Overview

The `orchestrator/` directory contains the central coordination system for the AI Financial Multi-Agent System. It manages multi-agent workflows, handles request routing, and coordinates complex financial processes across different agents and tools.

## 🏗️ Directory Structure

```
orchestrator/
├── __init__.py           # Package initialization
├── orchestrator.py       # Main orchestrator implementation
├── workflow_engine.py    # Workflow management and execution
└── context_manager.py    # Context and state management
```

## 🧩 Core Components

### 1. Agent Orchestrator (`orchestrator.py`)

The central coordination system that manages all agents and workflows.

#### Key Features:
- **Agent Management**: Register, unregister, and manage agents
- **Request Routing**: Intelligent routing of requests to appropriate agents
- **Workflow Execution**: Execute complex multi-step workflows
- **Concurrency Control**: Manage concurrent agent execution
- **State Management**: Track agent and workflow states
- **Error Handling**: Robust error handling and recovery

#### Usage Example:
```python
from ai_financial.orchestrator.orchestrator import get_orchestrator
from ai_financial.agents.advisory.ai_cfo_agent import AICFOAgent

# Get orchestrator instance
orchestrator = get_orchestrator()

# Register agents
ai_cfo = AICFOAgent(industry="healthcare")
orchestrator.register_agent(ai_cfo)

# Start orchestrator
await orchestrator.start()

# Route requests
result = await orchestrator.route_request(
    request="Analyze our company's financial health",
    preferred_agent="ai_cfo_agent"
)

# Execute workflows
workflow_result = await orchestrator.route_request(
    request="Provide comprehensive financial analysis",
    workflow_type="advisory"
)

# Stop orchestrator
await orchestrator.stop()
```

#### Orchestrator Methods:

**`register_agent(agent: BaseAgent)`**
```python
# Register a new agent
orchestrator.register_agent(MyCustomAgent())
```

**`unregister_agent(agent_id: str)`**
```python
# Unregister an agent
orchestrator.unregister_agent("my_agent")
```

**`route_request(request: Union[str, Dict], context: Optional[AgentContext] = None, preferred_agent: Optional[str] = None, workflow_type: Optional[str] = None)`**
```python
# Route request to specific agent
result = await orchestrator.route_request(
    request="Analyze financial health",
    preferred_agent="ai_cfo_agent"
)

# Route request to workflow
result = await orchestrator.route_request(
    request="Comprehensive analysis",
    workflow_type="advisory"
)

# Intelligent routing
result = await orchestrator.route_request(
    request="What is our current ratio?"
)
```

**`stream_workflow(workflow_type: str, request: Union[str, Dict], context: Optional[AgentContext] = None)`**
```python
# Stream workflow execution
async for update in orchestrator.stream_workflow("advisory", "Analyze financial health"):
    print(f"Update: {update}")
```

### 2. Workflow Engine (`workflow_engine.py`)

Manages complex multi-step workflows with approval processes and error handling.

#### Key Features:
- **Workflow Definition**: Define complex multi-step processes
- **State Management**: Track workflow state and progress
- **Approval Processes**: Human-in-the-loop (HITL) controls
- **Error Recovery**: Handle and recover from workflow errors
- **Parallel Execution**: Execute workflow steps in parallel when possible
- **Rollback Support**: Rollback failed workflow steps

#### Usage Example:
```python
from ai_financial.orchestrator.workflow_engine import WorkflowEngine

# Create workflow engine
workflow_engine = WorkflowEngine()

# Define workflow
workflow = {
    "name": "advisory_workflow",
    "steps": [
        {"name": "data_sync", "agent": "data_sync_agent"},
        {"name": "analysis", "agent": "ai_cfo_agent"},
        {"name": "forecasting", "agent": "forecasting_agent"},
        {"name": "reporting", "agent": "reporting_agent"}
    ],
    "approval_points": ["analysis", "forecasting"]
}

# Execute workflow
result = await workflow_engine.execute_workflow(workflow, context)
```

#### Workflow Types:

##### Advisory Workflow
Multi-step process for CEO support and strategic analysis:

```
Data Sync → Financial Analysis → Forecasting → Risk Assessment → Executive Reporting
```

**Steps:**
1. **Data Synchronization**: Sync latest financial data
2. **Financial Analysis**: Comprehensive financial health analysis
3. **Forecasting**: 13-week cash flow and 12-month P&L projections
4. **Risk Assessment**: Identify risks and opportunities
5. **Executive Reporting**: Generate board-ready reports

##### Transactional Workflow
Automated accounting and transaction processing:

```
OCR Processing → Standardization → Accounting → Reconciliation → Compliance
```

**Steps:**
1. **OCR Processing**: Extract data from financial documents
2. **Standardization**: Standardize and validate data
3. **Accounting**: Create accounting entries
4. **Reconciliation**: Reconcile with bank statements
5. **Compliance**: Validate compliance and create audit trail

### 3. Context Manager (`context_manager.py`)

Manages execution context and shared state across agents and workflows.

#### Key Features:
- **Context Creation**: Create and manage execution contexts
- **State Sharing**: Share state between agents and workflows
- **Session Management**: Manage user sessions and permissions
- **Data Persistence**: Persist context data across operations
- **Security**: Handle authentication and authorization

#### Usage Example:
```python
from ai_financial.orchestrator.context_manager import ContextManager

# Create context manager
context_manager = ContextManager()

# Create execution context
context = context_manager.create_context(
    agent_id="ai_cfo_agent",
    user_id="user_123",
    company_id="company_456",
    permissions=["read_financial_data", "write_reports"]
)

# Share state between agents
context_manager.set_shared_state(
    context.session_id,
    "financial_data",
    {"revenue": 1000000, "expenses": 800000}
)

# Get shared state
financial_data = context_manager.get_shared_state(
    context.session_id,
    "financial_data"
)
```

## 🔧 Orchestrator Configuration

### Concurrency Settings

```python
from ai_financial.core.config import settings

# Configure concurrent agent limits
settings.workflow.max_concurrent_agents = 10

# Configure workflow timeouts
settings.workflow.workflow_timeout = 300  # 5 minutes
```

### Agent Registration

```python
# Register multiple agents
orchestrator = get_orchestrator()

# Advisory agents
orchestrator.register_agent(AICFOAgent(industry="healthcare"))
orchestrator.register_agent(ForecastingAgent())
orchestrator.register_agent(RiskAssessmentAgent())
orchestrator.register_agent(ReportingAgent())

# Transactional agents
orchestrator.register_agent(OCRProcessingAgent())
orchestrator.register_agent(DataSyncAgent())
orchestrator.register_agent(AccountingAgent())
orchestrator.register_agent(ReconciliationAgent())
orchestrator.register_agent(ComplianceAgent())
```

## 🎯 Request Routing

### Intelligent Routing

The orchestrator uses intelligent routing to determine the best agent for each request:

```python
# Keyword-based routing
if "forecast" in request.lower():
    return await self._route_to_agent("forecasting_agent", request, context)
elif "alert" in request.lower():
    return await self._route_to_agent("alert_agent", request, context)
elif "report" in request.lower():
    return await self._route_to_agent("reporting_agent", request, context)
else:
    # Default to AI CFO agent
    return await self._route_to_agent("ai_cfo_agent", request, context)
```

### Direct Agent Routing

```python
# Route directly to specific agent
result = await orchestrator.route_request(
    request="Analyze our financial health",
    preferred_agent="ai_cfo_agent"
)
```

### Workflow Routing

```python
# Route to workflow
result = await orchestrator.route_request(
    request="Provide comprehensive financial analysis",
    workflow_type="advisory"
)
```

## ⚡ Workflow Execution

### Advisory Workflow

```python
async def _execute_advisory_workflow(self, workflow_state: WorkflowState) -> Dict[str, Any]:
    """Execute advisory workflow for CEO support."""
    results = {}
    
    # Step 1: Data synchronization
    if "data_sync_agent" in self.agents:
        sync_result = await self.agents["data_sync_agent"].invoke(
            "Sync latest financial data for analysis", context
        )
        results["data_sync"] = sync_result
        workflow_state.complete_step("data_sync")
    
    # Step 2: Financial analysis
    if "ai_cfo_agent" in self.agents:
        analysis_result = await self.agents["ai_cfo_agent"].invoke(request, context)
        results["analysis"] = analysis_result
        workflow_state.complete_step("analysis")
    
    # Step 3: Forecasting
    if "forecasting_agent" in self.agents:
        forecast_result = await self.agents["forecasting_agent"].invoke(
            "Generate financial forecasts based on current data", context
        )
        results["forecasting"] = forecast_result
        workflow_state.complete_step("forecasting")
    
    # Step 4: Risk assessment
    if "alert_agent" in self.agents:
        alert_result = await self.agents["alert_agent"].invoke(
            "Check for financial risks and opportunities", context
        )
        results["alerts"] = alert_result
        workflow_state.complete_step("alerts")
    
    # Step 5: Executive reporting
    if "reporting_agent" in self.agents:
        report_result = await self.agents["reporting_agent"].invoke(
            "Generate executive financial report", context
        )
        results["report"] = report_result
        workflow_state.complete_step("reporting")
    
    return {
        "success": True,
        "workflow_type": "advisory",
        "workflow_id": workflow_state.workflow_id,
        "results": results,
        "completed_steps": workflow_state.steps_completed,
    }
```

### Transactional Workflow

```python
async def _execute_transactional_workflow(self, workflow_state: WorkflowState) -> Dict[str, Any]:
    """Execute transactional workflow for automation."""
    results = {}
    
    # Step 1: OCR/Document processing
    if "ocr_agent" in self.agents:
        ocr_result = await self.agents["ocr_agent"].invoke(request, context)
        results["ocr_processing"] = ocr_result
        workflow_state.complete_step("ocr_processing")
    
    # Step 2: Data standardization
    if "data_sync_agent" in self.agents:
        standardization_result = await self.agents["data_sync_agent"].invoke(
            "Standardize and validate processed data", context
        )
        results["standardization"] = standardization_result
        workflow_state.complete_step("standardization")
    
    # Step 3: Accounting automation
    if "accounting_agent" in self.agents:
        accounting_result = await self.agents["accounting_agent"].invoke(
            "Create accounting entries from processed data", context
        )
        results["accounting"] = accounting_result
        workflow_state.complete_step("accounting")
    
    # Step 4: Reconciliation
    if "reconciliation_agent" in self.agents:
        reconciliation_result = await self.agents["reconciliation_agent"].invoke(
            "Reconcile transactions with bank statements", context
        )
        results["reconciliation"] = reconciliation_result
        workflow_state.complete_step("reconciliation")
    
    # Step 5: Compliance and audit
    if "compliance_agent" in self.agents:
        compliance_result = await self.agents["compliance_agent"].invoke(
            "Validate compliance and create audit trail", context
        )
        results["compliance"] = compliance_result
        workflow_state.complete_step("compliance")
    
    return {
        "success": True,
        "workflow_type": "transactional",
        "workflow_id": workflow_state.workflow_id,
        "results": results,
        "completed_steps": workflow_state.steps_completed,
    }
```

## 📊 Workflow Streaming

### Real-time Updates

```python
async def stream_workflow(
    self,
    workflow_type: str,
    request: Union[str, Dict[str, Any]],
    context: Optional[AgentContext] = None,
):
    """Stream workflow execution for real-time updates."""
    
    # Create workflow state
    workflow_state = WorkflowState(
        workflow_type=workflow_type,
        context=context,
        data={"request": request},
        status=AgentStatus.PROCESSING,
    )
    
    # Store workflow
    self.active_workflows[workflow_state.workflow_id] = workflow_state
    
    # Yield initial status
    yield {
        "type": "workflow_started",
        "workflow_id": workflow_state.workflow_id,
        "workflow_type": workflow_type,
        "timestamp": datetime.utcnow().isoformat(),
    }
    
    # Execute workflow with streaming
    if workflow_type == "advisory":
        async for update in self._stream_advisory_workflow(workflow_state):
            yield update
    elif workflow_type == "transactional":
        async for update in self._stream_transactional_workflow(workflow_state):
            yield update
    
    # Yield completion status
    yield {
        "type": "workflow_completed",
        "workflow_id": workflow_state.workflow_id,
        "status": workflow_state.status.value,
        "completed_steps": workflow_state.steps_completed,
        "timestamp": datetime.utcnow().isoformat(),
    }
```

### Streaming Updates

```python
# Stream workflow execution
async for update in orchestrator.stream_workflow("advisory", "Analyze financial health"):
    if update["type"] == "step_started":
        print(f"Started step: {update['step']}")
    elif update["type"] == "step_completed":
        print(f"Completed step: {update['step']}")
    elif update["type"] == "workflow_completed":
        print("Workflow completed successfully")
```

## 🔍 State Management

### Workflow State

```python
class WorkflowState(BaseModel):
    workflow_id: str = Field(default_factory=lambda: str(uuid4()))
    workflow_type: str
    context: AgentContext
    data: Dict[str, Any] = Field(default_factory=dict)
    status: AgentStatus
    current_step: Optional[str] = None
    steps_completed: List[str] = Field(default_factory=list)
    pending_approvals: List[Dict[str, Any]] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    def complete_step(self, step_name: str):
        """Mark a step as completed."""
        if step_name not in self.steps_completed:
            self.steps_completed.append(step_name)
        self.current_step = None
        self.updated_at = datetime.utcnow()
    
    def set_status(self, status: AgentStatus):
        """Set workflow status."""
        self.status = status
        self.updated_at = datetime.utcnow()
    
    def set_error(self, error: str):
        """Set workflow error."""
        self.status = AgentStatus.FAILED
        self.data["error"] = error
        self.updated_at = datetime.utcnow()
```

### Context Management

```python
class ContextManager:
    def __init__(self):
        self.contexts: Dict[str, AgentContext] = {}
        self.shared_states: Dict[str, Dict[str, Any]] = {}
    
    def create_context(
        self,
        agent_id: str,
        user_id: str,
        company_id: str,
        permissions: List[str],
        session_id: Optional[str] = None,
    ) -> AgentContext:
        """Create new execution context."""
        if session_id is None:
            session_id = str(uuid4())
        
        context = AgentContext(
            agent_id=agent_id,
            session_id=session_id,
            user_id=user_id,
            company_id=company_id,
            permissions=permissions,
            state={},
        )
        
        self.contexts[session_id] = context
        return context
    
    def get_context(self, session_id: str) -> Optional[AgentContext]:
        """Get execution context by session ID."""
        return self.contexts.get(session_id)
    
    def set_shared_state(self, session_id: str, key: str, value: Any):
        """Set shared state for session."""
        if session_id not in self.shared_states:
            self.shared_states[session_id] = {}
        self.shared_states[session_id][key] = value
    
    def get_shared_state(self, session_id: str, key: str) -> Any:
        """Get shared state for session."""
        return self.shared_states.get(session_id, {}).get(key)
```

## 🧪 Testing Orchestrator

### Unit Testing

```python
import pytest
from ai_financial.orchestrator.orchestrator import get_orchestrator
from ai_financial.agents.advisory.ai_cfo_agent import AICFOAgent

@pytest.mark.asyncio
async def test_orchestrator_initialization():
    """Test orchestrator initialization."""
    orchestrator = get_orchestrator()
    assert orchestrator is not None
    assert orchestrator._running is False

@pytest.mark.asyncio
async def test_agent_registration():
    """Test agent registration."""
    orchestrator = get_orchestrator()
    agent = AICFOAgent(industry="healthcare")
    
    orchestrator.register_agent(agent)
    assert "ai_cfo_agent" in orchestrator.agents
    assert orchestrator.agents["ai_cfo_agent"] == agent

@pytest.mark.asyncio
async def test_request_routing():
    """Test request routing."""
    orchestrator = get_orchestrator()
    agent = AICFOAgent(industry="healthcare")
    orchestrator.register_agent(agent)
    
    await orchestrator.start()
    
    result = await orchestrator.route_request(
        request="Analyze financial health",
        preferred_agent="ai_cfo_agent"
    )
    
    assert result is not None
    await orchestrator.stop()
```

### Integration Testing

```python
@pytest.mark.asyncio
async def test_workflow_execution():
    """Test workflow execution."""
    orchestrator = get_orchestrator()
    
    # Register multiple agents
    orchestrator.register_agent(AICFOAgent(industry="healthcare"))
    orchestrator.register_agent(ForecastingAgent())
    orchestrator.register_agent(ReportingAgent())
    
    await orchestrator.start()
    
    result = await orchestrator.route_request(
        request="Execute advisory workflow",
        workflow_type="advisory"
    )
    
    assert result.get("success") is True
    assert result.get("workflow_type") == "advisory"
    assert len(result.get("completed_steps", [])) > 0
    
    await orchestrator.stop()
```

## 📊 Performance Monitoring

### Orchestrator Metrics

```python
from ai_financial.core.logging import get_logger

logger = get_logger(__name__)

# Monitor orchestrator performance
logger.info(
    "Orchestrator performance metrics",
    registered_agents=len(orchestrator.agents),
    active_workflows=len(orchestrator.active_workflows),
    active_agent_count=orchestrator._active_agent_count,
    max_concurrent_agents=orchestrator._max_concurrent_agents
)
```

### Workflow Metrics

```python
# Monitor workflow performance
logger.info(
    "Workflow performance metrics",
    workflow_id=workflow_state.workflow_id,
    workflow_type=workflow_state.workflow_type,
    completed_steps=len(workflow_state.steps_completed),
    execution_time=execution_time,
    success_rate=success_rate
)
```

## 🚀 Deployment

### Orchestrator Configuration

```python
# Configure orchestrator for different environments
if settings.environment == "production":
    # Production configuration
    orchestrator._max_concurrent_agents = 20
    orchestrator.workflow_timeout = 600  # 10 minutes
else:
    # Development configuration
    orchestrator._max_concurrent_agents = 5
    orchestrator.workflow_timeout = 120  # 2 minutes
```

### Scaling

```python
# Scale orchestrator horizontally
orchestrator = get_orchestrator()

# Register multiple agent instances
for i in range(3):
    agent = AICFOAgent(industry="healthcare")
    agent.agent_id = f"ai_cfo_agent_{i}"
    orchestrator.register_agent(agent)
```

## 📚 Additional Resources

- **Agent Models**: See `models/agent_models.py`
- **Workflow Engine**: See `workflow_engine.py`
- **Context Manager**: See `context_manager.py`
- **Agent Integration**: See `agents/` directory
- **Tool Integration**: See `mcp/` directory



