# Data Models

## 📁 Overview

The `models/` directory contains all data models and schemas used throughout the AI Financial Multi-Agent System. These models define the structure of data for agents, financial information, workflows, and system integrations.

## 🏗️ Directory Structure

```
models/
├── __init__.py           # Package initialization and exports
├── agent_models.py       # Agent-related data models
├── agent.py              # Agent state and context models
├── enums.py              # System enumerations and constants
├── financial_models.py   # Financial data models
├── financial.py          # Financial domain models
└── integration.py        # External integration models
```

## 🧩 Model Categories

### 1. Agent Models (`agent_models.py`)

Core models for agent functionality and state management.

#### `AgentContext`
Context information for agent execution:

```python
class AgentContext(BaseModel):
    agent_id: str
    session_id: str
    user_id: str
    company_id: str
    permissions: List[str]
    state: Dict[str, Any]
    trace_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

**Usage Example:**
```python
from ai_financial.models.agent_models import AgentContext

context = AgentContext(
    agent_id="ai_cfo_agent",
    session_id="session_123",
    user_id="user_456",
    company_id="company_789",
    permissions=["read_financial_data", "write_reports"],
    state={"current_analysis": "financial_health"}
)
```

#### `AgentState`
State management for agent workflows:

```python
class AgentState(BaseModel):
    messages: List[BaseMessage] = Field(default_factory=list)
    context: Optional[AgentContext] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    completed_steps: List[str] = Field(default_factory=list)
    current_step: Optional[str] = None
    error: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Usage Example:**
```python
from ai_financial.models.agent_models import AgentState
from langchain_core.messages import HumanMessage

state = AgentState(
    messages=[HumanMessage(content="Analyze our financial health")],
    context=context,
    metadata={"analysis_type": "comprehensive"}
)
```

#### `WorkflowState`
Multi-step workflow state management:

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
```

### 2. Agent Models (`agent.py`)

Additional agent-related models and utilities.

#### Agent Configuration Models

```python
class AgentConfig(BaseModel):
    agent_id: str
    name: str
    description: str
    capabilities: List[str]
    industry: Optional[str] = None
    configuration: Dict[str, Any] = Field(default_factory=dict)
```

#### Agent Performance Models

```python
class AgentPerformance(BaseModel):
    agent_id: str
    requests_processed: int
    average_response_time: float
    success_rate: float
    error_count: int
    last_updated: datetime = Field(default_factory=datetime.utcnow)
```

### 3. Enumerations (`enums.py`)

System-wide enumerations and constants.

#### `AgentStatus`
Agent and workflow status enumeration:

```python
class AgentStatus(str, Enum):
    IDLE = "idle"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PENDING_APPROVAL = "pending_approval"
```

#### `WorkflowType`
Workflow type enumeration:

```python
class WorkflowType(str, Enum):
    ADVISORY = "advisory"
    TRANSACTIONAL = "transactional"
    CUSTOM = "custom"
```

#### `FinancialMetricType`
Financial metric types:

```python
class FinancialMetricType(str, Enum):
    LIQUIDITY = "liquidity"
    PROFITABILITY = "profitability"
    LEVERAGE = "leverage"
    EFFICIENCY = "efficiency"
    MARKET = "market"
```

#### `IndustryType`
Supported industry types:

```python
class IndustryType(str, Enum):
    GENERAL = "general"
    HEALTHCARE = "healthcare"
    AUTOMOTIVE = "automotive"
    PHARMACEUTICAL = "pharmaceutical"
    TECHNOLOGY = "technology"
    MANUFACTURING = "manufacturing"
```

### 4. Financial Models (`financial_models.py`)

Core financial data models and structures.

#### `Transaction`
Financial transaction model:

```python
class Transaction(BaseModel):
    transaction_id: str = Field(default_factory=lambda: str(uuid4()))
    amount: Decimal
    currency: str = "USD"
    transaction_type: str  # income, expense, transfer
    category: str
    description: str
    date: datetime
    account_id: str
    company_id: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

**Usage Example:**
```python
from ai_financial.models.financial_models import Transaction
from decimal import Decimal

transaction = Transaction(
    amount=Decimal("15000.00"),
    transaction_type="income",
    category="sales_revenue",
    description="Monthly sales revenue",
    date=datetime.utcnow(),
    account_id="acc_123",
    company_id="company_456"
)
```

#### `Account`
Account information model:

```python
class Account(BaseModel):
    account_id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    account_type: str  # asset, liability, equity, revenue, expense
    balance: Decimal
    currency: str = "USD"
    company_id: str
    is_active: bool = True
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

#### `Invoice`
Invoice data model:

```python
class Invoice(BaseModel):
    invoice_id: str = Field(default_factory=lambda: str(uuid4()))
    invoice_number: str
    amount: Decimal
    currency: str = "USD"
    status: str  # draft, sent, paid, overdue, cancelled
    due_date: datetime
    issue_date: datetime
    customer_id: str
    company_id: str
    line_items: List[Dict[str, Any]] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

#### `Forecast`
Financial forecasting model:

```python
class Forecast(BaseModel):
    forecast_id: str = Field(default_factory=lambda: str(uuid4()))
    forecast_type: ForecastType
    period_start: datetime
    period_end: datetime
    company_id: str
    data: Dict[str, Any]  # Forecasted financial data
    confidence_level: float = Field(ge=0.0, le=1.0)
    methodology: str
    assumptions: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### 5. Financial Domain Models (`financial.py`)

Domain-specific financial models and calculations.

#### `FinancialRatio`
Financial ratio calculation model:

```python
class FinancialRatio(BaseModel):
    ratio_name: str
    ratio_value: Optional[float] = None
    calculation_method: str
    interpretation: str
    benchmark_range: Dict[str, float]
    industry_average: Optional[float] = None
    calculation_date: datetime = Field(default_factory=datetime.utcnow)
```

#### `CashFlowStatement`
Cash flow statement model:

```python
class CashFlowStatement(BaseModel):
    period_start: datetime
    period_end: datetime
    company_id: str
    operating_cash_flow: Decimal
    investing_cash_flow: Decimal
    financing_cash_flow: Decimal
    net_cash_flow: Decimal
    beginning_cash: Decimal
    ending_cash: Decimal
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

#### `BalanceSheet`
Balance sheet model:

```python
class BalanceSheet(BaseModel):
    as_of_date: datetime
    company_id: str
    assets: Dict[str, Decimal] = Field(default_factory=dict)
    liabilities: Dict[str, Decimal] = Field(default_factory=dict)
    equity: Dict[str, Decimal] = Field(default_factory=dict)
    total_assets: Decimal
    total_liabilities: Decimal
    total_equity: Decimal
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

#### `IncomeStatement`
Income statement model:

```python
class IncomeStatement(BaseModel):
    period_start: datetime
    period_end: datetime
    company_id: str
    revenue: Decimal
    cost_of_goods_sold: Decimal
    gross_profit: Decimal
    operating_expenses: Decimal
    operating_income: Decimal
    interest_expense: Decimal
    net_income: Decimal
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

### 6. Integration Models (`integration.py`)

Models for external system integrations.

#### `ExternalSystemConfig`
External system configuration:

```python
class ExternalSystemConfig(BaseModel):
    system_name: str
    system_type: str  # erp, accounting, banking, pos
    connection_config: Dict[str, Any]
    authentication: Dict[str, Any]
    sync_settings: Dict[str, Any] = Field(default_factory=dict)
    is_active: bool = True
    last_sync: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

#### `DataSyncJob`
Data synchronization job model:

```python
class DataSyncJob(BaseModel):
    job_id: str = Field(default_factory=lambda: str(uuid4()))
    system_config: ExternalSystemConfig
    sync_type: str  # full, incremental, real_time
    status: str  # pending, running, completed, failed
    records_processed: int = 0
    records_successful: int = 0
    records_failed: int = 0
    error_messages: List[str] = Field(default_factory=list)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

#### `APIIntegration`
API integration model:

```python
class APIIntegration(BaseModel):
    integration_id: str = Field(default_factory=lambda: str(uuid4()))
    api_name: str
    base_url: str
    authentication_type: str  # api_key, oauth, basic
    headers: Dict[str, str] = Field(default_factory=dict)
    rate_limits: Dict[str, int] = Field(default_factory=dict)
    is_active: bool = True
    last_health_check: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

## 🔧 Model Usage

### Creating Model Instances

```python
from ai_financial.models.financial_models import Transaction, Account
from ai_financial.models.agent_models import AgentContext, AgentState
from decimal import Decimal

# Create financial models
account = Account(
    name="Operating Cash Account",
    account_type="asset",
    balance=Decimal("125000.00"),
    company_id="company_123"
)

transaction = Transaction(
    amount=Decimal("15000.00"),
    transaction_type="income",
    category="sales_revenue",
    description="Monthly sales revenue",
    date=datetime.utcnow(),
    account_id=account.account_id,
    company_id="company_123"
)

# Create agent context
context = AgentContext(
    agent_id="ai_cfo_agent",
    session_id="session_456",
    user_id="user_789",
    company_id="company_123",
    permissions=["read_financial_data"]
)

# Create agent state
state = AgentState(
    messages=[HumanMessage(content="Analyze financial health")],
    context=context,
    metadata={"analysis_type": "comprehensive"}
)
```

### Model Validation

```python
from pydantic import ValidationError

try:
    transaction = Transaction(
        amount=Decimal("15000.00"),
        transaction_type="invalid_type",  # This will raise validation error
        category="sales_revenue",
        description="Monthly sales revenue",
        date=datetime.utcnow(),
        account_id="acc_123",
        company_id="company_456"
    )
except ValidationError as e:
    print(f"Validation error: {e}")
```

### Model Serialization

```python
# Convert to dictionary
transaction_dict = transaction.model_dump()

# Convert to JSON
transaction_json = transaction.model_dump_json()

# Convert from dictionary
transaction_from_dict = Transaction.model_validate(transaction_dict)

# Convert from JSON
transaction_from_json = Transaction.model_validate_json(transaction_json)
```

## 🧪 Model Testing

### Unit Testing

```python
import pytest
from ai_financial.models.financial_models import Transaction, Account
from ai_financial.models.agent_models import AgentContext, AgentState
from decimal import Decimal

def test_transaction_creation():
    """Test transaction model creation."""
    transaction = Transaction(
        amount=Decimal("15000.00"),
        transaction_type="income",
        category="sales_revenue",
        description="Monthly sales revenue",
        date=datetime.utcnow(),
        account_id="acc_123",
        company_id="company_456"
    )
    
    assert transaction.amount == Decimal("15000.00")
    assert transaction.transaction_type == "income"
    assert transaction.category == "sales_revenue"

def test_agent_context_validation():
    """Test agent context validation."""
    context = AgentContext(
        agent_id="ai_cfo_agent",
        session_id="session_123",
        user_id="user_456",
        company_id="company_789",
        permissions=["read_financial_data"]
    )
    
    assert context.agent_id == "ai_cfo_agent"
    assert "read_financial_data" in context.permissions

def test_financial_ratio_calculation():
    """Test financial ratio model."""
    ratio = FinancialRatio(
        ratio_name="current_ratio",
        ratio_value=2.0,
        calculation_method="current_assets / current_liabilities",
        interpretation="Strong liquidity position",
        benchmark_range={"min": 1.0, "good": 2.0, "max": 3.0}
    )
    
    assert ratio.ratio_value == 2.0
    assert ratio.interpretation == "Strong liquidity position"
```

### Integration Testing

```python
@pytest.mark.asyncio
async def test_agent_state_workflow():
    """Test agent state workflow."""
    context = AgentContext(
        agent_id="ai_cfo_agent",
        session_id="session_123",
        user_id="user_456",
        company_id="company_789",
        permissions=["read_financial_data"]
    )
    
    state = AgentState(
        messages=[HumanMessage(content="Analyze financial health")],
        context=context
    )
    
    # Simulate workflow steps
    state.completed_steps.append("request_analysis")
    state.current_step = "data_gathering"
    state.metadata["analysis_type"] = "comprehensive"
    
    assert "request_analysis" in state.completed_steps
    assert state.current_step == "data_gathering"
    assert state.metadata["analysis_type"] == "comprehensive"
```

## 📊 Model Relationships

### Financial Data Relationships

```python
# Company has multiple accounts
company_id = "company_123"

accounts = [
    Account(name="Cash Account", account_type="asset", balance=Decimal("100000"), company_id=company_id),
    Account(name="Accounts Receivable", account_type="asset", balance=Decimal("50000"), company_id=company_id),
    Account(name="Accounts Payable", account_type="liability", balance=Decimal("25000"), company_id=company_id)
]

# Transactions belong to accounts
transactions = [
    Transaction(amount=Decimal("15000"), transaction_type="income", account_id=accounts[0].account_id, company_id=company_id),
    Transaction(amount=Decimal("5000"), transaction_type="expense", account_id=accounts[2].account_id, company_id=company_id)
]

# Invoices are related to transactions
invoices = [
    Invoice(invoice_number="INV-001", amount=Decimal("15000"), customer_id="customer_123", company_id=company_id)
]
```

### Agent Workflow Relationships

```python
# Agent context contains session information
context = AgentContext(
    agent_id="ai_cfo_agent",
    session_id="session_123",
    user_id="user_456",
    company_id="company_789"
)

# Agent state contains workflow information
state = AgentState(
    messages=[HumanMessage(content="Analyze financial health")],
    context=context,
    metadata={"analysis_type": "comprehensive"}
)

# Workflow state contains multi-step process information
workflow_state = WorkflowState(
    workflow_type="advisory",
    context=context,
    data={"request": "Analyze financial health"},
    status=AgentStatus.PROCESSING
)
```

## 🔍 Model Validation

### Custom Validators

```python
from pydantic import validator

class Transaction(BaseModel):
    amount: Decimal
    transaction_type: str
    category: str
    description: str
    date: datetime
    account_id: str
    company_id: str
    
    @validator('amount')
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError('Amount must be positive')
        return v
    
    @validator('transaction_type')
    def validate_transaction_type(cls, v):
        allowed_types = ['income', 'expense', 'transfer']
        if v not in allowed_types:
            raise ValueError(f'Transaction type must be one of {allowed_types}')
        return v
```

### Field Validation

```python
from pydantic import Field, validator

class FinancialRatio(BaseModel):
    ratio_name: str
    ratio_value: Optional[float] = Field(None, ge=0.0)  # Must be non-negative
    confidence_level: float = Field(0.95, ge=0.0, le=1.0)  # Between 0 and 1
    calculation_date: datetime = Field(default_factory=datetime.utcnow)
    
    @validator('ratio_value')
    def validate_ratio_value(cls, v):
        if v is not None and v > 1000:
            raise ValueError('Ratio value seems unreasonably high')
        return v
```

## 📚 Additional Resources

- **Pydantic Documentation**: https://pydantic-docs.helpmanual.io/
- **Model Validation**: See individual model files for validation rules
- **Financial Calculations**: See `financial_models.py` for calculation methods
- **Agent Integration**: See `agent_models.py` for agent-specific models
- **External Integrations**: See `integration.py` for integration models

