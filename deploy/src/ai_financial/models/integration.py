"""
Integration and external system models
"""

from sqlalchemy import Column, String, DateTime, Text, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from typing import Dict, Any, List, Optional
import uuid

from ..core.database import Base
from .enums import SystemType, ConnectionStatus


class ExternalSystem(Base):
    """External system connection model"""
    
    __tablename__ = "external_systems"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), nullable=False)
    type = Column(String(20), nullable=False)  # SystemType enum
    connection_config = Column(JSON, nullable=False)  # API endpoints, credentials, etc.
    sync_frequency = Column(String(50), nullable=True)  # e.g., "hourly", "daily", "real-time"
    last_sync = Column(DateTime, nullable=True)
    status = Column(String(20), nullable=False, default=ConnectionStatus.DISCONNECTED)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    data_mappings = relationship("DataMapping", back_populates="external_system", cascade="all, delete-orphan")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"<ExternalSystem(id={self.id}, name={self.name}, type={self.type})>"


class DataMapping(Base):
    """Data mapping configuration model"""
    
    __tablename__ = "data_mappings"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_system = Column(String(100), nullable=False)
    target_system = Column(String(100), nullable=False)
    field_mappings = Column(JSON, nullable=False)  # Dict mapping source fields to target fields
    is_active = Column(Boolean, default=True)
    
    # Relationships
    external_system_id = Column(UUID(as_uuid=True), nullable=True)
    external_system = relationship("ExternalSystem", back_populates="data_mappings")
    
    transformation_rules = relationship("TransformationRule", back_populates="data_mapping", cascade="all, delete-orphan")
    validation_rules = relationship("ValidationRule", back_populates="data_mapping", cascade="all, delete-orphan")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"<DataMapping(id={self.id}, source={self.source_system}, target={self.target_system})>"


class TransformationRule(Base):
    """Data transformation rule model"""
    
    __tablename__ = "transformation_rules"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rule_name = Column(String(200), nullable=False)
    field_name = Column(String(100), nullable=False)
    transformation_type = Column(String(50), nullable=False)  # e.g., "format", "calculate", "lookup"
    transformation_config = Column(JSON, nullable=False)  # Configuration for the transformation
    order = Column(String(10), nullable=False, default=1)  # Execution order
    is_active = Column(Boolean, default=True)
    
    # Relationships
    data_mapping_id = Column(UUID(as_uuid=True), nullable=False)
    data_mapping = relationship("DataMapping", back_populates="transformation_rules")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"<TransformationRule(id={self.id}, name={self.rule_name}, type={self.transformation_type})>"


class ValidationRule(Base):
    """Data validation rule model"""
    
    __tablename__ = "validation_rules"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rule_name = Column(String(200), nullable=False)
    field_name = Column(String(100), nullable=False)
    validation_type = Column(String(50), nullable=False)  # e.g., "required", "format", "range", "custom"
    validation_config = Column(JSON, nullable=False)  # Configuration for the validation
    error_message = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    data_mapping_id = Column(UUID(as_uuid=True), nullable=False)
    data_mapping = relationship("DataMapping", back_populates="validation_rules")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"<ValidationRule(id={self.id}, name={self.rule_name}, type={self.validation_type})>"


class SyncLog(Base):
    """Data synchronization log model"""
    
    __tablename__ = "sync_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    external_system_id = Column(UUID(as_uuid=True), nullable=False)
    sync_type = Column(String(50), nullable=False)  # e.g., "full", "incremental", "real-time"
    status = Column(String(20), nullable=False)  # success, error, partial
    records_processed = Column(String(20), nullable=True)
    records_success = Column(String(20), nullable=True)
    records_failed = Column(String(20), nullable=True)
    error_details = Column(JSON, nullable=True)
    
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    def __repr__(self) -> str:
        return f"<SyncLog(id={self.id}, system_id={self.external_system_id}, status={self.status})>"


class APICredential(Base):
    """API credential storage model"""
    
    __tablename__ = "api_credentials"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    system_name = Column(String(100), nullable=False)
    credential_type = Column(String(50), nullable=False)  # e.g., "api_key", "oauth", "basic_auth"
    encrypted_credentials = Column(Text, nullable=False)  # Encrypted credential data
    is_active = Column(Boolean, default=True)
    expires_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"<APICredential(id={self.id}, system={self.system_name}, type={self.credential_type})>"