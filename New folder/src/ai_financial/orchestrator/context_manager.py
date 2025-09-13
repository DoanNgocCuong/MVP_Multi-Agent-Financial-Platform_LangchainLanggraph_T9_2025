"""Context manager for handling agent execution contexts and state."""

from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
import asyncio
from uuid import uuid4

from ai_financial.models.agent_models import AgentContext, AgentState, WorkflowState
from ai_financial.core.config import settings
from ai_financial.core.logging import get_logger, get_tracer

logger = get_logger(__name__)
tracer = get_tracer(__name__)


class ContextManager:
    """Manager for agent execution contexts and shared state."""
    
    def __init__(self):
        """Initialize context manager."""
        self.active_contexts: Dict[str, AgentContext] = {}
        self.shared_state: Dict[str, Dict[str, Any]] = {}  # company_id -> shared data
        self.context_locks: Dict[str, asyncio.Lock] = {}
        
        # Context cleanup settings
        self.context_ttl_minutes = 60  # Context time-to-live
        self.cleanup_interval_minutes = 10
        
        # Start cleanup task
        self._cleanup_task: Optional[asyncio.Task] = None
        
        logger.info("Context Manager initialized")
    
    async def create_context(
        self,
        agent_id: str,
        user_id: str,
        company_id: str,
        permissions: Optional[List[str]] = None,
        initial_state: Optional[Dict[str, Any]] = None,
        trace_id: Optional[int] = None,
    ) -> AgentContext:
        """Create a new agent execution context.
        
        Args:
            agent_id: Agent identifier
            user_id: User identifier
            company_id: Company identifier
            permissions: User permissions
            initial_state: Initial context state
            trace_id: OpenTelemetry trace ID
            
        Returns:
            New agent context
        """
        with tracer.start_as_current_span("context_manager.create_context"):
            session_id = str(uuid4())
            
            context = AgentContext(
                agent_id=agent_id,
                session_id=session_id,
                user_id=user_id,
                company_id=company_id,
                permissions=permissions or [],
                state=initial_state or {},
                trace_id=trace_id,
            )
            
            # Store context
            self.active_contexts[session_id] = context
            
            # Initialize company shared state if needed
            if company_id not in self.shared_state:
                self.shared_state[company_id] = {}
            
            # Create lock for this context
            self.context_locks[session_id] = asyncio.Lock()
            
            logger.info(
                "Context created",
                session_id=session_id,
                agent_id=agent_id,
                user_id=user_id,
                company_id=company_id,
            )
            
            return context
    
    async def get_context(self, session_id: str) -> Optional[AgentContext]:
        """Get an existing context by session ID.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Agent context if found
        """
        return self.active_contexts.get(session_id)
    
    async def update_context_state(
        self,
        session_id: str,
        state_updates: Dict[str, Any],
        merge: bool = True,
    ) -> bool:
        """Update context state.
        
        Args:
            session_id: Session identifier
            state_updates: State updates to apply
            merge: Whether to merge with existing state or replace
            
        Returns:
            True if context was updated
        """
        with tracer.start_as_current_span("context_manager.update_context_state"):
            if session_id not in self.active_contexts:
                return False
            
            # Use lock to ensure thread safety
            async with self.context_locks.get(session_id, asyncio.Lock()):
                context = self.active_contexts[session_id]
                
                if merge:
                    context.state.update(state_updates)
                else:
                    context.state = state_updates.copy()
                
                logger.debug(
                    "Context state updated",
                    session_id=session_id,
                    updates_count=len(state_updates),
                )
                
                return True
    
    async def get_shared_state(
        self,
        company_id: str,
        key: Optional[str] = None,
    ) -> Any:
        """Get shared state for a company.
        
        Args:
            company_id: Company identifier
            key: Specific key to retrieve (optional)
            
        Returns:
            Shared state data
        """
        if company_id not in self.shared_state:
            return None if key else {}
        
        company_state = self.shared_state[company_id]
        
        if key:
            return company_state.get(key)
        else:
            return company_state.copy()
    
    async def update_shared_state(
        self,
        company_id: str,
        key: str,
        value: Any,
    ) -> None:
        """Update shared state for a company.
        
        Args:
            company_id: Company identifier
            key: State key
            value: State value
        """
        with tracer.start_as_current_span("context_manager.update_shared_state"):
            if company_id not in self.shared_state:
                self.shared_state[company_id] = {}
            
            self.shared_state[company_id][key] = value
            
            logger.debug(
                "Shared state updated",
                company_id=company_id,
                key=key,
            )
    
    async def share_context_data(
        self,
        source_session_id: str,
        target_session_id: str,
        keys: Optional[List[str]] = None,
    ) -> bool:
        """Share data between contexts.
        
        Args:
            source_session_id: Source context session ID
            target_session_id: Target context session ID
            keys: Specific keys to share (optional, shares all if None)
            
        Returns:
            True if data was shared successfully
        """
        with tracer.start_as_current_span("context_manager.share_context_data"):
            source_context = self.active_contexts.get(source_session_id)
            target_context = self.active_contexts.get(target_session_id)
            
            if not source_context or not target_context:
                return False
            
            # Use locks to ensure thread safety
            source_lock = self.context_locks.get(source_session_id, asyncio.Lock())
            target_lock = self.context_locks.get(target_session_id, asyncio.Lock())
            
            async with source_lock:
                async with target_lock:
                    if keys:
                        # Share specific keys
                        for key in keys:
                            if key in source_context.state:
                                target_context.state[key] = source_context.state[key]
                    else:
                        # Share all state
                        target_context.state.update(source_context.state)
            
            logger.info(
                "Context data shared",
                source_session_id=source_session_id,
                target_session_id=target_session_id,
                keys_shared=keys or "all",
            )
            
            return True
    
    async def create_workflow_context(
        self,
        workflow_state: WorkflowState,
        base_context: Optional[AgentContext] = None,
    ) -> AgentContext:
        """Create a context for workflow execution.
        
        Args:
            workflow_state: Workflow state
            base_context: Base context to inherit from
            
        Returns:
            Workflow execution context
        """
        with tracer.start_as_current_span("context_manager.create_workflow_context"):
            if base_context:
                # Inherit from base context
                context = AgentContext(
                    agent_id="workflow_orchestrator",
                    session_id=str(uuid4()),
                    user_id=base_context.user_id,
                    company_id=base_context.company_id,
                    permissions=base_context.permissions.copy(),
                    state=base_context.state.copy(),
                    trace_id=base_context.trace_id,
                )
            else:
                # Create new context
                context = AgentContext(
                    agent_id="workflow_orchestrator",
                    session_id=str(uuid4()),
                    user_id=workflow_state.context.user_id if workflow_state.context else "system",
                    company_id=workflow_state.context.company_id if workflow_state.context else "default",
                    permissions=[],
                    state={},
                )
            
            # Add workflow-specific state
            context.state.update({
                "workflow_id": workflow_state.workflow_id,
                "workflow_type": workflow_state.workflow_type,
                "workflow_data": workflow_state.data,
            })
            
            # Store context
            self.active_contexts[context.session_id] = context
            self.context_locks[context.session_id] = asyncio.Lock()
            
            logger.info(
                "Workflow context created",
                workflow_id=workflow_state.workflow_id,
                session_id=context.session_id,
            )
            
            return context
    
    async def cleanup_context(self, session_id: str) -> bool:
        """Clean up a specific context.
        
        Args:
            session_id: Session identifier
            
        Returns:
            True if context was cleaned up
        """
        if session_id not in self.active_contexts:
            return False
        
        # Remove context and lock
        del self.active_contexts[session_id]
        
        if session_id in self.context_locks:
            del self.context_locks[session_id]
        
        logger.info(
            "Context cleaned up",
            session_id=session_id,
        )
        
        return True
    
    async def cleanup_expired_contexts(self) -> int:
        """Clean up expired contexts.
        
        Returns:
            Number of contexts cleaned up
        """
        with tracer.start_as_current_span("context_manager.cleanup_expired_contexts"):
            current_time = datetime.utcnow()
            expired_sessions = []
            
            for session_id, context in self.active_contexts.items():
                # Check if context has expired
                age = current_time - context.created_at
                if age > timedelta(minutes=self.context_ttl_minutes):
                    expired_sessions.append(session_id)
            
            # Clean up expired contexts
            cleanup_count = 0
            for session_id in expired_sessions:
                if await self.cleanup_context(session_id):
                    cleanup_count += 1
            
            if cleanup_count > 0:
                logger.info(
                    "Expired contexts cleaned up",
                    cleanup_count=cleanup_count,
                )
            
            return cleanup_count
    
    async def get_context_statistics(self) -> Dict[str, Any]:
        """Get context manager statistics.
        
        Returns:
            Statistics dictionary
        """
        current_time = datetime.utcnow()
        
        # Calculate context age statistics
        context_ages = []
        company_counts = {}
        agent_counts = {}
        
        for context in self.active_contexts.values():
            age_minutes = (current_time - context.created_at).total_seconds() / 60
            context_ages.append(age_minutes)
            
            # Count by company
            company_counts[context.company_id] = company_counts.get(context.company_id, 0) + 1
            
            # Count by agent
            agent_counts[context.agent_id] = agent_counts.get(context.agent_id, 0) + 1
        
        return {
            "active_contexts": len(self.active_contexts),
            "shared_state_companies": len(self.shared_state),
            "average_context_age_minutes": sum(context_ages) / len(context_ages) if context_ages else 0,
            "oldest_context_age_minutes": max(context_ages) if context_ages else 0,
            "contexts_by_company": company_counts,
            "contexts_by_agent": agent_counts,
            "context_ttl_minutes": self.context_ttl_minutes,
        }
    
    async def start_cleanup_task(self) -> None:
        """Start the periodic cleanup task."""
        if self._cleanup_task and not self._cleanup_task.done():
            return
        
        self._cleanup_task = asyncio.create_task(self._periodic_cleanup())
        logger.info("Context cleanup task started")
    
    async def stop_cleanup_task(self) -> None:
        """Stop the periodic cleanup task."""
        if self._cleanup_task and not self._cleanup_task.done():
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass
        
        logger.info("Context cleanup task stopped")
    
    async def _periodic_cleanup(self) -> None:
        """Periodic cleanup task."""
        while True:
            try:
                await asyncio.sleep(self.cleanup_interval_minutes * 60)
                await self.cleanup_expired_contexts()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(
                    "Context cleanup task error",
                    error=str(e),
                )
    
    async def clear_all_contexts(self) -> int:
        """Clear all active contexts (for testing/shutdown).
        
        Returns:
            Number of contexts cleared
        """
        count = len(self.active_contexts)
        
        self.active_contexts.clear()
        self.context_locks.clear()
        self.shared_state.clear()
        
        logger.info(
            "All contexts cleared",
            cleared_count=count,
        )
        
        return count