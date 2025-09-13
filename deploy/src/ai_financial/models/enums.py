"""
Enumerations for AI Financial Multi-Agent System
"""

from enum import Enum


class TransactionType(str, Enum):
    """Transaction type enumeration"""
    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"


class TransactionStatus(str, Enum):
    """Transaction status enumeration"""
    PENDING = "pending"
    PROCESSED = "processed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class AccountType(str, Enum):
    """Account type enumeration following accounting principles"""
    ASSET = "asset"
    LIABILITY = "liability"
    EQUITY = "equity"
    REVENUE = "revenue"
    EXPENSE = "expense"


class InvoiceStatus(str, Enum):
    """Invoice status enumeration"""
    DRAFT = "draft"
    SENT = "sent"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"


class ForecastType(str, Enum):
    """Forecast type enumeration"""
    CASH_FLOW = "cash_flow"
    PL = "profit_loss"
    BALANCE_SHEET = "balance_sheet"


class SystemType(str, Enum):
    """External system type enumeration"""
    ERP = "erp"
    POS = "pos"
    BANK = "bank"
    ACCOUNTING = "accounting"
    INDUSTRY = "industry"


class ConnectionStatus(str, Enum):
    """Connection status enumeration"""
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"
    SYNCING = "syncing"


class WorkflowStatus(str, Enum):
    """Workflow status enumeration"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ApprovalStatus(str, Enum):
    """Approval status enumeration"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"


class AgentType(str, Enum):
    """Agent type enumeration"""
    AI_CFO = "ai_cfo"
    FORECASTING = "forecasting"
    ALERT = "alert"
    REPORTING = "reporting"
    OCR_PROCESSING = "ocr_processing"
    DATA_SYNC = "data_sync"
    ACCOUNTING_AUTOMATION = "accounting_automation"
    RECONCILIATION = "reconciliation"
    COMPLIANCE = "compliance"
    ORCHESTRATOR = "orchestrator"