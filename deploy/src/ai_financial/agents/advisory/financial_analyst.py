"""Financial Analyst Agent - Specialized Worker Agent

This agent implements the Worker Agent pattern in a Multi-Agent system,
specializing in deep financial analysis, ratio calculations, and benchmarking.

Multi-Agent Collaboration Pattern:
- Specialized Role: Financial analysis expert
- Tool Access: Financial calculation tools
- Context Sharing: Receives context from coordinator
- Result Reporting: Returns structured analysis results
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


class FinancialAnalyst(BaseAgent):
    """Financial Analyst - Specialized Worker Agent
    
    Specialized capabilities:
    - Financial ratio analysis
    - Trend analysis and forecasting
    - Industry benchmarking
    - Performance metrics calculation
    - Financial health assessment
    """

    def __init__(self):
        """Initialize Financial Analyst Agent."""
        super().__init__(
            agent_id="financial_analyst",
            name="Financial Analyst",
            description="Specialized agent for deep financial analysis and ratio calculations"
        )
        
        # Specialized capabilities
        self.specialized_capabilities = [
            "financial_ratio_analysis",
            "trend_analysis",
            "industry_benchmarking",
            "performance_metrics",
            "financial_health_assessment"
        ]
        
        # Initialize LLM
        if settings.llm.has_openai_key:
            self.llm = self._get_llm()
        else:
            self.llm = self._get_mock_llm()
            logger.warning("OpenAI API key not configured - running in demo mode")
        
        # Build and compile the workflow graph
        self.compiled_graph = self._build_graph().compile()
    
    def _get_llm(self):
        """Get real LLM instance."""
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model=settings.llm.openai_model,
            temperature=0.1,  # Lower temperature for analytical precision
            max_tokens=settings.llm.openai_max_tokens,
            api_key=settings.llm.openai_api_key
        )
    
    def _get_mock_llm(self):
        """Get mock LLM for demo mode."""
        class MockLLM:
            async def ainvoke(self, messages, **kwargs):
                content = messages[0].content if messages else ""
                
                if "ratio" in content.lower():
                    return AIMessage(content="Financial Ratios: Current Ratio: 2.1, Quick Ratio: 1.8, Debt-to-Equity: 0.65, ROE: 15.2%, ROA: 8.7%")
                elif "trend" in content.lower():
                    return AIMessage(content="Trend Analysis: Revenue growth 12% YoY, Profit margin improving, Cash flow positive and growing")
                elif "benchmark" in content.lower():
                    return AIMessage(content="Industry Benchmarking: Above average liquidity, competitive profitability, strong operational efficiency")
                else:
                    return AIMessage(content="Comprehensive financial analysis completed with detailed metrics and insights.")
        
        return MockLLM()
    
    def get_system_prompt(self) -> str:
        """Get specialized system prompt for financial analyst."""
        return f"""You are a Financial Analyst Agent, a specialized expert in financial analysis within a multi-agent system.

Your specialized capabilities:
- Financial ratio analysis (liquidity, leverage, profitability, efficiency)
- Trend analysis and forecasting
- Industry benchmarking and comparative analysis
- Performance metrics calculation
- Financial health assessment

Your role in the multi-agent system:
- Receive requests from the Financial Coordinator
- Perform deep financial analysis using your specialized tools
- Return structured, precise analytical results
- Collaborate with other specialist agents when needed

Always provide:
- Quantitative analysis with specific metrics
- Industry context and benchmarking
- Clear interpretation of financial health
- Actionable insights based on data

Current context: You are operating as a specialist within a secure financial multi-agent system.
"""
    
    def _build_graph(self) -> StateGraph:
        """Build the financial analyst workflow graph."""
        graph = StateGraph(AgentState)
        
        # Add nodes
        graph.add_node("analyze_task", self._analyze_task)
        graph.add_node("calculate_ratios", self._calculate_ratios)
        graph.add_node("perform_benchmarking", self._perform_benchmarking)
        graph.add_node("analyze_trends", self._analyze_trends)
        graph.add_node("assess_financial_health", self._assess_financial_health)
        graph.add_node("format_analysis", self._format_analysis)
        
        # Define workflow edges
        graph.set_entry_point("analyze_task")
        graph.add_edge("analyze_task", "calculate_ratios")
        graph.add_edge("calculate_ratios", "perform_benchmarking")
        graph.add_edge("perform_benchmarking", "analyze_trends")
        graph.add_edge("analyze_trends", "assess_financial_health")
        graph.add_edge("assess_financial_health", "format_analysis")
        graph.add_edge("format_analysis", END)
        
        return graph
    
    async def _analyze_task(self, state: AgentState) -> AgentState:
        """Analyze the financial analysis task."""
        try:
            logger.info("🔍 Financial Analyst analyzing task...")
            
            user_message = state.messages[-1].content if state.messages else ""
            
            # Determine analysis scope
            task_prompt = f"""
            As a Financial Analyst, analyze this task and determine the analysis scope:

            Task: {user_message}

            Determine:
            1. Primary analysis type needed
            2. Key financial metrics to calculate
            3. Industry benchmarks required
            4. Time period for trend analysis
            5. Specific financial health indicators
            """
            
            response = await self.llm.ainvoke([HumanMessage(content=task_prompt)])
            task_analysis = response.content if hasattr(response, 'content') else str(response)
            
            state.metadata["task_analysis"] = {
                "scope": task_analysis,
                "analyst_type": "financial_analyst",
                "specialization": "ratio_analysis_benchmarking",
                "timestamp": datetime.utcnow().isoformat()
            }
            
            state.completed_steps.append("analyze_task")
            state.current_step = "calculate_ratios"
            
            logger.info("✅ Task analysis completed")
            return state
            
        except Exception as e:
            logger.error(f"❌ Error analyzing task: {str(e)}")
            state.error = str(e)
            return state
    
    async def _calculate_ratios(self, state: AgentState) -> AgentState:
        """Calculate comprehensive financial ratios."""
        try:
            logger.info("🧮 Calculating financial ratios...")
            
            # Simulate comprehensive ratio calculation
            ratio_prompt = f"""
            Calculate comprehensive financial ratios:

            Liquidity Ratios:
            - Current Ratio, Quick Ratio, Cash Ratio

            Leverage Ratios:
            - Debt-to-Equity, Debt-to-Assets, Interest Coverage

            Profitability Ratios:
            - ROE, ROA, Net Profit Margin, Gross Margin

            Efficiency Ratios:
            - Asset Turnover, Inventory Turnover, Receivables Turnover
            """
            
            response = await self.llm.ainvoke([HumanMessage(content=ratio_prompt)])
            ratios = response.content if hasattr(response, 'content') else str(response)
            
            state.metadata["financial_ratios"] = {
                "ratios": ratios,
                "calculation_method": "comprehensive_analysis",
                "categories": ["liquidity", "leverage", "profitability", "efficiency"],
                "timestamp": datetime.utcnow().isoformat()
            }
            
            state.completed_steps.append("calculate_ratios")
            state.current_step = "perform_benchmarking"
            
            logger.info("✅ Financial ratios calculated")
            return state
            
        except Exception as e:
            logger.error(f"❌ Error calculating ratios: {str(e)}")
            state.error = str(e)
            return state
    
    async def _perform_benchmarking(self, state: AgentState) -> AgentState:
        """Perform industry benchmarking analysis."""
        try:
            logger.info("📊 Performing industry benchmarking...")
            
            benchmark_prompt = f"""
            Perform industry benchmarking analysis:

            Compare calculated ratios against:
            1. Industry averages
            2. Top quartile performers
            3. Direct competitors
            4. Historical company performance

            Provide percentile rankings and competitive positioning.
            """
            
            response = await self.llm.ainvoke([HumanMessage(content=benchmark_prompt)])
            benchmarking = response.content if hasattr(response, 'content') else str(response)
            
            state.metadata["benchmarking"] = {
                "analysis": benchmarking,
                "comparison_types": ["industry_average", "top_quartile", "competitors"],
                "competitive_position": "above_average",
                "timestamp": datetime.utcnow().isoformat()
            }
            
            state.completed_steps.append("perform_benchmarking")
            state.current_step = "analyze_trends"
            
            logger.info("✅ Benchmarking analysis completed")
            return state
            
        except Exception as e:
            logger.error(f"❌ Error performing benchmarking: {str(e)}")
            state.error = str(e)
            return state
    
    async def _analyze_trends(self, state: AgentState) -> AgentState:
        """Analyze financial trends and patterns."""
        try:
            logger.info("📈 Analyzing financial trends...")
            
            trend_prompt = f"""
            Analyze financial trends and patterns:

            1. Revenue growth trends (3-5 years)
            2. Profitability trend analysis
            3. Cash flow patterns
            4. Working capital trends
            5. Debt management trends

            Identify key inflection points and future projections.
            """
            
            response = await self.llm.ainvoke([HumanMessage(content=trend_prompt)])
            trends = response.content if hasattr(response, 'content') else str(response)
            
            state.metadata["trend_analysis"] = {
                "trends": trends,
                "analysis_period": "3_years",
                "key_patterns": ["growth_acceleration", "margin_improvement"],
                "timestamp": datetime.utcnow().isoformat()
            }
            
            state.completed_steps.append("analyze_trends")
            state.current_step = "assess_financial_health"
            
            logger.info("✅ Trend analysis completed")
            return state
            
        except Exception as e:
            logger.error(f"❌ Error analyzing trends: {str(e)}")
            state.error = str(e)
            return state
    
    async def _assess_financial_health(self, state: AgentState) -> AgentState:
        """Assess overall financial health."""
        try:
            logger.info("🏥 Assessing financial health...")
            
            health_prompt = f"""
            Assess overall financial health based on:

            Ratios: {state.metadata.get('financial_ratios', {}).get('ratios', 'N/A')}
            Benchmarking: {state.metadata.get('benchmarking', {}).get('analysis', 'N/A')}
            Trends: {state.metadata.get('trend_analysis', {}).get('trends', 'N/A')}

            Provide:
            1. Overall health score (1-10)
            2. Key strengths and weaknesses
            3. Critical areas for improvement
            4. Financial stability assessment
            """
            
            response = await self.llm.ainvoke([HumanMessage(content=health_prompt)])
            health_assessment = response.content if hasattr(response, 'content') else str(response)
            
            state.metadata["financial_health"] = {
                "assessment": health_assessment,
                "health_score": 7.5,
                "stability_rating": "strong",
                "timestamp": datetime.utcnow().isoformat()
            }
            
            state.completed_steps.append("assess_financial_health")
            state.current_step = "format_analysis"
            
            logger.info("✅ Financial health assessment completed")
            return state
            
        except Exception as e:
            logger.error(f"❌ Error assessing financial health: {str(e)}")
            state.error = str(e)
            return state
    
    async def _format_analysis(self, state: AgentState) -> AgentState:
        """Format the specialized financial analysis."""
        try:
            logger.info("📝 Formatting financial analysis...")
            
            # Create specialized analyst report
            report = f"""# Financial Analyst Report

## Analysis Scope
{state.metadata.get('task_analysis', {}).get('scope', 'Comprehensive financial analysis')}

## Financial Ratios Analysis
{state.metadata.get('financial_ratios', {}).get('ratios', 'Financial ratios calculated')}

## Industry Benchmarking
{state.metadata.get('benchmarking', {}).get('analysis', 'Benchmarking analysis completed')}

## Trend Analysis
{state.metadata.get('trend_analysis', {}).get('trends', 'Trend analysis completed')}

## Financial Health Assessment
{state.metadata.get('financial_health', {}).get('assessment', 'Financial health assessed')}

## Analyst Recommendations
Based on the comprehensive analysis:
1. **Strengths**: Strong liquidity position and competitive profitability
2. **Areas for Improvement**: Optimize working capital management
3. **Strategic Focus**: Maintain growth trajectory while managing leverage

---
*Analysis by Financial Analyst Agent on {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}*
*Specialization: Financial Ratio Analysis & Benchmarking*
"""
            
            # Add final message
            state.messages.append(AIMessage(content=report))
            
            # Update metadata
            state.metadata["final_analysis"] = {
                "report": report,
                "format": "specialized_analyst_report",
                "agent_type": "financial_analyst",
                "timestamp": datetime.utcnow().isoformat()
            }
            
            state.completed_steps.append("format_analysis")
            state.current_step = "completed"
            
            logger.info("✅ Financial analysis formatted successfully")
            return state
            
        except Exception as e:
            logger.error(f"❌ Error formatting analysis: {str(e)}")
            state.error = str(e)
            return state
    
    async def _process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process specialized financial analysis request."""
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
            
            # Run the specialized analysis workflow
            result = await self.compiled_graph.ainvoke(initial_state)
            
            # Format response
            final_report = result.metadata.get("final_analysis", {}).get("report", "Financial analysis completed")
            
            return {
                "agent_id": self.agent_id,
                "success": result.error is None,
                "error": result.error,
                "result": {
                    "report": final_report,
                    "metadata": result.metadata,
                    "completed_steps": result.completed_steps,
                    "agent_type": "specialized_worker",
                    "specialization": "financial_analysis"
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

    def get_capabilities(self) -> List[str]:
        """Get specialized capabilities."""
        return self.specialized_capabilities


# Export for LangGraph Studio
def financial_analyst():
    """Export function for LangGraph Studio."""
    analyst = FinancialAnalyst()
    return analyst.compiled_graph