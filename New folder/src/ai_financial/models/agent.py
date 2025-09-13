"""
Agent and workflow models
"""

from sqlalchemy import Column, String, DateTime, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from typing import Dict, Any, List, Optional
import uuid

from ..core.database import Base
from .enums import WorkflowStatus, ApprovalStatus, AgentType


class AgentContext(Base):
    """Agent execution context model"""
    
    __tablename__ = "agent_contexts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(String(100), nullable=False)
    agent_type = Column(String(50), nullable=False)  # AgentType enum
    session_id = Column(String(100), nullable=False)
    user_id = Column(String(100), nullable=True)
    company_id = Column(String(100), nullable=True)
    permissions = Column(JSON, nullable=True)  # List of permission strings
    state = Column(JSON, nullable=True)  # Agent state data
    trace_id = Column(String(100), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"<AgentContext(id={self.id}, agent_id={self.agent_id}, type={self.agent_type})>"


class WorkflowState(Base):
    """Workflow state management model"""
    
    __tablename__ = "workflow_states"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workflow_id = Column(String(100), nullable=False, unique=True)
    workflow_type = Column(String(50), nullable=False)  # e.g., "advisory", "transactional"
    current_step = Column(String(100), nullable=False)
    steps_completed = Column(JSON, nullable=True)  # List of completed step names
    status = Column(String(20), nullable=False, default=WorkflowStatus.PENDING)
    data = Column(JSON, nullable=True)  # Workflow data
    error_message = Column(Text, nullable=True)
    
    # Relationships
    approval_requests = relationship("ApprovalRequest", back_populates="workflow", cascade="all, delete-orphan")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"<WorkflowState(id={self.id}, workflow_id={self.workflow_id}, status={self.status})>"


class ApprovalRequest(Base):
    """Approval request model for HITL workflows"""
    
    __tablename__ = "approval_requests"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_type = Column(String(50), nullable=False)  # e.g., "transaction_approval", "policy_exception"
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    requested_by = Column(String(100), nullable=False)
    approver_id = Column(String(100), nullable=True)
    status = Column(String(20), nullable=False, default=ApprovalStatus.PENDING)
    priority = Column(String(20), nullable=False, default="medium")  # low, medium, high, critical
    data = Column(JSON, nullable=True)  # Request-specific data
    approval_reason = Column(Text, nullable=True)
    rejection_reason = Column(Text, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    approved_at = Column(DateTime, nullable=True)
    
    # Relationships
    workflow_id = Column(UUID(as_uuid=True), ForeignKey("workflow_states.id"), nullable=True)
    workflow = relationship("WorkflowState", back_populates="approval_requests")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"<ApprovalRequest(id={self.id}, type={self.request_type}, status={self.status})>"


class AgentExecution(Base):
    """Agent execution tracking model"""
    
    __tablename__ = "agent_executions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_type = Column(String(50), nullable=False)  # AgentType enum
    execution_id = Column(String(100), nullable=False)
    input_data = Column(JSON, nullable=True)
    output_data = Column(JSON, nullable=True)
    status = Column(String(20), nullable=False)  # success, error, timeout
    execution_time_ms = Column(String(20), nullable=True)
    error_message = Column(Text, nullable=True)
    trace_id = Column(String(100), nullable=True)
    
    # Context information
    context_id = Column(UUID(as_uuid=True), ForeignKey("agent_contexts.id"), nullable=True)
    context = relationship("AgentContext")
    
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    def __repr__(self) -> str:
        return f"<AgentExecution(id={self.id}, agent_type={self.agent_type}, status={self.status})>"


class AgentMemory(Base):
    """Agent memory storage model"""
    
    __tablename__ = "agent_memories"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(String(100), nullable=False)
    memory_key = Column(String(200), nullable=False)
    memory_value = Column(JSON, nullable=False)
    memory_type = Column(String(50), nullable=False)  # e.g., "conversation", "context", "learned_pattern"
    expires_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"<AgentMemory(id={self.id}, agent_id={self.agent_id}, key={self.memory_key})>"