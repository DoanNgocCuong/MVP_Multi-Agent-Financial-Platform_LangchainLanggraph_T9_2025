"""
Financial data models
"""

from sqlalchemy import Column, String, Numeric, DateTime, Text, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from decimal import Decimal
from typing import Dict, Any, List, Optional
import uuid

from ..core.database import Base
from .enums import TransactionType, TransactionStatus, AccountType, InvoiceStatus, ForecastType


class Transaction(Base):
    """Transaction model for financial transactions"""
    
    __tablename__ = "transactions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    amount = Column(Numeric(precision=15, scale=2), nullable=False)
    currency = Column(String(3), nullable=False, default="USD")
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    type = Column(String(20), nullable=False)  # TransactionType enum
    category = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    source_system = Column(String(50), nullable=True)
    confidence_score = Column(Float, nullable=True)
    status = Column(String(20), nullable=False, default=TransactionStatus.PENDING)
    metadata = Column(JSON, nullable=True)
    
    # Relationships
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=True)
    account = relationship("Account", back_populates="transactions")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"<Transaction(id={self.id}, amount={self.amount}, type={self.type})>"


class Account(Base):
    """Account model for financial accounts"""
    
    __tablename__ = "accounts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), nullable=False)
    type = Column(String(20), nullable=False)  # AccountType enum
    balance = Column(Numeric(precision=15, scale=2), nullable=False, default=0)
    currency = Column(String(3), nullable=False, default="USD")
    external_id = Column(String(100), nullable=True)
    source_system = Column(String(50), nullable=True)
    last_sync = Column(DateTime, nullable=True)
    
    # Relationships
    transactions = relationship("Transaction", back_populates="account")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"<Account(id={self.id}, name={self.name}, type={self.type})>"


class Invoice(Base):
    """Invoice model for invoice management"""
    
    __tablename__ = "invoices"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    invoice_number = Column(String(100), nullable=False, unique=True)
    amount = Column(Numeric(precision=15, scale=2), nullable=False)
    currency = Column(String(3), nullable=False, default="USD")
    issue_date = Column(DateTime, nullable=False)
    due_date = Column(DateTime, nullable=False)
    customer_id = Column(String(100), nullable=True)
    status = Column(String(20), nullable=False, default=InvoiceStatus.DRAFT)
    payment_terms = Column(String(50), nullable=True)  # e.g., "NET30"
    confidence_score = Column(Float, nullable=True)
    
    # Relationships
    line_items = relationship("InvoiceLineItem", back_populates="invoice", cascade="all, delete-orphan")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"<Invoice(id={self.id}, number={self.invoice_number}, amount={self.amount})>"


class InvoiceLineItem(Base):
    """Invoice line item model"""
    
    __tablename__ = "invoice_line_items"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    description = Column(Text, nullable=False)
    quantity = Column(Numeric(precision=10, scale=2), nullable=False)
    unit_price = Column(Numeric(precision=15, scale=2), nullable=False)
    total_amount = Column(Numeric(precision=15, scale=2), nullable=False)
    
    # Relationships
    invoice_id = Column(UUID(as_uuid=True), ForeignKey("invoices.id"), nullable=False)
    invoice = relationship("Invoice", back_populates="line_items")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"<InvoiceLineItem(id={self.id}, description={self.description})>"


class Forecast(Base):
    """Forecast model for financial forecasting"""
    
    __tablename__ = "forecasts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = Column(String(20), nullable=False)  # ForecastType enum
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    confidence_interval = Column(Float, nullable=True)
    methodology = Column(String(100), nullable=True)
    
    # Relationships
    predictions = relationship("ForecastPrediction", back_populates="forecast", cascade="all, delete-orphan")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"<Forecast(id={self.id}, type={self.type}, period={self.period_start}-{self.period_end})>"


class ForecastPrediction(Base):
    """Forecast prediction model for individual forecast data points"""
    
    __tablename__ = "forecast_predictions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date = Column(DateTime, nullable=False)
    predicted_value = Column(Numeric(precision=15, scale=2), nullable=False)
    confidence_score = Column(Float, nullable=True)
    category = Column(String(100), nullable=True)
    metadata = Column(JSON, nullable=True)
    
    # Relationships
    forecast_id = Column(UUID(as_uuid=True), ForeignKey("forecasts.id"), nullable=False)
    forecast = relationship("Forecast", back_populates="predictions")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"<ForecastPrediction(id={self.id}, date={self.date}, value={self.predicted_value})>"