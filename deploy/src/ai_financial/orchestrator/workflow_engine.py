"""Workflow engine for managing complex multi-agent workflows."""

from typing import Any, Dict, List, Optional, Callable
from datetime import datetime, timedelta
from enum import Enum
import asyncio

from ai_financial.models.agent_models import WorkflowState, AgentStatus, ApprovalRequest
from ai_financial.core.logging import get_logger, get_tracer

logger = get_logger(__name__)
tracer = get_tracer(__name__)


class WorkflowStepType(str, Enum):
    """Workflow step types."""
    AGENT_TASK = "agent_task"
    APPROVAL = "approval"
    CONDITION = "condition"
    PARALLEL = "parallel"
    SEQUENTIAL = "sequential"


class WorkflowStep:
    """Individual workflow step definition."""
    
    def __init__(
        self,
        step_id: str,
        step_type: WorkflowStepType,
        name: str,
        description: str,
        agent_id: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None,
        conditions: Optional[Dict[str, Any]] = None,
        timeout_minutes: Optional[int] = None,
    ):
        """Initialize workflow step.
        
        Args:
            step_id: Unique step identifier
            step_type: Type of step
            name: Step name
            description: Step description
            agent_id: Agent to execute step (for agent tasks)
            parameters: Step parameters
            conditions: Execution conditions
            timeout_minutes: Step timeout in minutes
        """
        self.step_id = step_id
        self.step_type = step_type
        self.name = name
        self.description = description
        self.agent_id = agent_id
        self.parameters = parameters or {}
        self.conditions = conditions or {}
        self.timeout_minutes = timeout_minutes
        
        # Execution state
        self.status = AgentStatus.IDLE
        self.result: Optional[Dict[str, Any]] = None
        self.error: Optional[str] = None
        self.started_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None


class WorkflowDefinition:
    """Workflow definition with steps and flow control."""
    
    def __init__(
        self,
        workflow_id: str,
        name: str,
        description: str,
        workflow_type: str,
    ):
        """Initialize workflow definition.
        
        Args:
            workflow_id: Unique workflow identifier
            name: Workflow name
            description: Workflow description
            workflow_type: Type of workflow
        """
        self.workflow_id = workflow_id
        self.name = name
        self.description = description
        self.workflow_type = workflow_type
        
        self.steps: Dict[str, WorkflowStep] = {}
        self.step_order: List[str] = []
        self.dependencies: Dict[str, List[str]] = {}  # step_id -> list of prerequisite step_ids
        
    def add_step(self, step: WorkflowStep, dependencies: Optional[List[str]] = None) -> None:
        """Add a step to the workflow.
        
        Args:
            step: Workflow step to add
            dependencies: List of prerequisite step IDs
        """
        self.steps[step.step_id] = step
        self.step_order.append(step.step_id)
        
        if dependencies:
            self.dependencies[step.step_id] = dependencies
    
    def get_ready_steps(self, completed_steps: List[str]) -> List[WorkflowStep]:
        """Get steps that are ready to execute.
        
        Args:
            completed_steps: List of completed step IDs
            
        Returns:
            List of steps ready for execution
        """
        ready_steps = []
        
        for step_id in self.step_order:
            if step_id in completed_steps:
                continue
            
            # Check if all dependencies are completed
            dependencies = self.dependencies.get(step_id, [])
            if all(dep in completed_steps for dep in dependencies):
                ready_steps.append(self.steps[step_id])
        
        return ready_steps


class WorkflowEngine:
    """Engine for executing complex workflows."""
    
    def __init__(self):
        """Initialize workflow engine."""
        self.workflow_definitions: Dict[str, WorkflowDefinition] = {}
        self.active_executions: Dict[str, WorkflowState] = {}
        
        # Initialize built-in workflow definitions
        self._initialize_builtin_workflows()
        
        logger.info("Workflow Engine initialized")
    
    def _initialize_builtin_workflows(self) -> None:
        """Initialize built-in workflow definitions."""
        # Advisory workflow
        advisory_workflow = WorkflowDefinition(
            workflow_id="advisory_ceo_support",
            name="CEO Advisory Workflow",
            description="Complete advisory workflow for CEO decision support",
            workflow_type="advisory",
        )
        
        # Add advisory workflow steps
        advisory_workflow.add_step(WorkflowStep(
            step_id="data_sync",
            step_type=WorkflowStepType.AGENT_TASK,
            name="Data Synchronization",
            description="Sync latest financial data from all sources",
            agent_id="data_sync_agent",
            timeout_minutes=10,
        ))
        
        advisory_workflow.add_step(WorkflowStep(
            step_id="financial_analysis",
            step_type=WorkflowStepType.AGENT_TASK,
            name="Financial Analysis",
            description="Perform comprehensive financial analysis",
            agent_id="ai_cfo_agent",
            timeout_minutes=15,
        ), dependencies=["data_sync"])
        
        advisory_workflow.add_step(WorkflowStep(
            step_id="forecasting",
            step_type=WorkflowStepType.AGENT_TASK,
            name="Financial Forecasting",
            description="Generate financial forecasts and projections",
            agent_id="forecasting_agent",
            timeout_minutes=20,
        ), dependencies=["financial_analysis"])
        
        advisory_workflow.add_step(WorkflowStep(
            step_id="risk_assessment",
            step_type=WorkflowStepType.AGENT_TASK,
            name="Risk Assessment",
            description="Assess financial risks and opportunities",
            agent_id="alert_agent",
            timeout_minutes=10,
        ), dependencies=["financial_analysis"])
        
        advisory_workflow.add_step(WorkflowStep(
            step_id="executive_reporting",
            step_type=WorkflowStepType.AGENT_TASK,
            name="Executive Reporting",
            description="Generate executive summary and recommendations",
            agent_id="reporting_agent",
            timeout_minutes=15,
        ), dependencies=["forecasting", "risk_assessment"])
        
        self.workflow_definitions["advisory"] = advisory_workflow
        
        # Transactional workflow
        transactional_workflow = WorkflowDefinition(
            workflow_id="transactional_automation",
            name="Transactional Automation Workflow",
            description="Complete transactional processing workflow",
            workflow_type="transactional",
        )
        
        # Add transactional workflow steps
        transactional_workflow.add_step(WorkflowStep(
            step_id="document_processing",
            step_type=WorkflowStepType.AGENT_TASK,
            name="Document Processing",
            description="OCR and document data extraction",
            agent_id="ocr_agent",
            timeout_minutes=5,
        ))
        
        transactional_workflow.add_step(WorkflowStep(
            step_id="data_standardization",
            step_type=WorkflowStepType.AGENT_TASK,
            name="Data Standardization",
            description="Standardize and validate extracted data",
            agent_id="data_sync_agent",
            timeout_minutes=5,
        ), dependencies=["document_processing"])
        
        transactional_workflow.add_step(WorkflowStep(
            step_id="accounting_entries",
            step_type=WorkflowStepType.AGENT_TASK,
            name="Accounting Entries",
            description="Create automated accounting entries",
            agent_id="accounting_agent",
            timeout_minutes=10,
        ), dependencies=["data_standardization"])
        
        transactional_workflow.add_step(WorkflowStep(
            step_id="approval_check",
            step_type=WorkflowStepType.APPROVAL,
            name="Transaction Approval",
            description="Human approval for high-value transactions",
            timeout_minutes=60,
        ), dependencies=["accounting_entries"])
        
        transactional_workflow.add_step(WorkflowStep(
            step_id="reconciliation",
            step_type=WorkflowStepType.AGENT_TASK,
            name="Bank Reconciliation",
            description="Reconcile transactions with bank statements",
            agent_id="reconciliation_agent",
            timeout_minutes=15,
        ), dependencies=["approval_check"])
        
        transactional_workflow.add_step(WorkflowStep(
            step_id="compliance_audit",
            step_type=WorkflowStepType.AGENT_TASK,
            name="Compliance Audit",
            description="Validate compliance and create audit trail",
            agent_id="compliance_agent",
            timeout_minutes=10,
        ), dependencies=["reconciliation"])
        
        self.workflow_definitions["transactional"] = transactional_workflow
    
    async def execute_workflow(
        self,
        workflow_type: str,
        workflow_state: WorkflowState,
        agent_executor: Callable[[str, Any, Any], Any],
    ) -> Dict[str, Any]:
        """Execute a workflow.
        
        Args:
            workflow_type: Type of workflow to execute
            workflow_state: Workflow state
            agent_executor: Function to execute agent tasks
            
        Returns:
            Workflow execution result
        """
        with tracer.start_as_current_span("workflow_engine.execute_workflow") as span:
            span.set_attribute("workflow_type", workflow_type)
            span.set_attribute("workflow_id", workflow_state.workflow_id)
            
            if workflow_type not in self.workflow_definitions:
                return {
                    "success": False,
                    "error": f"Unknown workflow type: {workflow_type}",
                }
            
            workflow_def = self.workflow_definitions[workflow_type]
            self.active_executions[workflow_state.workflow_id] = workflow_state
            
            try:
                workflow_state.set_status(AgentStatus.PROCESSING)
                
                # Execute workflow steps
                while True:
                    # Get ready steps
                    ready_steps = workflow_def.get_ready_steps(workflow_state.steps_completed)
                    
                    if not ready_steps:
                        # No more steps to execute
                        break
                    
                    # Execute ready steps (can be parallel)
                    step_results = await self._execute_steps(
                        ready_steps,
                        workflow_state,
                        agent_executor,
                    )
                    
                    # Process step results
                    for step_id, result in step_results.items():
                        if result.get("success", False):
                            workflow_state.complete_step(step_id)
                        else:
                            # Handle step failure
                            error_msg = result.get("error", "Step execution failed")
                            workflow_state.set_error(f"Step {step_id} failed: {error_msg}")
                            
                            return {
                                "success": False,
                                "error": workflow_state.error,
                                "workflow_id": workflow_state.workflow_id,
                                "failed_step": step_id,
                            }
                
                # Workflow completed successfully
                workflow_state.set_status(AgentStatus.COMPLETED)
                
                return {
                    "success": True,
                    "workflow_id": workflow_state.workflow_id,
                    "workflow_type": workflow_type,
                    "completed_steps": workflow_state.steps_completed,
                    "execution_time": (
                        datetime.utcnow() - workflow_state.created_at
                    ).total_seconds(),
                }
                
            except Exception as e:
                logger.error(
                    "Workflow execution failed",
                    workflow_type=workflow_type,
                    workflow_id=workflow_state.workflow_id,
                    error=str(e),
                )
                
                workflow_state.set_error(f"Workflow execution failed: {str(e)}")
                
                return {
                    "success": False,
                    "error": workflow_state.error,
                    "workflow_id": workflow_state.workflow_id,
                }
            
            finally:
                # Clean up
                if workflow_state.workflow_id in self.active_executions:
                    del self.active_executions[workflow_state.workflow_id]
    
    async def _execute_steps(
        self,
        steps: List[WorkflowStep],
        workflow_state: WorkflowState,
        agent_executor: Callable[[str, Any, Any], Any],
    ) -> Dict[str, Dict[str, Any]]:
        """Execute workflow steps.
        
        Args:
            steps: Steps to execute
            workflow_state: Workflow state
            agent_executor: Agent execution function
            
        Returns:
            Step execution results
        """
        results = {}
        
        # Execute steps (can be parallel for independent steps)
        tasks = []
        
        for step in steps:
            if step.step_type == WorkflowStepType.AGENT_TASK:
                task = self._execute_agent_step(step, workflow_state, agent_executor)
                tasks.append((step.step_id, task))
            
            elif step.step_type == WorkflowStepType.APPROVAL:
                task = self._execute_approval_step(step, workflow_state)
                tasks.append((step.step_id, task))
        
        # Wait for all tasks to complete
        for step_id, task in tasks:
            try:
                result = await task
                results[step_id] = result
            except Exception as e:
                results[step_id] = {
                    "success": False,
                    "error": str(e),
                }
        
        return results
    
    async def _execute_agent_step(
        self,
        step: WorkflowStep,
        workflow_state: WorkflowState,
        agent_executor: Callable[[str, Any, Any], Any],
    ) -> Dict[str, Any]:
        """Execute an agent task step.
        
        Args:
            step: Workflow step
            workflow_state: Workflow state
            agent_executor: Agent execution function
            
        Returns:
            Step execution result
        """
        with tracer.start_as_current_span("workflow_engine.execute_agent_step") as span:
            span.set_attribute("step_id", step.step_id)
            span.set_attribute("agent_id", step.agent_id or "unknown")
            
            try:
                step.status = AgentStatus.PROCESSING
                step.started_at = datetime.utcnow()
                
                # Prepare step request
                request = {
                    "step_name": step.name,
                    "step_description": step.description,
                    "parameters": step.parameters,
                    "workflow_data": workflow_state.data,
                }
                
                # Execute agent
                result = await agent_executor(step.agent_id, request, workflow_state.context)
                
                step.status = AgentStatus.COMPLETED
                step.completed_at = datetime.utcnow()
                step.result = result
                
                logger.info(
                    "Agent step completed",
                    step_id=step.step_id,
                    agent_id=step.agent_id,
                    success=result.get("success", False),
                )
                
                return result
                
            except Exception as e:
                step.status = AgentStatus.ERROR
                step.error = str(e)
                step.completed_at = datetime.utcnow()
                
                logger.error(
                    "Agent step failed",
                    step_id=step.step_id,
                    agent_id=step.agent_id,
                    error=str(e),
                )
                
                return {
                    "success": False,
                    "error": str(e),
                }
    
    async def _execute_approval_step(
        self,
        step: WorkflowStep,
        workflow_state: WorkflowState,
    ) -> Dict[str, Any]:
        """Execute an approval step.
        
        Args:
            step: Workflow step
            workflow_state: Workflow state
            
        Returns:
            Step execution result
        """
        with tracer.start_as_current_span("workflow_engine.execute_approval_step"):
            try:
                step.status = AgentStatus.WAITING
                step.started_at = datetime.utcnow()
                
                # Create approval request
                approval_request = workflow_state.add_approval_request(
                    agent_id="workflow_engine",
                    request_type="workflow_approval",
                    description=step.description,
                    data=step.parameters,
                    required_approvers=["financial_manager"],  # This would be configurable
                    expires_in_minutes=step.timeout_minutes,
                )
                
                # Wait for approval (in a real implementation, this would be event-driven)
                timeout = datetime.utcnow() + timedelta(minutes=step.timeout_minutes or 60)
                
                while datetime.utcnow() < timeout:
                    if approval_request.is_approved:
                        step.status = AgentStatus.COMPLETED
                        step.completed_at = datetime.utcnow()
                        
                        return {
                            "success": True,
                            "approved": True,
                            "approval_id": approval_request.id,
                        }
                    
                    elif approval_request.status == "rejected":
                        step.status = AgentStatus.ERROR
                        step.error = "Approval rejected"
                        step.completed_at = datetime.utcnow()
                        
                        return {
                            "success": False,
                            "error": "Approval rejected",
                            "approval_id": approval_request.id,
                        }
                    
                    # Wait before checking again
                    await asyncio.sleep(1)
                
                # Timeout reached
                step.status = AgentStatus.ERROR
                step.error = "Approval timeout"
                step.completed_at = datetime.utcnow()
                
                return {
                    "success": False,
                    "error": "Approval timeout",
                    "approval_id": approval_request.id,
                }
                
            except Exception as e:
                step.status = AgentStatus.ERROR
                step.error = str(e)
                step.completed_at = datetime.utcnow()
                
                return {
                    "success": False,
                    "error": str(e),
                }
    
    def get_workflow_definition(self, workflow_type: str) -> Optional[WorkflowDefinition]:
        """Get workflow definition by type.
        
        Args:
            workflow_type: Workflow type
            
        Returns:
            Workflow definition if found
        """
        return self.workflow_definitions.get(workflow_type)
    
    def list_workflow_types(self) -> List[str]:
        """List available workflow types.
        
        Returns:
            List of workflow type names
        """
        return list(self.workflow_definitions.keys())
    
    def get_active_executions(self) -> Dict[str, WorkflowState]:
        """Get all active workflow executions.
        
        Returns:
            Dictionary of active executions
        """
        return self.active_executions.copy()