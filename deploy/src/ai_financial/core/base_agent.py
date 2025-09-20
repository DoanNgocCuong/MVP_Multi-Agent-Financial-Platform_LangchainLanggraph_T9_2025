"""Base agent class with LangChain/LangGraph integration."""

import asyncio
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Type, TypeVar, Union
from uuid import uuid4

from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field

from ai_financial.core.config import settings
from ai_financial.core.logging import get_logger, get_tracer
from ai_financial.models.agent_models import AgentContext, AgentState, WorkflowState

T = TypeVar('T', bound=BaseModel)

logger = get_logger(__name__)
tracer = get_tracer(__name__)


class BaseAgent(ABC):
    """Base class for all AI agents in the financial system."""
    
    def __init__(
        self,
        agent_id: str,
        name: str,
        description: str,
        llm_model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ):
        """Initialize the base agent.
        
        Args:
            agent_id: Unique identifier for the agent
            name: Human-readable name for the agent
            description: Description of the agent's purpose
            llm_model: LLM model to use (defaults to config)
            temperature: LLM temperature (defaults to config)
            max_tokens: Maximum tokens for LLM (defaults to config)
        """
        self.agent_id = agent_id
        self.name = name
        self.description = description
        
        # Initialize LLM (lazy import to avoid heavy deps during startup)
        if settings.llm.has_openai_key:
            try:
                from langchain_openai import ChatOpenAI  # Lazy import

                self.llm = ChatOpenAI(
                    model=llm_model or settings.llm.openai_model,
                    temperature=temperature or settings.llm.openai_temperature,
                    max_tokens=max_tokens or settings.llm.openai_max_tokens,
                    openai_api_key=settings.llm.openai_api_key,
                )
            except Exception as e:
                # Fallback to mock LLM if provider import/init fails
                from unittest.mock import AsyncMock
                self.llm = AsyncMock()
                self.llm.model_name = llm_model or settings.llm.openai_model
                logger.warning(
                    "Failed to initialize OpenAI client, using mock LLM",
                    agent_id=self.agent_id,
                    error=str(e),
                )
        else:
            # Mock LLM for development/demo mode with ainvoke returning AIMessage-like object
            class _MockChat:
                def __init__(self, model_name: str):
                    self.model_name = model_name
                async def ainvoke(self, messages: List[BaseMessage]):
                    # Simple echo content for testing
                    last_human = next((m for m in reversed(messages) if m.__class__.__name__ == 'HumanMessage'), None)
                    content = f"[DEMO MODE] Simulated response from {self.model_name}. "
                    content += (f"You asked: '{last_human.content}'" if last_human else "No user input provided.")
                    from langchain_core.messages import AIMessage
                    return AIMessage(content=content)
            self.llm = _MockChat(llm_model or settings.llm.openai_model)
            logger.warning(
                "OpenAI API key not configured, using mock LLM for development",
                agent_id=self.agent_id,
            )
        
        # Initialize state graph
        self.graph = self._build_graph()
        self.compiled_graph = self.graph.compile()
        
        # Agent state
        self._context: Optional[AgentContext] = None
        
        logger.info(
            "Agent initialized",
            agent_id=self.agent_id,
            name=self.name,
            model=self.llm.model_name,
        )
    
    @abstractmethod
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph state graph for this agent.
        
        Returns:
            StateGraph: The configured state graph
        """
        pass
    
    @abstractmethod
    async def _process_request(self, state: AgentState) -> AgentState:
        """Process a request in the agent's main logic.
        
        Args:
            state: Current agent state
            
        Returns:
            Updated agent state
        """
        pass
    
    def get_system_prompt(self) -> str:
        """Get the system prompt for this agent.
        
        Returns:
            System prompt string
        """
        return f"""You are {self.name}, an AI agent in a financial multi-agent system.

Description: {self.description}

Your role is to process financial data and requests according to your specialized capabilities.
Always provide accurate, helpful, and compliant responses.
When uncertain, ask for clarification or escalate to human oversight.

Current context: You are operating within a secure financial system with proper audit trails.
"""
    
    async def invoke(
        self,
        request: Union[str, Dict[str, Any], BaseMessage],
        context: Optional[AgentContext] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Invoke the agent with a request.
        
        Args:
            request: The request to process
            context: Agent execution context
            **kwargs: Additional parameters
            
        Returns:
            Agent response
        """
        with tracer.start_as_current_span(f"{self.agent_id}.invoke") as span:
            # Set up context
            if context is None:
                context = AgentContext(
                    agent_id=self.agent_id,
                    session_id=str(uuid4()),
                    user_id="system",
                    company_id="default",
                    permissions=[],
                    state={},
                    trace_id=span.get_span_context().trace_id,
                )
            
            self._context = context
            
            # Prepare initial state
            initial_state = self._prepare_initial_state(request, context, **kwargs)
            
            try:
                # Execute the graph
                result = await self.compiled_graph.ainvoke(initial_state)
                
                logger.info(
                    "Agent request processed successfully",
                    agent_id=self.agent_id,
                    session_id=context.session_id,
                    trace_id=context.trace_id,
                )
                
                formatted_response = self._format_response(result)
                # Handle both sync and async _format_response methods
                if asyncio.iscoroutine(formatted_response):
                    return await formatted_response
                return formatted_response
                
            except Exception as e:
                logger.error(
                    "Agent request failed",
                    agent_id=self.agent_id,
                    session_id=context.session_id,
                    error=str(e),
                    trace_id=context.trace_id,
                )
                raise
            finally:
                self._context = None
    
    async def stream(
        self,
        request: Union[str, Dict[str, Any], BaseMessage],
        context: Optional[AgentContext] = None,
        **kwargs: Any,
    ):
        """Stream agent responses for real-time processing.
        
        Args:
            request: The request to process
            context: Agent execution context
            **kwargs: Additional parameters
            
        Yields:
            Streaming response chunks
        """
        with tracer.start_as_current_span(f"{self.agent_id}.stream") as span:
            # Set up context
            if context is None:
                context = AgentContext(
                    agent_id=self.agent_id,
                    session_id=str(uuid4()),
                    user_id="system",
                    company_id="default",
                    permissions=[],
                    state={},
                    trace_id=span.get_span_context().trace_id,
                )
            
            self._context = context
            
            # Prepare initial state
            initial_state = self._prepare_initial_state(request, context, **kwargs)
            
            try:
                # Stream the graph execution
                async for chunk in self.compiled_graph.astream(initial_state):
                    yield self._format_stream_chunk(chunk)
                    
            except Exception as e:
                logger.error(
                    "Agent streaming failed",
                    agent_id=self.agent_id,
                    session_id=context.session_id,
                    error=str(e),
                    trace_id=context.trace_id,
                )
                raise
            finally:
                self._context = None
    
    def _prepare_initial_state(
        self,
        request: Union[str, Dict[str, Any], BaseMessage],
        context: AgentContext,
        **kwargs: Any,
    ) -> AgentState:
        """Prepare the initial state for graph execution.
        
        Args:
            request: The request to process
            context: Agent execution context
            **kwargs: Additional parameters
            
        Returns:
            Initial agent state
        """
        # Convert request to messages
        messages = []
        
        # Add system message
        messages.append(SystemMessage(content=self.get_system_prompt()))
        
        # Add user message
        if isinstance(request, str):
            messages.append(HumanMessage(content=request))
        elif isinstance(request, BaseMessage):
            messages.append(request)
        elif isinstance(request, dict):
            content = request.get("content", str(request))
            messages.append(HumanMessage(content=content))
        
        return AgentState(
            messages=messages,
            context=context,
            metadata=kwargs,
            current_step="start",
            completed_steps=[],
            error=None,
        )
    
    def _format_response(self, result: AgentState) -> Dict[str, Any]:
        """Format the final response from graph execution.
        
        Args:
            result: Final agent state
            
        Returns:
            Formatted response
        """
        # Handle both AgentState and dict results
        if isinstance(result, dict):
            return {
                "agent_id": self.agent_id,
                "session_id": result.get("session_id"),
                "response": result.get("response", "No response generated"),
                "metadata": result.get("metadata", {}),
                "completed_steps": result.get("completed_steps", []),
                "error": result.get("error"),
            }
        
        # Get the last AI message
        messages = getattr(result, 'messages', [])
        ai_messages = [msg for msg in messages if hasattr(msg, 'content') and getattr(msg, '__class__', None) and getattr(msg.__class__, '__name__', '') == 'AIMessage']
        last_message = ai_messages[-1] if ai_messages else None
        
        return {
            "agent_id": self.agent_id,
            "session_id": getattr(getattr(result, 'context', None), 'session_id', None),
            "response": getattr(last_message, 'content', "No response generated") if last_message else "No response generated",
            "metadata": getattr(result, 'metadata', {}),
            "completed_steps": getattr(result, 'completed_steps', []),
            "error": getattr(result, 'error', None),
        }
    
    def _format_stream_chunk(self, chunk: Dict[str, Any]) -> Dict[str, Any]:
        """Format a streaming chunk.
        
        Args:
            chunk: Raw chunk from graph streaming
            
        Returns:
            Formatted chunk
        """
        return {
            "agent_id": self.agent_id,
            "chunk": chunk,
            "timestamp": asyncio.get_event_loop().time(),
        }
    
    async def get_state(self) -> Optional[AgentState]:
        """Get the current agent state.
        
        Returns:
            Current agent state if available
        """
        # This would typically retrieve state from a state store
        # For now, return None as state is managed during execution
        return None
    
    async def update_state(self, state: AgentState) -> None:
        """Update the agent state.
        
        Args:
            state: New agent state
        """
        # This would typically persist state to a state store
        # For now, this is a no-op as state is managed during execution
        pass
    
    def get_capabilities(self) -> List[str]:
        """Get the capabilities of this agent.
        
        Returns:
            List of capability names
        """
        return [
            "natural_language_processing",
            "financial_data_analysis",
            "workflow_execution",
            "error_handling",
            "audit_logging",
        ]
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get agent metadata.
        
        Returns:
            Agent metadata
        """
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "description": self.description,
            "capabilities": self.get_capabilities(),
            "model": self.llm.model_name,
            "version": "0.1.0",
        }


class SimpleAgent(BaseAgent):
    """A simple agent implementation for basic tasks."""
    
    def _build_graph(self) -> StateGraph:
        """Build a simple linear graph."""
        graph = StateGraph(AgentState)
        
        # Add nodes
        graph.add_node("process", self._process_request)
        
        # Add edges
        graph.set_entry_point("process")
        graph.add_edge("process", END)
        
        return graph
    
    async def _process_request(self, state: AgentState) -> AgentState:
        """Simple request processing."""
        with tracer.start_as_current_span(f"{self.agent_id}.process_request"):
            try:
                # Get the last human message
                human_messages = [msg for msg in state.messages if isinstance(msg, HumanMessage)]
                if not human_messages:
                    raise ValueError("No human message found in state")
                
                last_human_message = human_messages[-1]
                
                # Process with LLM
                if settings.llm.has_openai_key:
                    response = await self.llm.ainvoke(state.messages)
                else:
                    # Mock response for development
                    from langchain.schema import AIMessage
                    response = AIMessage(content=f"[DEMO MODE] This is a simulated response from {self.name}. The agent would normally process: '{last_human_message.content}' and provide detailed financial analysis. Configure OPENAI_API_KEY for full functionality.")
                
                # Update state
                state.messages.append(response)
                state.completed_steps.append("process")
                state.current_step = "completed"
                
                logger.info(
                    "Request processed",
                    agent_id=self.agent_id,
                    input_length=len(last_human_message.content),
                    output_length=len(response.content),
                    demo_mode=not settings.llm.has_openai_key,
                )
                
                return state
                
            except Exception as e:
                logger.error(
                    "Request processing failed",
                    agent_id=self.agent_id,
                    error=str(e),
                )
                state.error = str(e)
                state.current_step = "error"
                return state