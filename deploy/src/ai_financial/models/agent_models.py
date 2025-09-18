"""Agent-related data models."""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4

from langchain.schema import BaseMessage
from pydantic import BaseModel, Field


class AgentStatus(str, Enum):
    """Agent execution status."""
    IDLE = "idle"
    PROCESSING = "processing"
    WAITING = "waiting"
    ERROR = "error"
    COMPLETED = "completed"


class AgentContext(BaseModel):
    """Agent execution context."""
    
    agent_id: str = Field(..., description="Unique identifier for the agent")
    session_id: str = Field(default_factory=lambda: str(uuid4()), description="Session identifier")
    user_id: str = Field(..., description="User identifier")
    company_id: str = Field(..., description="Company identifier")
    permissions: List[str] = Field(default_factory=list, description="User permissions")
    state: Dict[str, Any] = Field(default_factory=dict, description="Agent state data")
    trace_id: Optional[int] = Field(None, description="OpenTelemetry trace ID")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        arbitrary_types_allowed = True


class AgentState(BaseModel):
    """Agent state for LangGraph execution."""
    
    messages: List[BaseMessage] = Field(default_factory=list, description="Conversation messages")
    context: Optional[AgentContext] = Field(None, description="Agent execution context")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    current_step: str = Field(default="start", description="Current execution step")
    completed_steps: List[str] = Field(default_factory=list, description="Completed steps")
    error: Optional[str] = Field(None, description="Error message if any")
    
    class Config:
        arbitrary_types_allowed = True


class ApprovalRequest(BaseModel):
    """Human-in-the-loop approval request."""
    
    id: str = Field(default_factory=lambda: str(uuid4()))
    workflow_id: str = Field(..., description="Associated workflow ID")
    agent_id: str = Field(..., description="Requesting agent ID")
    request_type: str = Field(..., description="Type of approval needed")
    description: str = Field(..., description="Description of what needs approval")
    data: Dict[str, Any] = Field(default_factory=dict, description="Request data")
    required_approvers: List[str] = Field(default_factory=list, description="Required approver IDs")
    approvals: List[Dict[str, Any]] = Field(default_factory=list, description="Received approvals")
    status: str = Field(default="pending", description="Approval status")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = Field(None, description="Expiration time")
    
    @property
    def is_approved(self) -> bool:
        """Check if request is fully approved."""
        if not self.required_approvers:
            return True
        
        approved_by = {approval["approver_id"] for approval in self.approvals if approval.get("approved")}
        required_set = set(self.required_approvers)
        
        return required_set.issubset(approved_by)
    
    @property
    def is_expired(self) -> bool:
        """Check if request has expired."""
        if not self.expires_at:
            return False
        return datetime.utcnow() > self.expires_at


class WorkflowState(BaseModel):
    """Workflow execution state."""
    
    workflow_id: str = Field(default_factory=lambda: str(uuid4()))
    workflow_type: str = Field(..., description="Type of workflow (advisory/transactional)")
    current_step: str = Field(default="start", description="Current workflow step")
    steps_completed: List[str] = Field(default_factory=list, description="Completed steps")
    pending_approvals: List[ApprovalRequest] = Field(default_factory=list, description="Pending approvals")
    data: Dict[str, Any] = Field(default_factory=dict, description="Workflow data")
    context: Optional[AgentContext] = Field(None, description="Execution context")
    status: AgentStatus = Field(default=AgentStatus.IDLE, description="Workflow status")
    error: Optional[str] = Field(None, description="Error message if any")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    def add_approval_request(
        self,
        agent_id: str,
        request_type: str,
        description: str,
        data: Dict[str, Any],
        required_approvers: List[str],
        expires_in_minutes: Optional[int] = None,
    ) -> ApprovalRequest:
        """Add an approval request to the workflow."""
        expires_at = None
        if expires_in_minutes:
            from datetime import timedelta
            expires_at = datetime.utcnow() + timedelta(minutes=expires_in_minutes)
        
        approval_request = ApprovalRequest(
            workflow_id=self.workflow_id,
            agent_id=agent_id,
            request_type=request_type,
            description=description,
            data=data,
            required_approvers=required_approvers,
            expires_at=expires_at,
        )
        
        self.pending_approvals.append(approval_request)
        self.updated_at = datetime.utcnow()
        
        return approval_request
    
    def approve_request(
        self,
        request_id: str,
        approver_id: str,
        approved: bool,
        comments: Optional[str] = None,
    ) -> bool:
        """Approve or reject a pending request."""
        for request in self.pending_approvals:
            if request.id == request_id:
                approval = {
                    "approver_id": approver_id,
                    "approved": approved,
                    "comments": comments,
                    "timestamp": datetime.utcnow(),
                }
                request.approvals.append(approval)
                
                if approved and request.is_approved:
                    request.status = "approved"
                elif not approved:
                    request.status = "rejected"
                
                self.updated_at = datetime.utcnow()
                return True
        
        return False
    
    def get_pending_approvals(self) -> List[ApprovalRequest]:
        """Get all pending approval requests."""
        return [req for req in self.pending_approvals if req.status == "pending" and not req.is_expired]
    
    def complete_step(self, step_name: str) -> None:
        """Mark a step as completed."""
        if step_name not in self.steps_completed:
            self.steps_completed.append(step_name)
        self.updated_at = datetime.utcnow()
    
    def set_error(self, error_message: str) -> None:
        """Set workflow error state."""
        self.error = error_message
        self.status = AgentStatus.ERROR
        self.updated_at = datetime.utcnow()
    
    def set_status(self, status: AgentStatus) -> None:
        """Update workflow status."""
        self.status = status
        self.updated_at = datetime.utcnow()


class AgentCapability(BaseModel):
    """Agent capability definition."""
    
    name: str = Field(..., description="Capability name")
    description: str = Field(..., description="Capability description")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Capability parameters")
    required_permissions: List[str] = Field(default_factory=list, description="Required permissions")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "financial_analysis",
                "description": "Analyze financial data and generate insights",
                "parameters": {
                    "data_sources": ["transactions", "accounts", "forecasts"],
                    "analysis_types": ["trend", "variance", "ratio"]
                },
                "required_permissions": ["read_financial_data", "generate_reports"]
            }
        }


class AgentMetrics(BaseModel):
    """Agent performance metrics."""
    
    agent_id: str = Field(..., description="Agent identifier")
    requests_processed: int = Field(default=0, description="Total requests processed")
    average_response_time: float = Field(default=0.0, description="Average response time in seconds")
    success_rate: float = Field(default=0.0, description="Success rate percentage")
    error_count: int = Field(default=0, description="Total error count")
    last_activity: Optional[datetime] = Field(None, description="Last activity timestamp")
    
    def update_metrics(
        self,
        response_time: float,
        success: bool,
    ) -> None:
        """Update agent metrics with new request data."""
        self.requests_processed += 1
        
        # Update average response time
        if self.requests_processed == 1:
            self.average_response_time = response_time
        else:
            self.average_response_time = (
                (self.average_response_time * (self.requests_processed - 1) + response_time)
                / self.requests_processed
            )
        
        # Update success rate
        if not success:
            self.error_count += 1
        
        self.success_rate = (
            (self.requests_processed - self.error_count) / self.requests_processed * 100
        )
        
        self.last_activity = datetime.utcnow()