"""Core financial data models."""

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field, validator


class TransactionType(str, Enum):
    """Transaction type enumeration."""
    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"
    ADJUSTMENT = "adjustment"


class TransactionStatus(str, Enum):
    """Transaction status enumeration."""
    PENDING = "pending"
    PROCESSED = "processed"
    RECONCILED = "reconciled"
    DISPUTED = "disputed"
    CANCELLED = "cancelled"


class AccountType(str, Enum):
    """Account type enumeration."""
    ASSET = "asset"
    LIABILITY = "liability"
    EQUITY = "equity"
    REVENUE = "revenue"
    EXPENSE = "expense"


class InvoiceStatus(str, Enum):
    """Invoice status enumeration."""
    DRAFT = "draft"
    SENT = "sent"
    VIEWED = "viewed"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"


class ForecastType(str, Enum):
    """Forecast type enumeration."""
    CASH_FLOW = "cash_flow"
    PROFIT_LOSS = "profit_loss"
    BALANCE_SHEET = "balance_sheet"
    REVENUE = "revenue"
    EXPENSES = "expenses"


class SystemType(str, Enum):
    """External system type enumeration."""
    ERP = "erp"
    POS = "pos"
    BANK = "bank"
    ACCOUNTING = "accounting"
    INDUSTRY_SPECIFIC = "industry_specific"


class ConnectionStatus(str, Enum):
    """Connection status enumeration."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    PENDING = "pending"


class Transaction(BaseModel):
    """Transaction data model."""
    
    id: str = Field(default_factory=lambda: str(uuid4()))
    amount: Decimal = Field(..., description="Transaction amount")
    currency: str = Field(default="USD", description="Currency code")
    date: datetime = Field(..., description="Transaction date")
    type: TransactionType = Field(..., description="Transaction type")
    category: str = Field(..., description="Transaction category")
    description: str = Field(..., description="Transaction description")
    source_system: str = Field(..., description="Source system identifier")
    external_id: Optional[str] = Field(None, description="External system transaction ID")
    confidence_score: float = Field(default=1.0, description="Data confidence score (0-1)")
    status: TransactionStatus = Field(default=TransactionStatus.PENDING)
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    # Accounting fields
    debit_account_id: Optional[str] = Field(None, description="Debit account ID")
    credit_account_id: Optional[str] = Field(None, description="Credit account ID")
    reference_number: Optional[str] = Field(None, description="Reference number")
    
    # Audit fields
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[str] = Field(None, description="Created by user ID")
    
    @validator("amount")
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError("Amount must be positive")
        return v
    
    @validator("confidence_score")
    def validate_confidence_score(cls, v):
        if not 0 <= v <= 1:
            raise ValueError("Confidence score must be between 0 and 1")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "amount": "1500.00",
                "currency": "USD",
                "date": "2024-01-15T10:30:00Z",
                "type": "expense",
                "category": "office_supplies",
                "description": "Office equipment purchase",
                "source_system": "quickbooks",
                "confidence_score": 0.95
            }
        }


class Account(BaseModel):
    """Account data model."""
    
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str = Field(..., description="Account name")
    code: Optional[str] = Field(None, description="Account code")
    type: AccountType = Field(..., description="Account type")
    balance: Decimal = Field(default=Decimal("0.00"), description="Current balance")
    currency: str = Field(default="USD", description="Currency code")
    external_id: Optional[str] = Field(None, description="External system account ID")
    source_system: str = Field(..., description="Source system identifier")
    parent_account_id: Optional[str] = Field(None, description="Parent account ID")
    is_active: bool = Field(default=True, description="Account active status")
    
    # Audit fields
    last_sync: Optional[datetime] = Field(None, description="Last synchronization time")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Cash - Operating Account",
                "code": "1001",
                "type": "asset",
                "balance": "25000.00",
                "currency": "USD",
                "source_system": "quickbooks"
            }
        }


class InvoiceLineItem(BaseModel):
    """Invoice line item model."""
    
    id: str = Field(default_factory=lambda: str(uuid4()))
    description: str = Field(..., description="Item description")
    quantity: Decimal = Field(..., description="Item quantity")
    unit_price: Decimal = Field(..., description="Unit price")
    total_amount: Decimal = Field(..., description="Total line amount")
    tax_amount: Optional[Decimal] = Field(None, description="Tax amount")
    
    @validator("total_amount")
    def validate_total_amount(cls, v, values):
        if "quantity" in values and "unit_price" in values:
            expected = values["quantity"] * values["unit_price"]
            if abs(v - expected) > Decimal("0.01"):
                raise ValueError("Total amount must equal quantity * unit_price")
        return v


class Invoice(BaseModel):
    """Invoice data model."""
    
    id: str = Field(default_factory=lambda: str(uuid4()))
    invoice_number: str = Field(..., description="Invoice number")
    amount: Decimal = Field(..., description="Total invoice amount")
    currency: str = Field(default="USD", description="Currency code")
    issue_date: datetime = Field(..., description="Invoice issue date")
    due_date: datetime = Field(..., description="Invoice due date")
    customer_id: str = Field(..., description="Customer identifier")
    customer_name: Optional[str] = Field(None, description="Customer name")
    status: InvoiceStatus = Field(default=InvoiceStatus.DRAFT)
    line_items: List[InvoiceLineItem] = Field(default_factory=list, description="Invoice line items")
    payment_terms: int = Field(default=30, description="Payment terms in days")
    confidence_score: float = Field(default=1.0, description="OCR confidence score")
    
    # External system fields
    external_id: Optional[str] = Field(None, description="External system invoice ID")
    source_system: str = Field(..., description="Source system identifier")
    
    # Audit fields
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    @validator("due_date")
    def validate_due_date(cls, v, values):
        if "issue_date" in values and v < values["issue_date"]:
            raise ValueError("Due date must be after issue date")
        return v
    
    @property
    def is_overdue(self) -> bool:
        """Check if invoice is overdue."""
        return self.status != InvoiceStatus.PAID and datetime.utcnow() > self.due_date
    
    @property
    def days_overdue(self) -> int:
        """Get number of days overdue."""
        if not self.is_overdue:
            return 0
        return (datetime.utcnow() - self.due_date).days


class ForecastPrediction(BaseModel):
    """Forecast prediction data point."""
    
    period: datetime = Field(..., description="Forecast period")
    predicted_value: Decimal = Field(..., description="Predicted value")
    confidence_interval_lower: Optional[Decimal] = Field(None, description="Lower confidence bound")
    confidence_interval_upper: Optional[Decimal] = Field(None, description="Upper confidence bound")
    factors: Dict[str, Any] = Field(default_factory=dict, description="Contributing factors")


class Forecast(BaseModel):
    """Financial forecast model."""
    
    id: str = Field(default_factory=lambda: str(uuid4()))
    type: ForecastType = Field(..., description="Forecast type")
    period_start: datetime = Field(..., description="Forecast period start")
    period_end: datetime = Field(..., description="Forecast period end")
    predictions: List[ForecastPrediction] = Field(default_factory=list, description="Forecast predictions")
    confidence_interval: float = Field(default=0.95, description="Confidence interval (0-1)")
    methodology: str = Field(..., description="Forecasting methodology used")
    input_data_sources: List[str] = Field(default_factory=list, description="Input data sources")
    
    # Metadata
    company_id: str = Field(..., description="Company identifier")
    created_by: str = Field(..., description="Created by agent/user ID")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    @validator("confidence_interval")
    def validate_confidence_interval(cls, v):
        if not 0 < v < 1:
            raise ValueError("Confidence interval must be between 0 and 1")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "type": "cash_flow",
                "period_start": "2024-01-01T00:00:00Z",
                "period_end": "2024-03-31T23:59:59Z",
                "confidence_interval": 0.95,
                "methodology": "ARIMA with seasonal adjustment",
                "company_id": "company_123"
            }
        }


class ExternalSystem(BaseModel):
    """External system connection model."""
    
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str = Field(..., description="System name")
    type: SystemType = Field(..., description="System type")
    connection_config: Dict[str, Any] = Field(default_factory=dict, description="Connection configuration")
    sync_frequency: str = Field(default="hourly", description="Synchronization frequency")
    last_sync: Optional[datetime] = Field(None, description="Last synchronization time")
    status: ConnectionStatus = Field(default=ConnectionStatus.PENDING)
    
    # Company association
    company_id: str = Field(..., description="Company identifier")
    
    # Audit fields
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "QuickBooks Online",
                "type": "accounting",
                "connection_config": {
                    "client_id": "xxx",
                    "sandbox": True,
                    "base_url": "https://sandbox-quickbooks.api.intuit.com"
                },
                "sync_frequency": "hourly",
                "company_id": "company_123"
            }
        }


class TransformationRule(BaseModel):
    """Data transformation rule."""
    
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str = Field(..., description="Rule name")
    source_field: str = Field(..., description="Source field path")
    target_field: str = Field(..., description="Target field path")
    transformation_type: str = Field(..., description="Transformation type")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Transformation parameters")
    is_active: bool = Field(default=True, description="Rule active status")


class ValidationRule(BaseModel):
    """Data validation rule."""
    
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str = Field(..., description="Rule name")
    field_path: str = Field(..., description="Field path to validate")
    validation_type: str = Field(..., description="Validation type")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Validation parameters")
    error_message: str = Field(..., description="Error message template")
    is_active: bool = Field(default=True, description="Rule active status")


class DataMapping(BaseModel):
    """Data mapping configuration between systems."""
    
    id: str = Field(default_factory=lambda: str(uuid4()))
    source_system: str = Field(..., description="Source system identifier")
    target_system: str = Field(..., description="Target system identifier")
    entity_type: str = Field(..., description="Entity type being mapped")
    field_mappings: Dict[str, str] = Field(default_factory=dict, description="Field mappings")
    transformation_rules: List[TransformationRule] = Field(default_factory=list, description="Transformation rules")
    validation_rules: List[ValidationRule] = Field(default_factory=list, description="Validation rules")
    
    # Configuration
    is_active: bool = Field(default=True, description="Mapping active status")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "source_system": "quickbooks",
                "target_system": "internal",
                "entity_type": "transaction",
                "field_mappings": {
                    "TxnDate": "date",
                    "Amount": "amount",
                    "Description": "description"
                }
            }
        }