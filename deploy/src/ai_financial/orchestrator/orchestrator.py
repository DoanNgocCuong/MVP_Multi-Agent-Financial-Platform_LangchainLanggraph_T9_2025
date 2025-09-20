"""Central Agent Orchestrator for coordinating multi-agent workflows."""

import asyncio
from typing import Any, Dict, List, Optional, Type, Union
from datetime import datetime
from uuid import uuid4

from ai_financial.core.base_agent import BaseAgent
from ai_financial.core.config import settings
from ai_financial.core.logging import get_logger, get_tracer
from ai_financial.models.agent_models import AgentContext, AgentState, WorkflowState, AgentStatus
from ai_financial.mcp.hub import get_tool_hub
from ai_financial.orchestrator.workflow_engine import WorkflowEngine
from ai_financial.orchestrator.context_manager import ContextManager

logger = get_logger(__name__)
tracer = get_tracer(__name__)


class AgentOrchestrator:
    """Central orchestrator for managing and coordinating AI agents."""
    
    def __init__(self):
        """Initialize the Agent Orchestrator."""
        self.agents: Dict[str, BaseAgent] = {}
        self.active_workflows: Dict[str, WorkflowState] = {}
        
        # Core components
        self.workflow_engine = WorkflowEngine()
        self.context_manager = ContextManager()
        self.tool_hub = get_tool_hub()
        
        # Orchestrator state
        self._running = False
        self._max_concurrent_agents = settings.workflow.max_concurrent_agents
        self._active_agent_count = 0
        
        logger.info(
            "Agent Orchestrator initialized",
            max_concurrent_agents=self._max_concurrent_agents,
        )
    
    def register_agent(self, agent: BaseAgent) -> None:
        """Register an agent with the orchestrator.
        
        Args:
            agent: Agent instance to register
        """
        with tracer.start_as_current_span("orchestrator.register_agent"):
            agent_id = agent.agent_id
            
            if agent_id in self.agents:
                logger.warning(
                    "Agent already registered, overwriting",
                    agent_id=agent_id,
                )
            
            self.agents[agent_id] = agent
            
            logger.info(
                "Agent registered",
                agent_id=agent_id,
                agent_name=agent.name,
                capabilities=len(agent.get_capabilities()),
            )
    
    def unregister_agent(self, agent_id: str) -> bool:
        """Unregister an agent from the orchestrator.
        
        Args:
            agent_id: Agent ID to unregister
            
        Returns:
            True if agent was unregistered, False if not found
        """
        if agent_id not in self.agents:
            return False
        
        agent = self.agents[agent_id]
        del self.agents[agent_id]
        
        logger.info(
            "Agent unregistered",
            agent_id=agent_id,
            agent_name=agent.name,
        )
        
        return True
    
    async def _resolve_result(self, result: Any) -> Dict[str, Any]:
        """Ensure an awaited, dictionary-like result for downstream usage."""
        # Await if coroutine
        if asyncio.iscoroutine(result):
            result = await result
        # Normalize non-dict results
        if not isinstance(result, dict):
            return {"success": True, "result": result}
        return result

    async def route_request(
        self,
        request: Union[str, Dict[str, Any]],
        context: Optional[AgentContext] = None,
        preferred_agent: Optional[str] = None,
        workflow_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Route a request to the appropriate agent or workflow.
        
        Args:
            request: The request to process
            context: Execution context
            preferred_agent: Preferred agent ID (optional)
            workflow_type: Workflow type (advisory/transactional)
            
        Returns:
            Processing result
        """
        with tracer.start_as_current_span("orchestrator.route_request") as span:
            # Create context if not provided
            if context is None:
                context = AgentContext(
                    agent_id="orchestrator",
                    session_id=str(uuid4()),
                    user_id="system",
                    company_id="default",
                    permissions=[],
                    state={},
                    trace_id=span.get_span_context().trace_id,
                )
            
            try:
                # Determine routing strategy
                if preferred_agent and preferred_agent in self.agents:
                    # Direct agent routing
                    return await self._route_to_agent(preferred_agent, request, context)
                
                elif workflow_type:
                    # Workflow-based routing
                    return await self._route_to_workflow(workflow_type, request, context)
                
                else:
                    # Intelligent routing based on request analysis
                    return await self._intelligent_routing(request, context)
                
            except Exception as e:
                logger.error(
                    "Request routing failed",
                    error=str(e),
                    session_id=context.session_id,
                )
                
                return {
                    "success": False,
                    "error": f"Routing failed: {str(e)}",
                    "session_id": context.session_id,
                }
    
    async def _route_to_agent(
        self,
        agent_id: str,
        request: Union[str, Dict[str, Any]],
        context: AgentContext,
    ) -> Dict[str, Any]:
        """Route request directly to a specific agent.
        
        Args:
            agent_id: Target agent ID
            request: Request to process
            context: Execution context
            
        Returns:
            Agent response
        """
        with tracer.start_as_current_span("orchestrator.route_to_agent") as span:
            span.set_attribute("agent_id", agent_id)
            
            if agent_id not in self.agents:
                return {
                    "success": False,
                    "error": f"Agent '{agent_id}' not found",
                    "session_id": context.session_id,
                }
            
            # Check concurrency limits
            if self._active_agent_count >= self._max_concurrent_agents:
                return {
                    "success": False,
                    "error": "Maximum concurrent agents reached",
                    "session_id": context.session_id,
                }
            
            agent = self.agents[agent_id]
            
            try:
                self._active_agent_count += 1
                
                # Execute agent
                result = await agent.invoke(request, context)
                # Only resolve if result is not already a dict
                if isinstance(result, dict):
                    normalized = result
                else:
                    normalized = await self._resolve_result(result)
                
                logger.info(
                    "Agent request completed",
                    agent_id=agent_id,
                    session_id=context.session_id,
                    success=(normalized.get("error") is None),
                )
                
                return normalized
                
            except Exception as e:
                logger.error(
                    "Agent execution failed",
                    agent_id=agent_id,
                    session_id=context.session_id,
                    error=str(e),
                )
                
                return {
                    "success": False,
                    "error": f"Agent execution failed: {str(e)}",
                    "session_id": context.session_id,
                }
                
            finally:
                self._active_agent_count -= 1
    
    async def _route_to_workflow(
        self,
        workflow_type: str,
        request: Union[str, Dict[str, Any]],
        context: AgentContext,
    ) -> Dict[str, Any]:
        """Route request to a workflow.
        
        Args:
            workflow_type: Type of workflow (advisory/transactional)
            request: Request to process
            context: Execution context
            
        Returns:
            Workflow response
        """
        with tracer.start_as_current_span("orchestrator.route_to_workflow") as span:
            span.set_attribute("workflow_type", workflow_type)
            
            try:
                # Create workflow state
                workflow_state = WorkflowState(
                    workflow_type=workflow_type,
                    context=context,
                    data={"request": request},
                    status=AgentStatus.PROCESSING,
                )
                
                # Store workflow
                self.active_workflows[workflow_state.workflow_id] = workflow_state
                
                # Execute workflow
                if workflow_type == "advisory":
                    result = await self._execute_advisory_workflow(workflow_state)
                elif workflow_type == "transactional":
                    result = await self._execute_transactional_workflow(workflow_state)
                else:
                    result = {
                        "success": False,
                        "error": f"Unknown workflow type: {workflow_type}",
                    }
                
                # Update workflow status
                if result.get("success", False):
                    workflow_state.set_status(AgentStatus.COMPLETED)
                else:
                    workflow_state.set_error(result.get("error", "Unknown error"))
                
                return result
                
            except Exception as e:
                logger.error(
                    "Workflow execution failed",
                    workflow_type=workflow_type,
                    error=str(e),
                )
                
                return {
                    "success": False,
                    "error": f"Workflow execution failed: {str(e)}",
                    "session_id": context.session_id,
                }
    
    async def _intelligent_routing(
        self,
        request: Union[str, Dict[str, Any]],
        context: AgentContext,
    ) -> Dict[str, Any]:
        """Intelligently route request based on content analysis.
        
        Args:
            request: Request to analyze and route
            context: Execution context
            
        Returns:
            Routing result
        """
        with tracer.start_as_current_span("orchestrator.intelligent_routing"):
            try:
                # Analyze request to determine best routing
                request_str = str(request) if not isinstance(request, str) else request
                request_lower = request_str.lower()
                
                # Simple keyword-based routing (in production, use ML-based classification)
                if any(keyword in request_lower for keyword in [
                    "forecast", "predict", "projection", "trend", "future"
                ]):
                    return await self._route_to_agent("forecasting_agent", request, context)
                
                elif any(keyword in request_lower for keyword in [
                    "alert", "warning", "risk", "threshold", "monitor"
                ]):
                    return await self._route_to_agent("alert_agent", request, context)
                
                elif any(keyword in request_lower for keyword in [
                    "report", "summary", "brief", "dashboard", "analysis"
                ]):
                    return await self._route_to_agent("reporting_agent", request, context)
                
                elif any(keyword in request_lower for keyword in [
                    "ocr", "scan", "receipt", "invoice", "document"
                ]):
                    return await self._route_to_agent("ocr_agent", request, context)
                
                elif any(keyword in request_lower for keyword in [
                    "sync", "integration", "import", "export", "data"
                ]):
                    return await self._route_to_agent("data_sync_agent", request, context)
                
                elif any(keyword in request_lower for keyword in [
                    "reconcile", "match", "balance", "statement"
                ]):
                    return await self._route_to_agent("reconciliation_agent", request, context)
                
                else:
                    # Default to AI CFO for general financial queries
                    return await self._route_to_agent("ai_cfo_agent", request, context)
                
            except Exception as e:
                logger.error(
                    "Intelligent routing failed",
                    error=str(e),
                )
                
                # Fallback to AI CFO agent
                return await self._route_to_agent("ai_cfo_agent", request, context)
    
    async def _execute_advisory_workflow(self, workflow_state: WorkflowState) -> Dict[str, Any]:
        """Execute advisory workflow (CEO support).
        
        Args:
            workflow_state: Workflow state
            
        Returns:
            Workflow result
        """
        with tracer.start_as_current_span("orchestrator.advisory_workflow"):
            try:
                request = workflow_state.data.get("request")
                context = workflow_state.context
                
                # Advisory workflow: Data sync → Analysis → Forecasting → Alerting → Reporting
                results = {}
                
                # Step 1: Data synchronization (if needed)
                if "data_sync_agent" in self.agents:
                    sync_result = await self.agents["data_sync_agent"].invoke(
                        "Sync latest financial data for analysis", context
                    )
                    results["data_sync"] = sync_result
                    workflow_state.complete_step("data_sync")
                
                # Step 2: Financial analysis
                if "ai_cfo_agent" in self.agents:
                    analysis_result = await self.agents["ai_cfo_agent"].invoke(request, context)
                    results["analysis"] = analysis_result
                    workflow_state.complete_step("analysis")
                
                # Step 3: Forecasting
                if "forecasting_agent" in self.agents:
                    forecast_result = await self.agents["forecasting_agent"].invoke(
                        "Generate financial forecasts based on current data", context
                    )
                    results["forecasting"] = forecast_result
                    workflow_state.complete_step("forecasting")
                
                # Step 4: Risk and opportunity alerts
                if "alert_agent" in self.agents:
                    alert_result = await self.agents["alert_agent"].invoke(
                        "Check for financial risks and opportunities", context
                    )
                    results["alerts"] = alert_result
                    workflow_state.complete_step("alerts")
                
                # Step 5: Executive reporting
                if "reporting_agent" in self.agents:
                    report_result = await self.agents["reporting_agent"].invoke(
                        "Generate executive financial report", context
                    )
                    results["report"] = report_result
                    workflow_state.complete_step("reporting")
                
                return {
                    "success": True,
                    "workflow_type": "advisory",
                    "workflow_id": workflow_state.workflow_id,
                    "results": results,
                    "completed_steps": workflow_state.steps_completed,
                }
                
            except Exception as e:
                logger.error(
                    "Advisory workflow failed",
                    workflow_id=workflow_state.workflow_id,
                    error=str(e),
                )
                
                return {
                    "success": False,
                    "error": f"Advisory workflow failed: {str(e)}",
                    "workflow_id": workflow_state.workflow_id,
                }
    
    async def _execute_transactional_workflow(self, workflow_state: WorkflowState) -> Dict[str, Any]:
        """Execute transactional workflow (automation).
        
        Args:
            workflow_state: Workflow state
            
        Returns:
            Workflow result
        """
        with tracer.start_as_current_span("orchestrator.transactional_workflow"):
            try:
                request = workflow_state.data.get("request")
                context = workflow_state.context
                
                # Transactional workflow: OCR/Ingest → Standardization → Accounting → Reconciliation → Audit
                results = {}
                
                # Step 1: OCR/Document processing
                if "ocr_agent" in self.agents:
                    ocr_result = await self.agents["ocr_agent"].invoke(request, context)
                    results["ocr_processing"] = ocr_result
                    workflow_state.complete_step("ocr_processing")
                
                # Step 2: Data standardization
                if "data_sync_agent" in self.agents:
                    standardization_result = await self.agents["data_sync_agent"].invoke(
                        "Standardize and validate processed data", context
                    )
                    results["standardization"] = standardization_result
                    workflow_state.complete_step("standardization")
                
                # Step 3: Accounting automation
                if "accounting_agent" in self.agents:
                    accounting_result = await self.agents["accounting_agent"].invoke(
                        "Create accounting entries from processed data", context
                    )
                    results["accounting"] = accounting_result
                    workflow_state.complete_step("accounting")
                
                # Step 4: Reconciliation
                if "reconciliation_agent" in self.agents:
                    reconciliation_result = await self.agents["reconciliation_agent"].invoke(
                        "Reconcile transactions with bank statements", context
                    )
                    results["reconciliation"] = reconciliation_result
                    workflow_state.complete_step("reconciliation")
                
                # Step 5: Compliance and audit
                if "compliance_agent" in self.agents:
                    compliance_result = await self.agents["compliance_agent"].invoke(
                        "Validate compliance and create audit trail", context
                    )
                    results["compliance"] = compliance_result
                    workflow_state.complete_step("compliance")
                
                return {
                    "success": True,
                    "workflow_type": "transactional",
                    "workflow_id": workflow_state.workflow_id,
                    "results": results,
                    "completed_steps": workflow_state.steps_completed,
                }
                
            except Exception as e:
                logger.error(
                    "Transactional workflow failed",
                    workflow_id=workflow_state.workflow_id,
                    error=str(e),
                )
                
                return {
                    "success": False,
                    "error": f"Transactional workflow failed: {str(e)}",
                    "workflow_id": workflow_state.workflow_id,
                }
    
    async def stream_workflow(
        self,
        workflow_type: str,
        request: Union[str, Dict[str, Any]],
        context: Optional[AgentContext] = None,
    ):
        """Stream workflow execution for real-time updates.
        
        Args:
            workflow_type: Type of workflow
            request: Request to process
            context: Execution context
            
        Yields:
            Streaming workflow updates
        """
        with tracer.start_as_current_span("orchestrator.stream_workflow"):
            # Create context if not provided
            if context is None:
                context = AgentContext(
                    agent_id="orchestrator",
                    session_id=str(uuid4()),
                    user_id="system",
                    company_id="default",
                    permissions=[],
                    state={},
                )
            
            try:
                # Create workflow state
                workflow_state = WorkflowState(
                    workflow_type=workflow_type,
                    context=context,
                    data={"request": request},
                    status=AgentStatus.PROCESSING,
                )
                
                # Store workflow
                self.active_workflows[workflow_state.workflow_id] = workflow_state
                
                # Yield initial status
                yield {
                    "type": "workflow_started",
                    "workflow_id": workflow_state.workflow_id,
                    "workflow_type": workflow_type,
                    "timestamp": datetime.utcnow().isoformat(),
                }
                
                # Execute workflow with streaming
                if workflow_type == "advisory":
                    async for update in self._stream_advisory_workflow(workflow_state):
                        yield update
                elif workflow_type == "transactional":
                    async for update in self._stream_transactional_workflow(workflow_state):
                        yield update
                else:
                    yield {
                        "type": "error",
                        "error": f"Unknown workflow type: {workflow_type}",
                        "timestamp": datetime.utcnow().isoformat(),
                    }
                
                # Yield completion status
                yield {
                    "type": "workflow_completed",
                    "workflow_id": workflow_state.workflow_id,
                    "status": workflow_state.status.value,
                    "completed_steps": workflow_state.steps_completed,
                    "timestamp": datetime.utcnow().isoformat(),
                }
                
            except Exception as e:
                logger.error(
                    "Workflow streaming failed",
                    workflow_type=workflow_type,
                    error=str(e),
                )
                
                yield {
                    "type": "error",
                    "error": f"Workflow streaming failed: {str(e)}",
                    "timestamp": datetime.utcnow().isoformat(),
                }
    
    async def _stream_advisory_workflow(self, workflow_state: WorkflowState):
        """Stream advisory workflow execution."""
        # This would implement streaming for each step of the advisory workflow
        # For brevity, showing a simplified version
        
        steps = ["data_sync", "analysis", "forecasting", "alerts", "reporting"]
        
        for step in steps:
            yield {
                "type": "step_started",
                "step": step,
                "workflow_id": workflow_state.workflow_id,
                "timestamp": datetime.utcnow().isoformat(),
            }
            
            # Simulate step execution
            await asyncio.sleep(0.1)
            
            workflow_state.complete_step(step)
            
            yield {
                "type": "step_completed",
                "step": step,
                "workflow_id": workflow_state.workflow_id,
                "timestamp": datetime.utcnow().isoformat(),
            }
    
    async def _stream_transactional_workflow(self, workflow_state: WorkflowState):
        """Stream transactional workflow execution."""
        # This would implement streaming for each step of the transactional workflow
        # For brevity, showing a simplified version
        
        steps = ["ocr_processing", "standardization", "accounting", "reconciliation", "compliance"]
        
        for step in steps:
            yield {
                "type": "step_started",
                "step": step,
                "workflow_id": workflow_state.workflow_id,
                "timestamp": datetime.utcnow().isoformat(),
            }
            
            # Simulate step execution
            await asyncio.sleep(0.1)
            
            workflow_state.complete_step(step)
            
            yield {
                "type": "step_completed",
                "step": step,
                "workflow_id": workflow_state.workflow_id,
                "timestamp": datetime.utcnow().isoformat(),
            }
    
    def get_orchestrator_status(self) -> Dict[str, Any]:
        """Get orchestrator status.
        
        Returns:
            Status information
        """
        return {
            "running": self._running,
            "registered_agents": len(self.agents),
            "active_workflows": len(self.active_workflows),
            "active_agent_count": self._active_agent_count,
            "max_concurrent_agents": self._max_concurrent_agents,
            "agent_list": list(self.agents.keys()),
            "workflow_types": ["advisory", "transactional"],
        }
    
    def get_workflow_status(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific workflow.
        
        Args:
            workflow_id: Workflow identifier
            
        Returns:
            Workflow status if found
        """
        if workflow_id not in self.active_workflows:
            return None
        
        workflow = self.active_workflows[workflow_id]
        
        return {
            "workflow_id": workflow_id,
            "workflow_type": workflow.workflow_type,
            "status": workflow.status.value,
            "current_step": workflow.current_step,
            "completed_steps": workflow.steps_completed,
            "pending_approvals": len(workflow.get_pending_approvals()),
            "created_at": workflow.created_at.isoformat(),
            "updated_at": workflow.updated_at.isoformat(),
        }
    
    async def start(self) -> None:
        """Start the orchestrator."""
        if self._running:
            logger.warning("Orchestrator already running")
            return
        
        self._running = True
        
        # Start tool hub
        await self.tool_hub.start_all_servers()
        
        logger.info(
            "Agent Orchestrator started",
            registered_agents=len(self.agents),
        )
    
    async def stop(self) -> None:
        """Stop the orchestrator."""
        if not self._running:
            return
        
        self._running = False
        
        # Stop tool hub
        await self.tool_hub.stop_all_servers()
        
        # Clear active workflows
        self.active_workflows.clear()
        
        logger.info("Agent Orchestrator stopped")


# Global orchestrator instance
orchestrator = AgentOrchestrator()


def get_orchestrator() -> AgentOrchestrator:
    """Get the global orchestrator instance.
    
    Returns:
        Orchestrator instance
    """
    return orchestrator