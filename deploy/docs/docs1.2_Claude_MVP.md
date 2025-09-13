
Tôi sẽ thiết kế khung xương cấu trúc code cho luồng **Advisory cho CEO** dựa trên Agentic Design Patterns và stack công nghệ đã đề xuất.## Tóm tắt kiến trúc Advisory đã thiết kế:

### **1. Multi-Agent Architecture với LangGraph**

* **Orchestrator** điều phối workflow qua state machine
* **7 Specialized Agents** : Router, Supervisor, Data Collector, Analyzer, Forecaster, Alert Manager, Advisor, Explainer
* Mỗi agent có vai trò riêng, kế thừa từ BaseAgent với telemetry và error handling

### **2. Core Patterns từ sách Agentic Design Patterns**

* **Routing** : Định tuyến request theo loại (full_analysis, quick_check, forecast, what_if)
* **Parallelization** : Thu thập data từ nhiều nguồn đồng thời
* **Planning** : Workflow orchestration với LangGraph
* **Reflection** : Validate và refine kết quả phân tích
* **Memory Management** : RAG với vector store cho historical context
* **Tool Use** : MCP integration cho tools nội bộ và industry-specific
* **Guardrails** : Validation ở input/output của mỗi agent
* **Monitoring** : OpenTelemetry tracing + Langfuse

### **3. Key Features đã design**

* **Streaming events** qua FastAPI SSE
* **Industry-specific analysis** thông qua MCP tools
* **13-week cash flow + 12-month P&L forecasting**
* **What-if scenarios** với Monte Carlo simulation
* **Explainability** với citations và confidence scores
* **Supervisor pattern** cho quality control

### **4. Gợi ý implement MVP - Phase 1 (2 tuần)**

**Tuần 1: Core Foundation**

```python
# 1. Setup base infrastructure
- FastAPI app với basic endpoints
- PostgreSQL + Redis setup
- OpenTelemetry basic config
- Docker compose environment

# 2. Implement BaseAgent và State management
- AdvisoryState TypedDict
- BaseAgent với error handling
- Simple memory với Redis

# 3. Data Collector Agent (simplified)
- Mock connectors cho ERP/accounting
- Basic data normalization
- Store raw_data trong state
```

**Tuần 2: Analysis & Forecasting**

```python
# 4. Financial Analyzer Agent
- Basic metrics calculation (cash flow, P&L)
- Simple health scoring (0-100)
- Industry templates (hardcode cho 2-3 ngành)

# 5. Forecaster Agent (basic)
- Linear projection cho cash flow 13 tuần
- Simple trend analysis
- 1-2 what-if scenarios cứng

# 6. Basic Orchestrator
- Sequential flow: collect → analyze → forecast
- Simple routing logic
- Basic streaming response
```

### **5. MVP Demo Flow**

```python
# Request
POST /api/v1/advisory/analyze
{
  "company_id": "demo_company",
  "request_type": "quick_check",
  "industry": "retail"
}

# Response (streaming)
data: {"phase": "data_collection", "progress": 20}
data: {"phase": "analysis", "progress": 50, "health_score": 72}
data: {"phase": "forecasting", "progress": 80}
data: {"phase": "complete", "results": {...}}
```

### **6. Tech Stack cho MVP**

```
- Python 3.11+ 
- LangChain 0.1.x + LangGraph
- FastAPI + Uvicorn
- PostgreSQL + SQLAlchemy
- Redis cho caching
- OpenAI GPT-4 (hoặc local LLM)
- Docker + Docker Compose
```

### **7. Folder structure cho quick start**

```bash
# Tạo project structure
mkdir ai-cfo-advisory && cd ai-cfo-advisory

# Core directories
mkdir -p src/{core,agents,tools,api}
mkdir -p config tests docs

# Create initial files
touch src/core/{__init__.py,state.py,base_agent.py}
touch src/agents/{__init__.py,data_collector.py,analyzer.py}
touch src/api/{__init__.py,main.py,models.py}
touch config/agents.yaml
touch docker-compose.yml
touch requirements.txt
```

**Bạn muốn tôi deep dive vào phần nào trước?**

1. Code chi tiết cho một agent cụ thể (VD: Analyzer)
2. MCP tool integration
3. Streaming implementation với LangGraph
4. Industry-specific templates


---



# AI CFO Advisory System - Kiến trúc Multi-Agent

## 1. Tổng quan kiến trúc

```
┌─────────────────────────────────────────────────────────────┐
│                     Advisory Orchestrator                     │
│                    (LangGraph StateMachine)                  │
└──────────┬──────────────────────────────────┬───────────────┘
           │                                  │
     ┌─────▼──────┐                    ┌─────▼──────┐
     │   Router   │                    │ Supervisor │
     │   Agent    │                    │   Agent    │
     └─────┬──────┘                    └─────┬──────┘
           │                                  │
┌──────────┼──────────────────────────────────┼──────────────┐
│          │         Specialized Agents       │              │
│  ┌───────▼────────┐  ┌──────────┐  ┌──────▼──────┐       │
│  │ Data Collector │  │ Analyzer │  │  Forecaster │       │
│  └────────────────┘  └──────────┘  └─────────────┘       │
│  ┌────────────────┐  ┌──────────┐  ┌─────────────┐       │
│  │ Alert Manager  │  │ Advisor  │  │ Explainer   │       │
│  └────────────────┘  └──────────┘  └─────────────┘       │
└────────────────────────────────────────────────────────────┘
           │                                  │
     ┌─────▼──────┐                    ┌─────▼──────┐
     │  Tool Hub  │                    │   Memory    │
     │(MCP Server)│                    │   Manager   │
     └────────────┘                    └─────────────┘
```

## 2. Cấu trúc thư mục dự án

```
ai-cfo-advisory/
├── src/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── state.py              # Shared state definitions
│   │   ├── base_agent.py         # Base agent class
│   │   └── orchestrator.py       # Main LangGraph orchestrator
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── router.py             # Routing agent (Pattern: Routing)
│   │   ├── supervisor.py         # Supervisor agent (Pattern: Multi-Agent)
│   │   ├── data_collector.py     # Data sync & collection
│   │   ├── analyzer.py           # Financial analysis (Pattern: Reasoning)
│   │   ├── forecaster.py         # Forecasting & scenarios (Pattern: Planning)
│   │   ├── alert_manager.py      # Alert generation (Pattern: Monitoring)
│   │   ├── advisor.py            # Advisory & recommendations
│   │   └── explainer.py          # Explanation generation (Pattern: Reflection)
│   │
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── mcp_client.py         # MCP client implementation
│   │   ├── data_connectors/      # ERP, accounting software connectors
│   │   │   ├── erp_connector.py
│   │   │   ├── accounting_connector.py
│   │   │   └── bank_connector.py
│   │   ├── financial_tools.py    # Financial calculation tools
│   │   └── industry_tools.py     # Industry-specific tools
│   │
│   ├── memory/
│   │   ├── __init__.py
│   │   ├── memory_manager.py     # Pattern: Memory Management
│   │   ├── vector_store.py       # RAG implementation
│   │   └── cache.py              # Caching layer
│   │
│   ├── patterns/
│   │   ├── __init__.py
│   │   ├── chain.py              # Pattern: Prompt Chaining
│   │   ├── parallel.py           # Pattern: Parallelization
│   │   ├── reflection.py         # Pattern: Reflection
│   │   └── guardrails.py         # Pattern: Guardrails/Safety
│   │
│   ├── monitoring/
│   │   ├── __init__.py
│   │   ├── telemetry.py          # OpenTelemetry integration
│   │   ├── langfuse_client.py    # Langfuse monitoring
│   │   └── metrics.py            # Metrics collection
│   │
│   └── utils/
│       ├── __init__.py
│       ├── config.py             # Configuration management
│       └── exceptions.py         # Exception handling
│
├── config/
│   ├── agents.yaml               # Agent configurations
│   ├── tools.yaml                # Tool configurations
│   └── policies.yaml             # Business policies & rules
│
├── tests/
│   └── ...
│
└── requirements.txt
```

## 3. Core Components

### 3.1 State Management (state.py)

```python
from typing import TypedDict, List, Dict, Any, Optional
from enum import Enum
from pydantic import BaseModel
from datetime import datetime

class AnalysisPhase(Enum):
    DATA_COLLECTION = "data_collection"
    ANALYSIS = "analysis"
    FORECASTING = "forecasting"
    ALERT_GENERATION = "alert_generation"
    ADVISORY = "advisory"
    EXPLANATION = "explanation"
    COMPLETE = "complete"

class FinancialHealth(BaseModel):
    cash_flow_health: float  # 0-100
    profitability_health: float
    liquidity_health: float
    debt_health: float
    overall_score: float
    timestamp: datetime

class AdvisoryState(TypedDict):
    # Request info
    request_id: str
    user_id: str
    company_id: str
    industry: str
    request_type: str  # "full_analysis", "quick_check", "forecast", "what_if"
  
    # Processing state
    current_phase: AnalysisPhase
    messages: List[Dict[str, Any]]
  
    # Data collection
    raw_data: Dict[str, Any]
    data_sources: List[str]
    last_sync_timestamp: Optional[datetime]
  
    # Analysis results
    financial_health: Optional[FinancialHealth]
    key_metrics: Dict[str, Any]
    trends: Dict[str, Any]
  
    # Forecasts
    cash_flow_forecast: Optional[Dict[str, Any]]  # 13 weeks
    pnl_forecast: Optional[Dict[str, Any]]  # 12 months
    scenarios: List[Dict[str, Any]]  # what-if scenarios
  
    # Alerts & recommendations
    alerts: List[Dict[str, Any]]
    recommendations: List[Dict[str, Any]]
    action_items: List[Dict[str, Any]]
  
    # Explanations
    explanations: Dict[str, str]
    citations: List[Dict[str, str]]
    confidence_scores: Dict[str, float]
  
    # Metadata
    processing_time: float
    token_usage: Dict[str, int]
    errors: List[str]
```

### 3.2 Base Agent (base_agent.py)

```python
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from opentelemetry import trace
from langchain.agents import AgentExecutor
from langchain.memory import ConversationBufferMemory
import structlog

tracer = trace.get_tracer(__name__)
logger = structlog.get_logger()

class BaseAgent(ABC):
    """Base class implementing common patterns for all agents"""
  
    def __init__(self, 
                 name: str,
                 llm: Any,
                 tools: List[Any] = None,
                 memory_manager: Optional[Any] = None):
        self.name = name
        self.llm = llm
        self.tools = tools or []
        self.memory_manager = memory_manager
        self.memory = ConversationBufferMemory()
      
    @abstractmethod
    async def process(self, state: AdvisoryState) -> AdvisoryState:
        """Main processing logic - must be implemented by each agent"""
        pass
  
    @tracer.start_as_current_span("agent_execution")
    async def execute(self, state: AdvisoryState) -> AdvisoryState:
        """Execute with monitoring and error handling (Pattern: Exception Handling)"""
        span = trace.get_current_span()
        span.set_attribute("agent.name", self.name)
        span.set_attribute("request.id", state["request_id"])
      
        try:
            logger.info(f"Agent {self.name} starting", 
                       request_id=state["request_id"])
          
            # Pattern: Reflection - validate input
            state = await self._validate_input(state)
          
            # Main processing
            state = await self.process(state)
          
            # Pattern: Reflection - validate output
            state = await self._validate_output(state)
          
            logger.info(f"Agent {self.name} completed",
                       request_id=state["request_id"])
            return state
          
        except Exception as e:
            logger.error(f"Agent {self.name} error", 
                        error=str(e),
                        request_id=state["request_id"])
            state["errors"].append(f"{self.name}: {str(e)}")
            span.record_exception(e)
            raise
  
    async def _validate_input(self, state: AdvisoryState) -> AdvisoryState:
        """Pattern: Guardrails - validate input state"""
        # Implementation specific to each agent
        return state
  
    async def _validate_output(self, state: AdvisoryState) -> AdvisoryState:
        """Pattern: Guardrails - validate output state"""
        # Implementation specific to each agent
        return state
```

### 3.3 Orchestrator (orchestrator.py)

```python
from langgraph.graph import StateGraph, END
from langgraph.checkpoint import MemorySaver
from typing import Literal

class AdvisoryOrchestrator:
    """Main orchestrator using LangGraph (Pattern: Planning + Multi-Agent)"""
  
    def __init__(self, agents: Dict[str, BaseAgent], config: Dict):
        self.agents = agents
        self.config = config
        self.workflow = self._build_workflow()
      
    def _build_workflow(self) -> StateGraph:
        """Build the advisory workflow graph"""
        workflow = StateGraph(AdvisoryState)
      
        # Add nodes for each agent
        workflow.add_node("router", self.route_request)
        workflow.add_node("data_collector", self.collect_data)
        workflow.add_node("analyzer", self.analyze_financials)
        workflow.add_node("forecaster", self.generate_forecasts)
        workflow.add_node("alert_manager", self.generate_alerts)
        workflow.add_node("advisor", self.generate_advice)
        workflow.add_node("explainer", self.generate_explanations)
        workflow.add_node("supervisor", self.supervise)
      
        # Define edges (Pattern: Routing)
        workflow.set_entry_point("router")
      
        workflow.add_conditional_edges(
            "router",
            self.determine_flow,
            {
                "full_analysis": "data_collector",
                "quick_check": "analyzer",
                "forecast": "forecaster",
                "what_if": "forecaster"
            }
        )
      
        # Standard flow
        workflow.add_edge("data_collector", "analyzer")
        workflow.add_edge("analyzer", "forecaster")
        workflow.add_edge("forecaster", "alert_manager")
        workflow.add_edge("alert_manager", "advisor")
        workflow.add_edge("advisor", "explainer")
        workflow.add_edge("explainer", "supervisor")
      
        # Supervisor can loop back or end
        workflow.add_conditional_edges(
            "supervisor",
            self.supervisor_decision,
            {
                "approve": END,
                "revise": "analyzer",
                "need_more_data": "data_collector"
            }
        )
      
        # Compile with memory
        memory = MemorySaver()
        app = workflow.compile(checkpointer=memory)
        return app
  
    async def route_request(self, state: AdvisoryState) -> AdvisoryState:
        """Pattern: Routing - determine processing path"""
        return await self.agents["router"].execute(state)
  
    async def collect_data(self, state: AdvisoryState) -> AdvisoryState:
        """Pattern: Parallelization - collect from multiple sources"""
        return await self.agents["data_collector"].execute(state)
  
    async def analyze_financials(self, state: AdvisoryState) -> AdvisoryState:
        """Pattern: Reasoning - deep financial analysis"""
        return await self.agents["analyzer"].execute(state)
  
    # ... other agent methods ...
  
    def determine_flow(self, state: AdvisoryState) -> Literal["full_analysis", "quick_check", "forecast", "what_if"]:
        """Determine which flow to execute based on request type"""
        return state["request_type"]
  
    def supervisor_decision(self, state: AdvisoryState) -> Literal["approve", "revise", "need_more_data"]:
        """Pattern: Human-in-the-Loop readiness check"""
        confidence = state["confidence_scores"].get("overall", 0)
      
        if confidence > 0.85:
            return "approve"
        elif confidence > 0.6:
            return "revise"
        else:
            return "need_more_data"
  
    async def run(self, request: Dict) -> Dict:
        """Main entry point for running advisory analysis"""
        initial_state = self._prepare_initial_state(request)
      
        # Stream events for real-time updates
        async for event in self.workflow.astream_events(
            initial_state,
            version="v1"
        ):
            # Handle streaming events
            await self._handle_stream_event(event)
      
        # Get final result
        final_state = await self.workflow.ainvoke(initial_state)
        return self._format_response(final_state)
```

### 3.4 Sample Agent Implementation (analyzer.py)

```python
from typing import Dict, List
import asyncio
from src.core.base_agent import BaseAgent
from src.patterns.parallel import ParallelProcessor
from src.patterns.reflection import ReflectionValidator

class FinancialAnalyzer(BaseAgent):
    """Financial Analysis Agent (Pattern: Reasoning + Reflection)"""
  
    async def process(self, state: AdvisoryState) -> AdvisoryState:
        """Analyze financial data with industry-specific insights"""
      
        # Pattern: Parallelization - analyze multiple aspects concurrently
        parallel_tasks = [
            self._analyze_cash_flow(state),
            self._analyze_profitability(state),
            self._analyze_liquidity(state),
            self._analyze_debt(state),
            self._analyze_industry_benchmarks(state)
        ]
      
        results = await asyncio.gather(*parallel_tasks)
      
        # Merge results
        state["key_metrics"] = self._merge_metrics(results)
      
        # Pattern: Reasoning - deep analysis with chain of thought
        analysis_prompt = self._build_analysis_prompt(state)
        analysis_result = await self.llm.ainvoke(analysis_prompt)
      
        # Pattern: Reflection - validate and refine analysis
        validator = ReflectionValidator(self.llm)
        refined_analysis = await validator.validate_and_refine(
            analysis_result,
            context=state["raw_data"],
            criteria=self._get_validation_criteria(state["industry"])
        )
      
        # Calculate financial health scores
        state["financial_health"] = self._calculate_health_scores(
            state["key_metrics"],
            refined_analysis
        )
      
        # Identify trends
        state["trends"] = self._identify_trends(state["raw_data"])
      
        # Update confidence
        state["confidence_scores"]["analysis"] = self._calculate_confidence(
            data_completeness=self._assess_data_completeness(state),
            industry_match=self._assess_industry_expertise(state["industry"])
        )
      
        state["current_phase"] = AnalysisPhase.FORECASTING
        return state
  
    async def _analyze_cash_flow(self, state: AdvisoryState) -> Dict:
        """Analyze cash flow patterns"""
        # Implementation
        pass
  
    async def _analyze_industry_benchmarks(self, state: AdvisoryState) -> Dict:
        """Compare against industry benchmarks using MCP tools"""
        # Use industry-specific tools via MCP
        industry_tool = await self._get_industry_tool(state["industry"])
        benchmarks = await industry_tool.get_benchmarks(
            metrics=state["key_metrics"],
            company_size=state["company_size"]
        )
        return benchmarks
  
    def _build_analysis_prompt(self, state: AdvisoryState) -> str:
        """Build analysis prompt with industry context"""
        return f"""
        Analyze the financial data for a {state['industry']} company.
      
        Key Metrics:
        {state['key_metrics']}
      
        Industry Context:
        - Typical cash cycles in {state['industry']}
        - Regulatory requirements
        - Seasonal patterns
      
        Provide:
        1. Health assessment (0-100 scores)
        2. Key strengths and weaknesses
        3. Critical risk factors
        4. Comparison to industry standards
      
        Use chain of thought reasoning and show your work.
        """
```

## 4. Tool Integration (MCP)

### 4.1 MCP Client (mcp_client.py)

```python
from typing import Dict, Any, List
import asyncio
from mcp import Client, Tool

class MCPToolHub:
    """MCP Client for tool integration (Pattern: Tool Use)"""
  
    def __init__(self, config: Dict):
        self.config = config
        self.clients = {}
        self.tools = {}
      
    async def initialize(self):
        """Initialize MCP connections to tool servers"""
        for server_config in self.config["mcp_servers"]:
            client = await self._connect_to_server(server_config)
            self.clients[server_config["name"]] = client
          
            # Discover available tools
            tools = await client.list_tools()
            for tool in tools:
                self.tools[tool.name] = tool
  
    async def _connect_to_server(self, config: Dict) -> Client:
        """Connect to an MCP server"""
        client = Client()
        await client.connect(
            host=config["host"],
            port=config["port"],
            auth=config.get("auth")
        )
        return client
  
    async def call_tool(self, tool_name: str, params: Dict) -> Any:
        """Call a tool through MCP"""
        if tool_name not in self.tools:
            raise ValueError(f"Tool {tool_name} not found")
      
        tool = self.tools[tool_name]
        result = await tool.call(params)
        return result
  
    def get_tools_for_industry(self, industry: str) -> List[Tool]:
        """Get industry-specific tools"""
        return [
            tool for tool in self.tools.values()
            if industry.lower() in tool.metadata.get("industries", [])
        ]
```

## 5. Memory Management

### 5.1 Memory Manager (memory_manager.py)

```python
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import asyncio
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

class AdvisoryMemoryManager:
    """Memory management with RAG (Pattern: Memory Management + RAG)"""
  
    def __init__(self, config: Dict):
        self.config = config
        self.embeddings = OpenAIEmbeddings()
        self.vector_store = Chroma(
            collection_name="advisory_memory",
            embedding_function=self.embeddings
        )
        self.short_term_memory = {}  # Request-specific memory
        self.long_term_memory = {}   # Company-specific insights
      
    async def store_analysis(self, 
                            company_id: str,
                            analysis: Dict,
                            metadata: Dict):
        """Store analysis results for future reference"""
        # Store in vector DB for RAG
        documents = self._prepare_documents(analysis, metadata)
        await self.vector_store.aadd_documents(documents)
      
        # Update long-term memory
        if company_id not in self.long_term_memory:
            self.long_term_memory[company_id] = {
                "analyses": [],
                "patterns": {},
                "key_events": []
            }
      
        self.long_term_memory[company_id]["analyses"].append({
            "timestamp": datetime.now(),
            "analysis": analysis,
            "metadata": metadata
        })
      
        # Identify and store patterns
        patterns = await self._identify_patterns(company_id)
        self.long_term_memory[company_id]["patterns"].update(patterns)
  
    async def retrieve_context(self, 
                              company_id: str,
                              query: str,
                              k: int = 5) -> List[Dict]:
        """Retrieve relevant historical context"""
        # RAG retrieval
        relevant_docs = await self.vector_store.asimilarity_search(
            query,
            k=k,
            filter={"company_id": company_id}
        )
      
        # Combine with recent analyses
        recent_analyses = self._get_recent_analyses(company_id, days=30)
      
        return {
            "historical_context": relevant_docs,
            "recent_analyses": recent_analyses,
            "identified_patterns": self.long_term_memory.get(company_id, {}).get("patterns", {})
        }
  
    async def _identify_patterns(self, company_id: str) -> Dict:
        """Identify patterns in historical data"""
        analyses = self.long_term_memory[company_id]["analyses"]
      
        if len(analyses) < 3:
            return {}
      
        # Analyze patterns using LLM
        pattern_prompt = f"""
        Analyze the following historical financial analyses and identify patterns:
      
        {analyses[-10:]}  # Last 10 analyses
      
        Identify:
        1. Recurring issues or strengths
        2. Seasonal patterns
        3. Growth/decline trends
        4. Risk patterns
        """
      
        # Call LLM to identify patterns
        patterns = await self.llm.ainvoke(pattern_prompt)
        return patterns
```

## 6. Monitoring & Observability

### 6.1 Telemetry (telemetry.py)

```python
from opentelemetry import trace, metrics
from opentelemetry.exporter.otlp.proto.grpc import (
    trace_exporter,
    metrics_exporter
)
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.instrumentation.langchain import LangchainInstrumentor
import structlog

class TelemetryManager:
    """OpenTelemetry integration for distributed tracing"""
  
    def __init__(self, config: Dict):
        self.config = config
        self._setup_tracing()
        self._setup_metrics()
        self._setup_logging()
      
    def _setup_tracing(self):
        """Setup distributed tracing"""
        tracer_provider = TracerProvider()
      
        # OTLP exporter
        otlp_exporter = trace_exporter.OTLPSpanExporter(
            endpoint=self.config["otlp_endpoint"],
            insecure=True
        )
      
        tracer_provider.add_span_processor(
            BatchSpanProcessor(otlp_exporter)
        )
      
        trace.set_tracer_provider(tracer_provider)
      
        # Instrument Langchain
        LangchainInstrumentor().instrument()
  
    def _setup_metrics(self):
        """Setup metrics collection"""
        meter_provider = MeterProvider()
      
        metrics_exporter = metrics_exporter.OTLPMetricExporter(
            endpoint=self.config["otlp_endpoint"],
            insecure=True
        )
      
        meter_provider.add_metric_reader(
            PeriodicExportingMetricReader(metrics_exporter)
        )
      
        metrics.set_meter_provider(meter_provider)
      
        # Create meters
        self.meter = metrics.get_meter(__name__)
      
        # Define metrics
        self.request_counter = self.meter.create_counter(
            "advisory_requests_total",
            description="Total number of advisory requests"
        )
      
        self.processing_time = self.meter.create_histogram(
            "advisory_processing_time_seconds",
            description="Time taken to process advisory requests"
        )
      
        self.token_usage = self.meter.create_counter(
            "llm_token_usage_total",
            description="Total LLM token usage"
        )
  
    def _setup_logging(self):
        """Setup structured logging"""
        structlog.configure(
            processors=[
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeDecoder(),
                structlog.processors.JSONRenderer()
            ],
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )
```

## 7. API Layer

### 7.1 FastAPI Application (main.py)

```python
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Dict, Optional
import asyncio
import json

app = FastAPI(title="AI CFO Advisory API")

# Initialize components
orchestrator = None
telemetry = None

@app.on_event("startup")
async def startup_event():
    """Initialize all components on startup"""
    global orchestrator, telemetry
  
    # Load configuration
    config = load_config()
  
    # Initialize telemetry
    telemetry = TelemetryManager(config["telemetry"])
  
    # Initialize agents
    agents = await initialize_agents(config["agents"])
  
    # Initialize orchestrator
    orchestrator = AdvisoryOrchestrator(agents, config["orchestrator"])
  
    # Initialize MCP tools
    mcp_hub = MCPToolHub(config["mcp"])
    await mcp_hub.initialize()

class AdvisoryRequest(BaseModel):
    company_id: str
    user_id: str
    request_type: str  # "full_analysis", "quick_check", "forecast", "what_if"
    parameters: Optional[Dict] = {}
    streaming: bool = False

class AdvisoryResponse(BaseModel):
    request_id: str
    status: str
    results: Dict
    processing_time: float
    confidence_scores: Dict

@app.post("/api/v1/advisory/analyze")
async def analyze(
    request: AdvisoryRequest,
    background_tasks: BackgroundTasks
) -> AdvisoryResponse:
    """Run financial analysis"""
  
    with telemetry.meter.create_counter("requests").add(
        1, {"type": request.request_type}
    ):
        if request.streaming:
            return StreamingResponse(
                stream_analysis(request),
                media_type="text/event-stream"
            )
        else:
            result = await orchestrator.run(request.dict())
          
            # Schedule background tasks
            background_tasks.add_task(
                store_analysis_results,
                request.company_id,
                result
            )
          
            return AdvisoryResponse(**result)

async def stream_analysis(request: AdvisoryRequest):
    """Stream analysis results as they become available"""
    async for event in orchestrator.workflow.astream_events(
        request.dict(),
        version="v1"
    ):
        if event["event"] == "on_chain_end":
            yield f"data: {json.dumps(event['data'])}\n\n"

@app.get("/api/v1/advisory/health/{company_id}")
async def get_financial_health(company_id: str) -> Dict:
    """Get latest financial health snapshot"""
    # Quick analysis using cached data
    pass

@app.post("/api/v1/advisory/forecast/{company_id}")
async def generate_forecast(
    company_id: str,
    scenario: Optional[Dict] = None
) -> Dict:
    """Generate cash flow and P&L forecasts"""
    pass

@app.get("/api/v1/advisory/alerts/{company_id}")
async def get_alerts(company_id: str) -> Dict:
    """Get active alerts and warnings"""
    pass
```

## 8. Configuration Files

### 8.1 Agent Configuration (agents.yaml)

```yaml
agents:
  data_collector:
    model: "gpt-4-turbo"
    temperature: 0.1
    max_retries: 3
    timeout: 30
    tools:
      - erp_connector
      - accounting_connector
      - bank_connector
  
  analyzer:
    model: "gpt-4-turbo"
    temperature: 0.3
    system_prompt: |
      You are an expert financial analyst specializing in SMB financial health.
      Analyze data with industry-specific insights and identify key patterns.
    tools:
      - financial_calculator
      - industry_benchmarks
      - ratio_analyzer
  
  forecaster:
    model: "gpt-4-turbo"
    temperature: 0.2
    system_prompt: |
      You are an expert at financial forecasting and scenario planning.
      Generate accurate forecasts based on historical data and trends.
    tools:
      - forecasting_models
      - scenario_generator
      - monte_carlo_simulator

orchestrator:
  max_iterations: 10
  timeout: 120
  checkpoint_interval: 5
  
mcp:
  servers:
    - name: "internal_tools"
      host: "localhost"
      port: 5000
      tools:
        - save_to_memory
        - retrieve_from_memory
        - calculate_metrics
  
    - name: "industry_tools"
      host: "industry-mcp.example.com"
      port: 5001
      auth:
        type: "api_key"
        key: "${INDUSTRY_MCP_API_KEY}"
```

## 9. Docker Compose Setup

```yaml
version: '3.8'

services:
  advisory-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DATABASE_URL=postgresql://user:pass@db:5432/advisory
      - REDIS_URL=redis://redis:6379
      - OTLP_ENDPOINT=http://otel-collector:4317
    depends_on:
      - db
      - redis
      - otel-collector
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=advisory
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
  
  otel-collector:
    image: otel/opentelemetry-collector:latest
    ports:
      - "4317:4317"  # OTLP gRPC
      - "4318:4318"  # OTLP HTTP
    volumes:
      - ./config/otel-collector.yaml:/etc/otel-collector.yaml
    command: ["--config=/etc/otel-collector.yaml"]
  
  langfuse:
    image: langfuse/langfuse:latest
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/langfuse
      - NEXTAUTH_SECRET=${NEXTAUTH_SECRET}
      - NEXTAUTH_URL=http://localhost:3000

volumes:
  postgres_data:
```

## 10. Next Steps

1. **Implement core agents** theo thứ tự ưu tiên:
   * Data Collector (kết nối ERP/accounting)
   * Analyzer (phân tích tài chính)
   * Forecaster (dự báo)
   * Alert Manager (cảnh báo)
2. **Tích hợp MCP tools** :

* Internal tools (memory, calculation)
* Industry-specific tools
* External data sources

1. **Testing & Validation** :

* Unit tests cho từng agent
* Integration tests cho workflow
* Load testing cho streaming

1. **Deployment** :

* CI/CD pipeline
* Monitoring dashboard
* Alert configuration
