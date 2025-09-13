# Hiểu về Kiến trúc Code - AI Financial Multi-Agent System

## 📋 Tổng quan

Tài liệu này cung cấp cái nhìn chi tiết về kiến trúc code của AI Financial Multi-Agent System, bao gồm cấu trúc thư mục, các component chính, và cách chúng tương tác với nhau.

**Phiên bản hệ thống**: 0.1.0
**Ngày cập nhật**: 13/09/2025
**Môi trường**: Python 3.12, FastAPI, LangChain, LangGraph

---

## 🏗️ Cấu trúc Thư mục

```
src/ai_financial/
├── __init__.py                 # Package initialization
├── main.py                     # FastAPI application entry point
├── cli.py                      # Command-line interface
├── core/                       # Core infrastructure layer
│   ├── __init__.py
│   ├── base_agent.py          # Base class for all agents
│   ├── config.py              # Configuration management
│   ├── database.py            # Database connections
│   └── logging.py             # Logging and tracing setup
├── models/                     # Data models layer
│   ├── __init__.py
│   ├── agent_models.py        # Agent-related models
│   ├── financial_models.py    # Financial data models
│   ├── agent.py               # Agent base models
│   ├── financial.py           # Financial base models
│   ├── integration.py         # Integration models
│   └── enums.py               # Enumeration definitions
├── agents/                     # AI agents layer
│   ├── __init__.py
│   └── advisory/              # Advisory context agents
│       ├── __init__.py
│       └── ai_cfo_agent.py    # AI CFO Agent implementation
├── mcp/                       # MCP (Model Context Protocol) layer
│   ├── __init__.py
│   ├── server.py              # MCP server implementation
│   ├── hub.py                 # Tool hub management
│   └── tools/                 # MCP tools
│       ├── __init__.py
│       ├── base_tool.py       # Base tool class
│       └── financial_tools.py # Financial analysis tools
└── orchestrator/              # Orchestration layer
    ├── __init__.py
    ├── orchestrator.py        # Main orchestrator
    ├── workflow_engine.py     # Workflow management
    └── context_manager.py     # Context management
```

---

## 🧩 Kiến trúc Layered

### **Layer 1: Presentation Layer**

```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer                        │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │   FastAPI REST  │  │   CLI Interface │  │  WebSocket  │  │
│  │     (main.py)   │  │     (cli.py)    │  │ Streaming   │  │
│  └─────────────────┘  └─────────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### **Layer 2: Orchestration Layer**

```
┌─────────────────────────────────────────────────────────────┐
│                 Orchestration Layer                         │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │  Agent          │  │  Workflow       │  │  Context    │  │
│  │ Orchestrator    │  │  Engine         │  │ Manager     │  │
│  │ (orchestrator.py)│  │ (workflow_engine)│  │(context_mgr)│  │
│  └─────────────────┘  └─────────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### **Layer 3: Agent Layer**

```
┌─────────────────────────────────────────────────────────────┐
│                    Agent Layer                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │   Base Agent    │  │  AI CFO Agent   │  │  Future     │  │
│  │ (base_agent.py) │  │ (ai_cfo_agent)  │  │ Agents      │  │
│  └─────────────────┘  └─────────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### **Layer 4: MCP Tools Layer**

```
┌─────────────────────────────────────────────────────────────┐
│                    MCP Tools Layer                          │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │   MCP Server    │  │   Tool Hub      │  │ Financial   │  │
│  │  (server.py)    │  │   (hub.py)      │  │ Tools       │  │
│  └─────────────────┘  └─────────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### **Layer 5: Data Models Layer**

```
┌─────────────────────────────────────────────────────────────┐
│                   Data Models Layer                         │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │   Agent         │  │  Financial      │  │ Integration │  │
│  │   Models        │  │  Models         │  │ Models      │  │
│  │(agent_models.py)│  │(financial_models)│  │(integration)│  │
│  └─────────────────┘  └─────────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### **Layer 6: Core Infrastructure**

```
┌─────────────────────────────────────────────────────────────┐
│                Core Infrastructure                          │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │ Configuration   │  │    Database     │  │   Logging   │  │
│  │  (config.py)    │  │ (database.py)   │  │(logging.py) │  │
│  └─────────────────┘  └─────────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

---



## 🔧 Component Chi tiết

### **1. Core Infrastructure (`core/`)**

#### **`config.py` - Configuration Management**

```python
class DatabaseSettings(BaseSettings):
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "ai_financial"
    postgres_password: str = ""
    postgres_db: str = "ai_financial"
  
    @property
    def postgres_url(self) -> str:
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

class LLMSettings(BaseSettings):
    openai_api_key: str = ""
    openai_model: str = "gpt-4-turbo-preview"
    openai_temperature: float = 0.1
    openai_max_tokens: int = 4000
  
    @property
    def has_openai_key(self) -> bool:
        return bool(self.openai_api_key and self.openai_api_key.startswith("sk-"))
```

**Chức năng:**

- Quản lý tất cả configuration settings
- Environment variables handling
- Database connection strings
- LLM configuration
- Security settings

#### **`base_agent.py` - Base Agent Class**

```python
class BaseAgent(ABC):
    def __init__(self, agent_id: str, name: str, description: str):
        self.agent_id = agent_id
        self.name = name
        self.description = description
        self.llm = ChatOpenAI(...)  # LangChain integration
        self.graph = self._build_graph()  # LangGraph integration
        self.compiled_graph = self.graph.compile()
  
    @abstractmethod
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph state graph for this agent."""
        pass
  
    @abstractmethod
    async def _process_request(self, state: AgentState) -> AgentState:
        """Process a request in the agent's main logic."""
        pass
  
    async def invoke(self, request, context=None) -> Dict[str, Any]:
        """Invoke the agent with a request."""
        # Execute the graph
        result = await self.compiled_graph.ainvoke(initial_state)
        return self._format_response(result)
```

**Chức năng:**

- Base class cho tất cả AI agents
- LangChain/LangGraph integration
- Async request processing
- Error handling và logging
- State management

#### **`logging.py` - Logging và Tracing**

```python
def setup_logging() -> None:
    """Set up structured logging with OpenTelemetry integration."""
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.processors.JSONRenderer(),
        ],
        logger_factory=structlog.WriteLoggerFactory(sys.stdout),
    )

def setup_tracing() -> None:
    """Set up OpenTelemetry tracing."""
    resource = Resource.create({
        "service.name": settings.monitoring.otel_service_name,
        "service.version": "0.1.0",
        "deployment.environment": settings.environment,
    })
    tracer_provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(tracer_provider)
```

**Chức năng:**

- Structured logging với JSON format
- OpenTelemetry tracing
- Performance monitoring
- Error tracking

### **2. Data Models (`models/`)**

#### **`agent_models.py` - Agent Models**

```python
class AgentContext(BaseModel):
    agent_id: str
    session_id: str = Field(default_factory=lambda: str(uuid4()))
    user_id: str
    company_id: str
    permissions: List[str] = Field(default_factory=list)
    state: Dict[str, Any] = Field(default_factory=dict)
    trace_id: Optional[int] = None

class AgentState(BaseModel):
    messages: List[BaseMessage] = Field(default_factory=list)
    context: Optional[AgentContext] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    current_step: str = "start"
    completed_steps: List[str] = Field(default_factory=list)
    error: Optional[str] = None

class WorkflowState(BaseModel):
    workflow_id: str = Field(default_factory=lambda: str(uuid4()))
    workflow_type: str
    status: WorkflowStatus = WorkflowStatus.PENDING
    agents: List[str] = Field(default_factory=list)
    current_step: str = "start"
    results: Dict[str, Any] = Field(default_factory=dict)
```

#### **`financial_models.py` - Financial Models**

```python
class Transaction(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    amount: Decimal = Field(..., description="Transaction amount")
    currency: str = Field(default="USD", description="Currency code")
    type: TransactionType
    status: TransactionStatus = TransactionStatus.PENDING
    description: str
    category: str
    account_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Account(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    code: str
    type: AccountType
    balance: Decimal = Field(default=Decimal("0.00"))
    currency: str = Field(default="USD")
    company_id: str
    is_active: bool = True

class Invoice(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    invoice_number: str
    amount: Decimal
    currency: str = Field(default="USD")
    status: InvoiceStatus = InvoiceStatus.DRAFT
    due_date: datetime
    customer_id: str
    items: List[InvoiceItem] = Field(default_factory=list)
```

### **3. Agent Layer (`agents/`)**

#### **`advisory/ai_cfo_agent.py` - AI CFO Agent**

```python
class AICFOAgent(BaseAgent):
    def __init__(self, industry: str = "general"):
        super().__init__(
            agent_id="ai_cfo_agent",
            name="AI CFO",
            description=f"AI Chief Financial Officer specialized in {industry} industry"
        )
        self.industry = industry
        self.industry_metrics = self._load_industry_metrics()
        self.industry_benchmarks = self._load_industry_benchmarks()
  
    def _build_graph(self) -> StateGraph:
        graph = StateGraph(AgentState)
      
        # Add nodes
        graph.add_node("analyze_request", self._analyze_request)
        graph.add_node("gather_data", self._gather_financial_data)
        graph.add_node("perform_analysis", self._perform_financial_analysis)
        graph.add_node("generate_insights", self._generate_insights)
        graph.add_node("assess_risks", self._assess_risks)
        graph.add_node("provide_recommendations", self._provide_recommendations)
        graph.add_node("format_response", self._format_response)
      
        # Add edges
        graph.set_entry_point("analyze_request")
        graph.add_edge("analyze_request", "gather_data")
        graph.add_edge("gather_data", "perform_analysis")
        graph.add_edge("perform_analysis", "generate_insights")
        graph.add_edge("generate_insights", "assess_risks")
        graph.add_edge("assess_risks", "provide_recommendations")
        graph.add_edge("provide_recommendations", "format_response")
        graph.add_edge("format_response", END)
      
        return graph
  
    async def _analyze_request(self, state: AgentState) -> AgentState:
        """Analyze the incoming request to determine analysis type."""
        # LLM-based request classification
        # Store analysis plan in metadata
        pass
  
    async def _gather_financial_data(self, state: AgentState) -> AgentState:
        """Gather relevant financial data for analysis."""
        # Fetch from databases
        # Simulate financial data for demo
        pass
  
    async def _perform_financial_analysis(self, state: AgentState) -> AgentState:
        """Perform comprehensive financial analysis."""
        # Liquidity, profitability, efficiency, leverage analysis
        # Industry comparison
        pass
  
    async def _generate_insights(self, state: AgentState) -> AgentState:
        """Generate financial insights using LLM."""
        # LLM-based insight generation
        pass
  
    async def _assess_risks(self, state: AgentState) -> AgentState:
        """Assess financial risks and opportunities."""
        # Risk assessment across multiple categories
        pass
  
    async def _provide_recommendations(self, state: AgentState) -> AgentState:
        """Provide actionable financial recommendations."""
        # Strategic recommendations with timelines
        pass
  
    async def _format_response(self, state: AgentState) -> AgentState:
        """Format the final CFO response."""
        # Executive-level report formatting
        pass
```

**Workflow của AI CFO Agent:**

```
Request → Analyze → Gather Data → Analysis → Insights → Risk Assessment → Recommendations → Format Response
```

### **4. MCP Tools Layer (`mcp/`)**

#### **`server.py` - MCP Server Implementation**

```python
class MCPServer:
    def __init__(self, server_id: str = "default"):
        self.server_id = server_id
        self.tools: Dict[str, BaseTool] = {}
        self.tool_hub = get_tool_hub()
  
    async def handle_request(self, request: MCPRequest) -> MCPResponse:
        if request.method == "tools/list":
            tools = [def_.model_dump() for def_ in self.get_tool_definitions()]
            return MCPResponse(id=request.id, result={"tools": tools})
      
        elif request.method == "tools/call":
            tool_name = request.params.get("name")
            parameters = request.params.get("arguments", {})
            result = await self.execute_tool(tool_name, parameters)
            return MCPResponse(id=request.id, result=result.model_dump())
      
        elif request.method == "tools/get":
            definition = self.get_tool_definition(tool_name)
            return MCPResponse(id=request.id, result=definition.model_dump())
  
    async def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> ToolResult:
        tool = self.tools.get(tool_name)
        if not tool:
            return ToolResult(success=False, error=f"Tool {tool_name} not found")
      
        return await tool.execute(parameters)
```

#### **`tools/financial_tools.py` - Financial Analysis Tools**

```python
class FinancialRatioTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="financial_ratio_calculator",
            description="Calculate various financial ratios",
            category="financial_analysis",
            version="1.0.0"
        )
  
    async def execute(self, parameters: Dict[str, Any], context=None) -> ToolResult:
        ratio_type = parameters.get("ratio_type")
        financial_data = parameters.get("financial_data", {})
      
        if ratio_type == "current_ratio":
            result = self._calculate_current_ratio(financial_data)
        elif ratio_type == "quick_ratio":
            result = self._calculate_quick_ratio(financial_data)
        elif ratio_type == "debt_to_equity":
            result = self._calculate_debt_to_equity(financial_data)
        elif ratio_type == "return_on_equity":
            result = self._calculate_roe(financial_data)
        else:
            return ToolResult(success=False, error=f"Unknown ratio type: {ratio_type}")
      
        return ToolResult(success=True, data=result)
  
    def _calculate_current_ratio(self, data: Dict[str, Any]) -> Dict[str, Any]:
        current_assets = data.get("current_assets", 0)
        current_liabilities = data.get("current_liabilities", 0)
      
        if current_liabilities == 0:
            return {"error": "Cannot calculate current ratio: current liabilities is zero"}
      
        ratio = current_assets / current_liabilities
      
        return {
            "ratio_type": "current_ratio",
            "value": float(ratio),
            "interpretation": self._interpret_current_ratio(ratio),
            "calculation": f"{current_assets} / {current_liabilities} = {ratio:.2f}"
        }
```

### **5. Orchestration Layer (`orchestrator/`)**

#### **`orchestrator.py` - Main Orchestrator**

```python
class AgentOrchestrator:
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.active_workflows: Dict[str, WorkflowState] = {}
        self.workflow_engine = WorkflowEngine()
        self.context_manager = ContextManager()
        self.tool_hub = get_tool_hub()
        self._running = False
        self._max_concurrent_agents = settings.workflow.max_concurrent_agents
  
    def register_agent(self, agent: BaseAgent) -> None:
        """Register an agent with the orchestrator."""
        self.agents[agent.agent_id] = agent
        logger.info(f"Agent {agent.agent_id} registered")
  
    async def route_request(self, request: str, workflow_type: str) -> Dict[str, Any]:
        """Route a request to the appropriate workflow."""
        workflow_id = str(uuid4())
        workflow_state = WorkflowState(
            workflow_id=workflow_id,
            workflow_type=workflow_type,
            status=WorkflowStatus.PROCESSING
        )
      
        self.active_workflows[workflow_id] = workflow_state
      
        try:
            if workflow_type == "advisory":
                result = await self._execute_advisory_workflow(request, workflow_state)
            elif workflow_type == "transactional":
                result = await self._execute_transactional_workflow(request, workflow_state)
            else:
                raise ValueError(f"Unknown workflow type: {workflow_type}")
          
            workflow_state.status = WorkflowStatus.COMPLETED
            workflow_state.results = result
          
            return result
          
        except Exception as e:
            workflow_state.status = WorkflowStatus.ERROR
            workflow_state.error = str(e)
            logger.error(f"Workflow {workflow_id} failed: {e}")
            raise
  
    async def _execute_advisory_workflow(self, request: str, workflow_state: WorkflowState) -> Dict[str, Any]:
        """Execute advisory workflow using AI CFO agent."""
        ai_cfo = self.agents.get("ai_cfo_agent")
        if not ai_cfo:
            raise ValueError("AI CFO agent not available")
      
        context = AgentContext(
            agent_id="ai_cfo_agent",
            user_id="system",
            company_id="default"
        )
      
        result = await ai_cfo.invoke(request, context)
        return result
```

### **6. Presentation Layer**

#### **`main.py` - FastAPI Application**

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    logger.info("Starting AI Financial Multi-Agent System")
  
    # Initialize components
    orchestrator = get_orchestrator()
    tool_hub = get_tool_hub()
  
    # Register agents
    try:
        ai_cfo = AICFOAgent(industry="general")
        orchestrator.register_agent(ai_cfo)
    except Exception as e:
        logger.warning(f"Failed to register AI CFO agent: {e}")
  
    # Register tools
    financial_ratio_tool = FinancialRatioTool()
    cash_flow_tool = CashFlowAnalysisTool()
    profitability_tool = ProfitabilityAnalysisTool()
  
    tool_hub.register_tool(financial_ratio_tool)
    tool_hub.register_tool(cash_flow_tool)
    tool_hub.register_tool(profitability_tool)
  
    # Start MCP server
    mcp_server = MCPServer()
    await mcp_server.start()
  
    yield
  
    # Cleanup
    await orchestrator.stop()
    await mcp_server.stop()

app = FastAPI(
    title="AI Financial Multi-Agent System",
    description="Financial automation platform for SMBs",
    version="0.1.0",
    lifespan=lifespan
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "0.1.0"}

@app.post("/api/v1/agents/{agent_id}/invoke")
async def invoke_agent(agent_id: str, request: Dict[str, Any]):
    orchestrator = get_orchestrator()
    result = await orchestrator.route_request(
        request=request["message"],
        workflow_type="advisory"
    )
    return result

@app.get("/api/v1/tools")
async def list_tools():
    tool_hub = get_tool_hub()
    tools = tool_hub.get_available_tools()
    return {
        "tools": [tool.model_dump() for tool in tools],
        "count": len(tools),
    }

@app.post("/api/v1/tools/{tool_name}/execute")
async def execute_tool(tool_name: str, request: Dict[str, Any]):
    tool_hub = get_tool_hub()
    result = await tool_hub.execute_tool(
        tool_name=tool_name,
        parameters=request.get("parameters", {}),
        context=request.get("context")
    )
    return result.model_dump()
```

---

## 🔄 Data Flow

### **1. Request Flow**

```
Client Request → FastAPI → Orchestrator → Agent → Tools → Response
```

### **2. Agent Workflow**

```
User Input → Request Analysis → Data Gathering → Analysis → Insights → Risk Assessment → Recommendations → Response Formatting
```

### **3. Tool Execution Flow**

```
Agent Request → Tool Hub → Tool Selection → Parameter Validation → Tool Execution → Result Processing → Agent Response
```

---

## 🎯 Design Patterns

### **1. Factory Pattern**

- `get_orchestrator()` - Singleton orchestrator
- `get_tool_hub()` - Singleton tool hub
- Agent creation with industry specialization

### **2. Strategy Pattern**

- Different analysis strategies for different industries
- Multiple tool implementations for different calculations
- Various workflow types (advisory, transactional)

### **3. Observer Pattern**

- Workflow state changes
- Agent status updates
- Tool execution monitoring

### **4. Template Method Pattern**

- `BaseAgent._process_request()` - Template for agent processing
- `BaseTool.execute()` - Template for tool execution
- Workflow execution templates

### **5. Dependency Injection**

- Configuration injection through settings
- Tool injection into agents
- Context injection into workflows

---

## 🔒 Security Architecture

### **1. Authentication & Authorization**

```python
class AgentContext(BaseModel):
    user_id: str
    company_id: str
    permissions: List[str]
    # JWT token validation
    # Role-based access control
```

### **2. Data Validation**

- Pydantic models for all data structures
- Input validation at API boundaries
- Parameter validation in tools

### **3. Audit Logging**

```python
# Structured logging with correlation IDs
logger.info(
    "Agent request processed",
    agent_id=self.agent_id,
    session_id=context.session_id,
    trace_id=context.trace_id,
    user_id=context.user_id
)
```

---

## 📊 Monitoring & Observability

### **1. OpenTelemetry Integration**

```python
with tracer.start_as_current_span(f"{self.agent_id}.invoke") as span:
    span.set_attribute("agent_id", self.agent_id)
    span.set_attribute("request_type", "financial_analysis")
    # Distributed tracing across all components
```

### **2. Structured Logging**

```python
logger.info(
    "Financial analysis completed",
    agent_id=self.agent_id,
    analysis_types=list(analysis_results.keys()),
    execution_time=execution_time
)
```

### **3. Health Monitoring**

```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "0.1.0",
        "agents_count": len(orchestrator.agents),
        "tools_count": len(tool_hub.tools),
        "demo_mode": not settings.llm.has_openai_key
    }
```

---

## 🚀 Extension Points

### **1. Adding New Agents**

```python
class MyCustomAgent(BaseAgent):
    def _build_graph(self) -> StateGraph:
        # Define agent workflow
        pass
  
    async def _process_request(self, state: AgentState) -> AgentState:
        # Implement agent logic
        pass
```

### **2. Adding New Tools**

```python
class MyCustomTool(BaseTool):
    async def execute(self, parameters, context=None) -> ToolResult:
        # Implement tool logic
        return ToolResult(success=True, data=result)
```

### **3. Adding New Workflows**

```python
async def _execute_custom_workflow(self, request: str, workflow_state: WorkflowState):
    # Implement custom workflow logic
    pass
```

---

## 📈 Performance Considerations

### **1. Async/Await Pattern**

- All I/O operations are async
- Non-blocking database operations
- Concurrent agent execution

### **2. Caching Strategy**

- Redis for session caching
- In-memory caching for frequently accessed data
- Tool result caching

### **3. Resource Management**

- Connection pooling for databases
- Rate limiting for API calls
- Memory management for large datasets

---

## 🧪 Testing Architecture

### **1. Unit Testing**

- Individual component testing
- Mock dependencies
- Isolated agent testing

### **2. Integration Testing**

- End-to-end workflow testing
- API integration testing
- Database integration testing

### **3. Load Testing**

- Concurrent user simulation
- Performance benchmarking
- Stress testing

---

## 📝 Kết luận

Kiến trúc AI Financial Multi-Agent System được thiết kế theo nguyên tắc:

1. **Modularity**: Tách biệt rõ ràng các layer và component
2. **Scalability**: Dễ dàng thêm agents và tools mới
3. **Maintainability**: Code structure rõ ràng, dễ hiểu và maintain
4. **Extensibility**: Nhiều extension points cho customization
5. **Observability**: Comprehensive monitoring và logging
6. **Security**: Built-in security mechanisms
7. **Performance**: Async/await pattern và caching strategies

Hệ thống sử dụng các công nghệ hiện đại như FastAPI, LangChain, LangGraph, và OpenTelemetry để tạo ra một platform mạnh mẽ và linh hoạt cho financial automation.

---

*Tài liệu được tạo tự động bởi Doan Ngoc Cuong - AI Assistant*
*Cập nhật lần cuối: 13/09/2025*
