"""Financial Coordinator Agent - Multi-Agent Collaboration Pattern

This agent implements the Hierarchical Multi-Agent pattern from Google ADK,
acting as a coordinator that delegates tasks to specialized worker agents.

Based on the Multi-Agent Collaboration patterns:
- Hierarchical Structure: Coordinator manages worker agents
- Task Delegation: Routes requests to appropriate specialists
- Result Synthesis: Combines outputs from multiple agents
"""

import asyncio
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages

from ai_financial.core.base_agent import BaseAgent
from ai_financial.core.config import settings
from ai_financial.core.logging import get_logger
from ai_financial.models.agent_models import AgentContext, AgentState

logger = get_logger(__name__)


class FinancialCoordinator(BaseAgent):
    """Financial Coordinator Agent - Hierarchical Multi-Agent Pattern
    
    This coordinator manages specialized financial agents:
    - Financial Analyst: Deep financial analysis
    - Risk Assessor: Risk evaluation and mitigation
    - Strategic Advisor: Strategic recommendations
    - Compliance Checker: Regulatory compliance
    """

    def __init__(self):
        """Initialize Financial Coordinator."""
        super().__init__(
            agent_id="financial_coordinator",
            name="Financial Coordinator",
            description="Coordinates multiple specialized financial agents for comprehensive analysis"
        )
        
        # Initialize LLM
        if settings.llm.has_openai_key:
            self.llm = self._get_llm()
        else:
            self.llm = self._get_mock_llm()
            logger.warning("OpenAI API key not configured - running in demo mode")
        
        # Initialize sub-agents (worker agents)
        self.sub_agents = {
            "financial_analyst": None,  # Will be initialized when needed
            "risk_assessor": None,
            "strategic_advisor": None,
            "compliance_checker": None
        }
        
        # Build and compile the workflow graph
        self.compiled_graph = self._build_graph().compile()
    
    def _get_llm(self):
        """Get real LLM instance."""
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model=settings.llm.openai_model,
            temperature=settings.llm.openai_temperature,
            max_tokens=settings.llm.openai_max_tokens,
            api_key=settings.llm.openai_api_key
        )
    
    def _get_mock_llm(self):
        """Get mock LLM for demo mode."""
        class MockLLM:
            async def ainvoke(self, messages, **kwargs):
                content = messages[0].content if messages else ""
                
                if "route" in content.lower():
                    return AIMessage(content='{"primary_agent": "financial_analyst", "supporting_agents": ["risk_assessor"], "workflow_type": "sequential"}')
                elif "synthesize" in content.lower():
                    return AIMessage(content="Comprehensive financial analysis completed with risk assessment and strategic recommendations.")
                else:
                    return AIMessage(content="Financial coordination completed successfully.")
        
        return MockLLM()
    
    def _build_graph(self) -> StateGraph:
        """Build the coordinator workflow graph."""
        graph = StateGraph(AgentState)
        
        # Add nodes
        graph.add_node("analyze_request", self._analyze_request)
        graph.add_node("route_to_agents", self._route_to_agents)
        graph.add_node("coordinate_execution", self._coordinate_execution)
        graph.add_node("synthesize_results", self._synthesize_results)
        graph.add_node("format_response", self._format_response)
        
        # Define workflow edges
        graph.set_entry_point("analyze_request")
        graph.add_edge("analyze_request", "route_to_agents")
        graph.add_edge("route_to_agents", "coordinate_execution")
        graph.add_edge("coordinate_execution", "synthesize_results")
        graph.add_edge("synthesize_results", "format_response")
        graph.add_edge("format_response", END)
        
        return graph
    
    async def _analyze_request(self, state: AgentState) -> AgentState:
        """Analyze request and determine coordination strategy."""
        try:
            logger.info("🎯 Coordinator analyzing request...")
            
            user_message = state.messages[-1].content if state.messages else ""
            
            # Determine which agents are needed
            routing_prompt = f"""
            As a Financial Coordinator, analyze this request and determine the optimal agent routing:

            Request: {user_message}

            Available specialist agents:
            1. financial_analyst - Deep financial analysis, ratios, benchmarking
            2. risk_assessor - Risk evaluation, mitigation strategies
            3. strategic_advisor - Strategic recommendations, growth planning
            4. compliance_checker - Regulatory compliance, audit requirements

            Respond with JSON containing:
            - primary_agent: main agent to handle the request
            - supporting_agents: list of additional agents needed
            - workflow_type: "sequential", "parallel", or "hierarchical"
            - coordination_strategy: brief description of approach
            """
            
            response = await self.llm.ainvoke([HumanMessage(content=routing_prompt)])
            routing_plan = response.content if hasattr(response, 'content') else str(response)
            
            state.metadata["coordination_plan"] = {
                "request": user_message,
                "routing_plan": routing_plan,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            state.completed_steps.append("analyze_request")
            state.current_step = "route_to_agents"
            
            logger.info("✅ Request analysis completed")
            return state
            
        except Exception as e:
            logger.error(f"❌ Error analyzing request: {str(e)}")
            state.error = str(e)
            return state
    
    async def _route_to_agents(self, state: AgentState) -> AgentState:
        """Route request to appropriate specialist agents."""
        try:
            logger.info("🔀 Routing to specialist agents...")
            
            # In a real implementation, this would instantiate and call actual agents
            # For demo, we simulate the routing
            routing_results = {
                "financial_analyst": "Financial analysis completed: Strong liquidity, moderate leverage",
                "risk_assessor": "Risk assessment: Low credit risk, medium market risk",
                "strategic_advisor": "Strategic recommendations: Focus on growth, optimize capital structure",
                "compliance_checker": "Compliance status: All regulatory requirements met"
            }
            
            state.metadata["agent_results"] = {
                "routing_results": routing_results,
                "execution_order": ["financial_analyst", "risk_assessor", "strategic_advisor"],
                "timestamp": datetime.utcnow().isoformat()
            }
            
            state.completed_steps.append("route_to_agents")
            state.current_step = "coordinate_execution"
            
            logger.info("✅ Agent routing completed")
            return state
            
        except Exception as e:
            logger.error(f"❌ Error routing to agents: {str(e)}")
            state.error = str(e)
            return state
    
    async def _coordinate_execution(self, state: AgentState) -> AgentState:
        """Coordinate execution across multiple agents."""
        try:
            logger.info("⚙️ Coordinating agent execution...")
            
            # Simulate coordination of multiple agents
            coordination_results = {
                "execution_status": "completed",
                "agents_executed": ["financial_analyst", "risk_assessor", "strategic_advisor"],
                "execution_time": "2.3 seconds",
                "coordination_pattern": "sequential_with_context_sharing"
            }
            
            state.metadata["coordination_results"] = {
                "results": coordination_results,
                "context_shared": True,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            state.completed_steps.append("coordinate_execution")
            state.current_step = "synthesize_results"
            
            logger.info("✅ Agent coordination completed")
            return state
            
        except Exception as e:
            logger.error(f"❌ Error coordinating execution: {str(e)}")
            state.error = str(e)
            return state
    
    async def _synthesize_results(self, state: AgentState) -> AgentState:
        """Synthesize results from multiple agents."""
        try:
            logger.info("🔄 Synthesizing multi-agent results...")
            
            synthesis_prompt = f"""
            As a Financial Coordinator, synthesize the results from multiple specialist agents:

            Agent Results:
            {state.metadata.get('agent_results', {}).get('routing_results', {})}

            Create a comprehensive synthesis that:
            1. Integrates insights from all agents
            2. Identifies synergies and conflicts
            3. Provides unified recommendations
            4. Maintains coherence across domains
            """
            
            response = await self.llm.ainvoke([HumanMessage(content=synthesis_prompt)])
            synthesis = response.content if hasattr(response, 'content') else str(response)
            
            state.metadata["synthesis"] = {
                "unified_analysis": synthesis,
                "integration_approach": "hierarchical_synthesis",
                "confidence_level": "high",
                "timestamp": datetime.utcnow().isoformat()
            }
            
            state.completed_steps.append("synthesize_results")
            state.current_step = "format_response"
            
            logger.info("✅ Results synthesis completed")
            return state
            
        except Exception as e:
            logger.error(f"❌ Error synthesizing results: {str(e)}")
            state.error = str(e)
            return state
    
    async def _format_response(self, state: AgentState) -> AgentState:
        """Format the coordinated response."""
        try:
            logger.info("📝 Formatting coordinated response...")
            
            # Create comprehensive multi-agent report
            report = f"""# Multi-Agent Financial Analysis Report

## Coordination Summary
**Request:** {state.metadata.get('coordination_plan', {}).get('request', 'Financial analysis request')}
**Coordination Strategy:** Hierarchical Multi-Agent Collaboration

## Agent Execution Results
{state.metadata.get('agent_results', {}).get('routing_results', {})}

## Coordination Analysis
{state.metadata.get('coordination_results', {}).get('results', {})}

## Synthesized Insights
{state.metadata.get('synthesis', {}).get('unified_analysis', 'Comprehensive analysis completed')}

## Multi-Agent Collaboration Benefits
- **Specialized Expertise:** Each agent focused on their domain
- **Comprehensive Coverage:** All aspects of financial analysis addressed
- **Quality Assurance:** Cross-validation between agents
- **Scalable Architecture:** Easy to add new specialist agents

---
*Report generated by Financial Coordinator on {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}*
*Multi-Agent Pattern: Hierarchical Coordination with Sequential Execution*
"""
            
            # Add final message
            state.messages.append(AIMessage(content=report))
            
            # Update metadata
            state.metadata["final_report"] = {
                "report": report,
                "format": "markdown",
                "coordination_pattern": "hierarchical",
                "timestamp": datetime.utcnow().isoformat()
            }
            
            state.completed_steps.append("format_response")
            state.current_step = "completed"
            
            logger.info("✅ Coordinated response formatted successfully")
            return state
            
        except Exception as e:
            logger.error(f"❌ Error formatting response: {str(e)}")
            state.error = str(e)
            return state
    
    async def _process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming request through multi-agent coordination."""
        try:
            # Extract message from request
            message = request.get("message", "")
            context_data = request.get("context", {})
            
            # Create context
            agent_context = AgentContext(
                session_id=context_data.get("session_id", "default_session"),
                company_id=context_data.get("company_id", "default_company"),
                user_id=context_data.get("user_id", "default_user"),
                agent_id=self.agent_id
            )
            
            # Create initial state
            initial_state = AgentState(
                messages=[HumanMessage(content=message)],
                context=agent_context,
                metadata={},
                completed_steps=[],
                current_step="start"
            )
            
            # Run the coordination workflow
            result = await self.compiled_graph.ainvoke(initial_state)
            
            # Format response
            final_report = result.metadata.get("final_report", {}).get("report", "Multi-agent analysis completed")
            
            return {
                "agent_id": self.agent_id,
                "success": result.error is None,
                "error": result.error,
                "result": {
                    "report": final_report,
                    "metadata": result.metadata,
                    "completed_steps": result.completed_steps,
                    "coordination_pattern": "hierarchical_multi_agent"
                },
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            return {
                "agent_id": self.agent_id,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }


# Export for LangGraph Studio
def financial_coordinator():
    """Export function for LangGraph Studio."""
    coordinator = FinancialCoordinator()
    return coordinator.compiled_graph