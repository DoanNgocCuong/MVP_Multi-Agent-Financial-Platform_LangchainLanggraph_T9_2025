"""AI CFO Agent for industry-specific financial advisory and analysis."""

from typing import Any, Dict, List, Optional
from decimal import Decimal
from datetime import datetime, timedelta

from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END

from ai_financial.core.base_agent import BaseAgent
from ai_financial.models.agent_models import AgentState
from ai_financial.models.financial_models import (
    Transaction, Account, Invoice, Forecast, ForecastType
)
from ai_financial.core.logging import get_logger, get_tracer

logger = get_logger(__name__)
tracer = get_tracer(__name__)


class AICFOAgent(BaseAgent):
    """AI CFO Agent providing industry-specific financial advisory and analysis."""
    
    def __init__(self, industry: str = "general"):
        """Initialize the AI CFO Agent.
        
        Args:
            industry: Industry specialization (healthcare, automotive, pharmaceutical, etc.)
        """
        self.industry = industry
        
        super().__init__(
            agent_id="ai_cfo_agent",
            name="AI CFO",
            description=f"AI Chief Financial Officer specialized in {industry} industry providing financial advisory, analysis, and strategic insights",
        )
        
        # Industry-specific knowledge
        self.industry_metrics = self._load_industry_metrics()
        self.industry_benchmarks = self._load_industry_benchmarks()
        
        logger.info(
            "AI CFO Agent initialized",
            industry=self.industry,
            metrics_count=len(self.industry_metrics),
        )
    
    def _build_graph(self) -> StateGraph:
        """Build the AI CFO agent workflow graph."""
        graph = StateGraph(AgentState)
        
        # Add nodes
        graph.add_node("analyze_request", self._analyze_request)
        graph.add_node("gather_data", self._gather_financial_data)
        graph.add_node("perform_analysis", self._perform_financial_analysis)
        graph.add_node("generate_insights", self._generate_insights)
        graph.add_node("assess_risks", self._assess_risks)
        graph.add_node("provide_recommendations", self._provide_recommendations)
        graph.add_node("format_response", self._format_response)
        
        # Add edges
        graph.set_entry_point("analyze_request")
        graph.add_edge("analyze_request", "gather_data")
        graph.add_edge("gather_data", "perform_analysis")
        graph.add_edge("perform_analysis", "generate_insights")
        graph.add_edge("generate_insights", "assess_risks")
        graph.add_edge("assess_risks", "provide_recommendations")
        graph.add_edge("provide_recommendations", "format_response")
        graph.add_edge("format_response", END)
        
        return graph
    
    def get_system_prompt(self) -> str:
        """Get the AI CFO system prompt."""
        return f"""You are an AI Chief Financial Officer (CFO) specialized in the {self.industry} industry.

Your expertise includes:
- Financial analysis and interpretation
- Industry-specific financial metrics and KPIs
- Risk assessment and mitigation strategies
- Strategic financial planning and forecasting
- Regulatory compliance and reporting
- Cash flow management and optimization
- Investment analysis and capital allocation

Industry Specialization: {self.industry}
Key Industry Metrics: {', '.join(self.industry_metrics.keys())}

Your role is to:
1. Analyze financial data with industry context
2. Identify trends, patterns, and anomalies
3. Assess financial risks and opportunities
4. Provide actionable recommendations
5. Ensure compliance with industry regulations
6. Support strategic decision-making

Always provide:
- Clear, executive-level insights
- Quantified analysis with specific numbers
- Industry benchmarks and comparisons
- Risk assessments with mitigation strategies
- Actionable recommendations with timelines
- Proper citations and data sources

Maintain a professional, confident tone while being transparent about limitations and assumptions.
"""
    
    async def _analyze_request(self, state: AgentState) -> AgentState:
        """Analyze the incoming request to determine analysis type."""
        with tracer.start_as_current_span("ai_cfo.analyze_request"):
            try:
                # Get the user request
                human_messages = [msg for msg in state.messages if isinstance(msg, HumanMessage)]
                if not human_messages:
                    raise ValueError("No user request found")
                
                user_request = human_messages[-1].content
                
                # Analyze request type using LLM
                analysis_prompt = f"""Analyze this financial request and determine the type of analysis needed:

Request: {user_request}

Classify the request into one or more categories:
1. Financial Health Assessment
2. Cash Flow Analysis
3. Profitability Analysis
4. Risk Assessment
5. Investment Analysis
6. Compliance Review
7. Strategic Planning
8. Industry Benchmarking

Respond with a JSON object containing:
- analysis_types: list of applicable categories
- priority: high/medium/low
- data_requirements: list of data types needed
- timeline: expected analysis timeline
"""
                
                messages = [
                    SystemMessage(content="You are a financial analysis classifier."),
                    HumanMessage(content=analysis_prompt)
                ]
                
                response = await self.llm.ainvoke(messages)
                
                # Store analysis plan in metadata
                state.metadata["analysis_plan"] = {
                    "request": user_request,
                    "classification": response.content,
                    "timestamp": datetime.utcnow().isoformat()
                }
                
                state.completed_steps.append("analyze_request")
                state.current_step = "gather_data"
                
                logger.info(
                    "Request analyzed",
                    agent_id=self.agent_id,
                    request_length=len(user_request),
                )
                
                return state
                
            except Exception as e:
                logger.error("Request analysis failed", error=str(e))
                state.error = f"Request analysis failed: {str(e)}"
                return state
    
    async def _gather_financial_data(self, state: AgentState) -> AgentState:
        """Gather relevant financial data for analysis."""
        with tracer.start_as_current_span("ai_cfo.gather_data"):
            try:
                # In a real implementation, this would fetch data from databases
                # For now, we'll simulate data gathering
                
                company_id = state.context.company_id if state.context else "default"
                
                # Simulate financial data
                financial_data = {
                    "transactions": self._get_sample_transactions(),
                    "accounts": self._get_sample_accounts(),
                    "invoices": self._get_sample_invoices(),
                    "cash_flow": self._get_sample_cash_flow(),
                    "industry_benchmarks": self.industry_benchmarks,
                }
                
                state.metadata["financial_data"] = financial_data
                state.completed_steps.append("gather_data")
                state.current_step = "perform_analysis"
                
                logger.info(
                    "Financial data gathered",
                    agent_id=self.agent_id,
                    company_id=company_id,
                    data_points=len(financial_data),
                )
                
                return state
                
            except Exception as e:
                logger.error("Data gathering failed", error=str(e))
                state.error = f"Data gathering failed: {str(e)}"
                return state
    
    async def _perform_financial_analysis(self, state: AgentState) -> AgentState:
        """Perform comprehensive financial analysis."""
        with tracer.start_as_current_span("ai_cfo.perform_analysis"):
            try:
                financial_data = state.metadata.get("financial_data", {})
                
                # Perform various financial analyses
                analysis_results = {
                    "liquidity_analysis": self._analyze_liquidity(financial_data),
                    "profitability_analysis": self._analyze_profitability(financial_data),
                    "efficiency_analysis": self._analyze_efficiency(financial_data),
                    "leverage_analysis": self._analyze_leverage(financial_data),
                    "industry_comparison": self._compare_to_industry(financial_data),
                }
                
                state.metadata["analysis_results"] = analysis_results
                state.completed_steps.append("perform_analysis")
                state.current_step = "generate_insights"
                
                logger.info(
                    "Financial analysis completed",
                    agent_id=self.agent_id,
                    analysis_types=list(analysis_results.keys()),
                )
                
                return state
                
            except Exception as e:
                logger.error("Financial analysis failed", error=str(e))
                state.error = f"Financial analysis failed: {str(e)}"
                return state
    
    async def _generate_insights(self, state: AgentState) -> AgentState:
        """Generate financial insights using LLM."""
        with tracer.start_as_current_span("ai_cfo.generate_insights"):
            try:
                analysis_results = state.metadata.get("analysis_results", {})
                
                # Create insights prompt
                insights_prompt = f"""Based on the following financial analysis results, generate key insights:

Analysis Results:
{self._format_analysis_for_llm(analysis_results)}

Industry: {self.industry}

Generate insights covering:
1. Key financial strengths and weaknesses
2. Trends and patterns identified
3. Performance vs industry benchmarks
4. Areas of concern or opportunity
5. Strategic implications

Provide specific, quantified insights with clear explanations.
"""
                
                messages = [
                    SystemMessage(content=self.get_system_prompt()),
                    HumanMessage(content=insights_prompt)
                ]
                
                response = await self.llm.ainvoke(messages)
                
                state.metadata["insights"] = response.content
                state.completed_steps.append("generate_insights")
                state.current_step = "assess_risks"
                
                logger.info(
                    "Insights generated",
                    agent_id=self.agent_id,
                    insights_length=len(response.content),
                )
                
                return state
                
            except Exception as e:
                logger.error("Insight generation failed", error=str(e))
                state.error = f"Insight generation failed: {str(e)}"
                return state
    
    async def _assess_risks(self, state: AgentState) -> AgentState:
        """Assess financial risks and opportunities."""
        with tracer.start_as_current_span("ai_cfo.assess_risks"):
            try:
                analysis_results = state.metadata.get("analysis_results", {})
                
                # Perform risk assessment
                risk_assessment = {
                    "liquidity_risk": self._assess_liquidity_risk(analysis_results),
                    "credit_risk": self._assess_credit_risk(analysis_results),
                    "operational_risk": self._assess_operational_risk(analysis_results),
                    "market_risk": self._assess_market_risk(analysis_results),
                    "compliance_risk": self._assess_compliance_risk(analysis_results),
                }
                
                # Generate risk summary using LLM
                risk_prompt = f"""Based on the risk assessment data, provide a comprehensive risk analysis:

Risk Assessment:
{self._format_risks_for_llm(risk_assessment)}

Industry Context: {self.industry}

Provide:
1. Overall risk rating (Low/Medium/High)
2. Top 3 risk priorities
3. Risk mitigation strategies
4. Monitoring recommendations
5. Timeline for risk review

Be specific and actionable in your recommendations.
"""
                
                messages = [
                    SystemMessage(content=self.get_system_prompt()),
                    HumanMessage(content=risk_prompt)
                ]
                
                response = await self.llm.ainvoke(messages)
                
                state.metadata["risk_assessment"] = {
                    "detailed_risks": risk_assessment,
                    "risk_summary": response.content
                }
                
                state.completed_steps.append("assess_risks")
                state.current_step = "provide_recommendations"
                
                logger.info(
                    "Risk assessment completed",
                    agent_id=self.agent_id,
                    risk_categories=len(risk_assessment),
                )
                
                return state
                
            except Exception as e:
                logger.error("Risk assessment failed", error=str(e))
                state.error = f"Risk assessment failed: {str(e)}"
                return state
    
    async def _provide_recommendations(self, state: AgentState) -> AgentState:
        """Provide actionable financial recommendations."""
        with tracer.start_as_current_span("ai_cfo.provide_recommendations"):
            try:
                insights = state.metadata.get("insights", "")
                risk_assessment = state.metadata.get("risk_assessment", {})
                
                # Generate recommendations using LLM
                recommendations_prompt = f"""Based on the financial insights and risk assessment, provide strategic recommendations:

Financial Insights:
{insights}

Risk Assessment Summary:
{risk_assessment.get('risk_summary', '')}

Industry: {self.industry}

Provide recommendations in these categories:
1. Immediate Actions (0-30 days)
2. Short-term Initiatives (1-6 months)
3. Long-term Strategic Moves (6+ months)
4. Financial Controls and Monitoring
5. Industry-specific Opportunities

For each recommendation, include:
- Specific action items
- Expected impact/benefits
- Resource requirements
- Timeline
- Success metrics

Prioritize recommendations by impact and feasibility.
"""
                
                messages = [
                    SystemMessage(content=self.get_system_prompt()),
                    HumanMessage(content=recommendations_prompt)
                ]
                
                response = await self.llm.ainvoke(messages)
                
                state.metadata["recommendations"] = response.content
                state.completed_steps.append("provide_recommendations")
                state.current_step = "format_response"
                
                logger.info(
                    "Recommendations generated",
                    agent_id=self.agent_id,
                    recommendations_length=len(response.content),
                )
                
                return state
                
            except Exception as e:
                logger.error("Recommendation generation failed", error=str(e))
                state.error = f"Recommendation generation failed: {str(e)}"
                return state
    
    async def _format_response(self, state: AgentState) -> AgentState:
        """Format the final CFO response."""
        with tracer.start_as_current_span("ai_cfo.format_response"):
            try:
                # Compile comprehensive CFO report
                insights = state.metadata.get("insights", "")
                risk_summary = state.metadata.get("risk_assessment", {}).get("risk_summary", "")
                recommendations = state.metadata.get("recommendations", "")
                
                final_response = f"""# AI CFO Financial Analysis Report

## Executive Summary
{insights}

## Risk Assessment
{risk_summary}

## Strategic Recommendations
{recommendations}

## Industry Context
This analysis is tailored for the {self.industry} industry, incorporating relevant benchmarks and regulatory considerations.

---
*Report generated by AI CFO Agent on {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC*
*Analysis based on current financial data and industry benchmarks*
"""
                
                # Add final response to messages
                state.messages.append(AIMessage(content=final_response))
                
                state.completed_steps.append("format_response")
                state.current_step = "completed"
                
                logger.info(
                    "CFO analysis completed",
                    agent_id=self.agent_id,
                    report_length=len(final_response),
                )
                
                return state
                
            except Exception as e:
                logger.error("Response formatting failed", error=str(e))
                state.error = f"Response formatting failed: {str(e)}"
                return state
    
    def _load_industry_metrics(self) -> Dict[str, Any]:
        """Load industry-specific metrics and KPIs."""
        # This would typically load from a database or configuration
        industry_metrics = {
            "general": {
                "current_ratio": {"min": 1.0, "target": 2.0, "max": 3.0},
                "debt_to_equity": {"min": 0.0, "target": 0.5, "max": 1.0},
                "gross_margin": {"min": 0.2, "target": 0.4, "max": 0.6},
            },
            "healthcare": {
                "current_ratio": {"min": 1.5, "target": 2.5, "max": 4.0},
                "debt_to_equity": {"min": 0.0, "target": 0.3, "max": 0.6},
                "gross_margin": {"min": 0.3, "target": 0.5, "max": 0.7},
                "days_in_ar": {"min": 30, "target": 45, "max": 60},
            },
            "automotive": {
                "current_ratio": {"min": 1.0, "target": 1.5, "max": 2.5},
                "debt_to_equity": {"min": 0.2, "target": 0.6, "max": 1.2},
                "inventory_turnover": {"min": 6, "target": 12, "max": 20},
            },
            "pharmaceutical": {
                "current_ratio": {"min": 2.0, "target": 3.0, "max": 5.0},
                "rd_expense_ratio": {"min": 0.15, "target": 0.20, "max": 0.30},
                "gross_margin": {"min": 0.6, "target": 0.8, "max": 0.9},
            }
        }
        
        return industry_metrics.get(self.industry, industry_metrics["general"])
    
    def _load_industry_benchmarks(self) -> Dict[str, Any]:
        """Load industry benchmark data."""
        # This would typically load from external data sources
        return {
            "industry_avg_revenue_growth": 0.08,
            "industry_avg_profit_margin": 0.12,
            "industry_avg_roe": 0.15,
            "industry_avg_current_ratio": 2.1,
        }
    
    def _get_sample_transactions(self) -> List[Dict[str, Any]]:
        """Get sample transaction data."""
        return [
            {
                "amount": 15000.00,
                "type": "income",
                "category": "sales_revenue",
                "date": datetime.utcnow() - timedelta(days=5),
            },
            {
                "amount": 3500.00,
                "type": "expense", 
                "category": "operating_expenses",
                "date": datetime.utcnow() - timedelta(days=3),
            }
        ]
    
    def _get_sample_accounts(self) -> List[Dict[str, Any]]:
        """Get sample account data."""
        return [
            {
                "name": "Cash - Operating",
                "type": "asset",
                "balance": 125000.00,
            },
            {
                "name": "Accounts Receivable",
                "type": "asset", 
                "balance": 85000.00,
            }
        ]
    
    def _get_sample_invoices(self) -> List[Dict[str, Any]]:
        """Get sample invoice data."""
        return [
            {
                "amount": 25000.00,
                "status": "paid",
                "due_date": datetime.utcnow() - timedelta(days=10),
            },
            {
                "amount": 18000.00,
                "status": "pending",
                "due_date": datetime.utcnow() + timedelta(days=15),
            }
        ]
    
    def _get_sample_cash_flow(self) -> Dict[str, Any]:
        """Get sample cash flow data."""
        return {
            "operating_cash_flow": 45000.00,
            "investing_cash_flow": -12000.00,
            "financing_cash_flow": -8000.00,
            "net_cash_flow": 25000.00,
        }
    
    def _analyze_liquidity(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze liquidity metrics."""
        # Simplified liquidity analysis
        cash_balance = 125000.00  # From sample data
        current_liabilities = 45000.00  # Estimated
        
        current_ratio = cash_balance / current_liabilities if current_liabilities > 0 else 0
        
        return {
            "current_ratio": current_ratio,
            "cash_balance": cash_balance,
            "liquidity_score": "High" if current_ratio > 2.0 else "Medium" if current_ratio > 1.0 else "Low"
        }
    
    def _analyze_profitability(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze profitability metrics."""
        # Simplified profitability analysis
        revenue = 150000.00  # Estimated monthly revenue
        expenses = 120000.00  # Estimated monthly expenses
        
        gross_profit = revenue - expenses
        gross_margin = gross_profit / revenue if revenue > 0 else 0
        
        return {
            "gross_profit": gross_profit,
            "gross_margin": gross_margin,
            "profitability_trend": "Positive" if gross_margin > 0.2 else "Concerning"
        }
    
    def _analyze_efficiency(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze operational efficiency metrics."""
        return {
            "asset_turnover": 1.8,
            "inventory_turnover": 8.5,
            "efficiency_score": "Good"
        }
    
    def _analyze_leverage(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze leverage and debt metrics."""
        return {
            "debt_to_equity": 0.4,
            "interest_coverage": 12.5,
            "leverage_score": "Conservative"
        }
    
    def _compare_to_industry(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Compare metrics to industry benchmarks."""
        return {
            "vs_industry_revenue_growth": "Above Average",
            "vs_industry_margins": "In Line",
            "vs_industry_liquidity": "Above Average",
            "overall_ranking": "Upper Quartile"
        }
    
    def _assess_liquidity_risk(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Assess liquidity risk."""
        return {
            "risk_level": "Low",
            "key_factors": ["Strong cash position", "Stable cash flow"],
            "mitigation_actions": ["Monitor cash flow trends", "Maintain credit facilities"]
        }
    
    def _assess_credit_risk(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Assess credit risk."""
        return {
            "risk_level": "Medium",
            "key_factors": ["Concentration in key customers", "Industry cyclicality"],
            "mitigation_actions": ["Diversify customer base", "Implement credit monitoring"]
        }
    
    def _assess_operational_risk(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Assess operational risk."""
        return {
            "risk_level": "Medium",
            "key_factors": ["Key person dependency", "Process automation gaps"],
            "mitigation_actions": ["Cross-train staff", "Invest in automation"]
        }
    
    def _assess_market_risk(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Assess market risk."""
        return {
            "risk_level": "Medium",
            "key_factors": ["Economic uncertainty", "Competitive pressure"],
            "mitigation_actions": ["Scenario planning", "Market diversification"]
        }
    
    def _assess_compliance_risk(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Assess compliance risk."""
        return {
            "risk_level": "Low",
            "key_factors": ["Strong controls", "Regular audits"],
            "mitigation_actions": ["Maintain compliance program", "Regular training"]
        }
    
    def _format_analysis_for_llm(self, analysis_results: Dict[str, Any]) -> str:
        """Format analysis results for LLM consumption."""
        formatted = []
        for category, results in analysis_results.items():
            formatted.append(f"{category.replace('_', ' ').title()}:")
            for key, value in results.items():
                formatted.append(f"  - {key}: {value}")
            formatted.append("")
        
        return "\n".join(formatted)
    
    def _format_risks_for_llm(self, risk_assessment: Dict[str, Any]) -> str:
        """Format risk assessment for LLM consumption."""
        formatted = []
        for risk_type, assessment in risk_assessment.items():
            formatted.append(f"{risk_type.replace('_', ' ').title()}:")
            formatted.append(f"  Risk Level: {assessment['risk_level']}")
            formatted.append(f"  Key Factors: {', '.join(assessment['key_factors'])}")
            formatted.append(f"  Mitigation Actions: {', '.join(assessment['mitigation_actions'])}")
            formatted.append("")
        
        return "\n".join(formatted)
    
    async def _process_request(self, state: AgentState) -> AgentState:
        """Process a request using the AI CFO workflow.
        
        This method serves as the main entry point for the AI CFO agent's processing pipeline.
        It delegates to the specific workflow steps defined in the graph.
        
        Args:
            state: Current agent state
            
        Returns:
            Updated agent state
        """
        # The actual processing is handled by the graph workflow
        # This method is required by the BaseAgent abstract class
        # The graph will route through the appropriate workflow steps
        
        # For direct processing without the full graph, we can call analyze_request
        return await self._analyze_request(state)
    
    def get_capabilities(self) -> List[str]:
        """Get AI CFO agent capabilities."""
        return [
            "financial_analysis",
            "industry_benchmarking", 
            "risk_assessment",
            "strategic_recommendations",
            "cash_flow_analysis",
            "profitability_analysis",
            "liquidity_analysis",
            "compliance_monitoring",
            "investment_analysis",
            "scenario_planning"
        ]