"""Financial Forecasting Agent for predictive analysis and trend forecasting."""

import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from uuid import uuid4

from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END

from ai_financial.core.base_agent import BaseAgent
from ai_financial.models.agent_models import AgentState, AgentContext
from ai_financial.core.logging import get_logger
from ai_financial.core.config import settings

logger = get_logger(__name__)


class ForecastingAgent(BaseAgent):
    """Financial Forecasting Agent for predictive analysis."""
    
    def __init__(self, industry: str = "general"):
        """Initialize the Forecasting Agent."""
        super().__init__(
            agent_id="forecasting_agent",
            name="Financial Forecasting Agent",
            description="Predictive financial analysis and forecasting",
            capabilities=[
                "financial_forecasting",
                "trend_analysis", 
                "scenario_planning",
                "revenue_projection",
                "expense_forecasting",
                "cash_flow_prediction",
                "risk_assessment",
                "market_analysis",
                "seasonal_analysis",
                "growth_modeling"
            ]
        )
        self.industry = industry
        self._build_graph()
    
    def _build_graph(self):
        """Build the LangGraph workflow for forecasting."""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("analyze_forecast_request", self._analyze_forecast_request)
        workflow.add_node("gather_historical_data", self._gather_historical_data)
        workflow.add_node("perform_trend_analysis", self._perform_trend_analysis)
        workflow.add_node("generate_forecasts", self._generate_forecasts)
        workflow.add_node("create_scenarios", self._create_scenarios)
        workflow.add_node("assess_forecast_risks", self._assess_forecast_risks)
        workflow.add_node("format_forecast_response", self._format_forecast_response)
        
        # Define workflow
        workflow.set_entry_point("analyze_forecast_request")
        workflow.add_edge("analyze_forecast_request", "gather_historical_data")
        workflow.add_edge("gather_historical_data", "perform_trend_analysis")
        workflow.add_edge("perform_trend_analysis", "generate_forecasts")
        workflow.add_edge("generate_forecasts", "create_scenarios")
        workflow.add_edge("create_scenarios", "assess_forecast_risks")
        workflow.add_edge("assess_forecast_risks", "format_forecast_response")
        workflow.add_edge("format_forecast_response", END)
        
        self.compiled_graph = workflow.compile()
    
    async def _analyze_forecast_request(self, state: AgentState) -> AgentState:
        """Analyze the forecasting request."""
        with self.tracer.start_as_current_span("forecasting.analyze_request"):
            request = state.messages[-1].content if state.messages else ""
            
            # Mock analysis plan
            analysis_plan = {
                "request": request,
                "forecast_type": "comprehensive",
                "time_horizon": "12_months",
                "methodology": "time_series_analysis",
                "confidence_level": 0.95,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            state.metadata["analysis_plan"] = analysis_plan
            state.completed_steps.append("analyze_forecast_request")
            
            logger.info("Forecast request analyzed", agent_id=self.agent_id)
            return state
    
    async def _gather_historical_data(self, state: AgentState) -> AgentState:
        """Gather historical financial data."""
        with self.tracer.start_as_current_span("forecasting.gather_data"):
            # Mock historical data
            historical_data = {
                "revenue_history": [
                    {"period": "2024-Q1", "value": 1000000, "growth": 0.05},
                    {"period": "2024-Q2", "value": 1100000, "growth": 0.10},
                    {"period": "2024-Q3", "value": 1200000, "growth": 0.09},
                    {"period": "2024-Q4", "value": 1300000, "growth": 0.08}
                ],
                "expense_history": [
                    {"period": "2024-Q1", "value": 800000, "ratio": 0.80},
                    {"period": "2024-Q2", "value": 880000, "ratio": 0.80},
                    {"period": "2024-Q3", "value": 960000, "ratio": 0.80},
                    {"period": "2024-Q4", "value": 1040000, "ratio": 0.80}
                ],
                "cash_flow_history": [
                    {"period": "2024-Q1", "operating": 200000, "investing": -50000, "financing": -30000},
                    {"period": "2024-Q2", "operating": 220000, "investing": -60000, "financing": -40000},
                    {"period": "2024-Q3", "operating": 240000, "investing": -70000, "financing": -50000},
                    {"period": "2024-Q4", "operating": 260000, "investing": -80000, "financing": -60000}
                ]
            }
            
            state.metadata["historical_data"] = historical_data
            state.completed_steps.append("gather_historical_data")
            
            logger.info("Historical data gathered", agent_id=self.agent_id)
            return state
    
    async def _perform_trend_analysis(self, state: AgentState) -> AgentState:
        """Perform trend analysis on historical data."""
        with self.tracer.start_as_current_span("forecasting.trend_analysis"):
            # Mock trend analysis
            trend_analysis = {
                "revenue_trends": {
                    "average_growth_rate": 0.08,
                    "trend_direction": "increasing",
                    "seasonality": "moderate",
                    "volatility": "low"
                },
                "expense_trends": {
                    "average_ratio": 0.80,
                    "trend_direction": "stable",
                    "cost_efficiency": "improving"
                },
                "cash_flow_trends": {
                    "operating_cash_flow_growth": 0.10,
                    "cash_flow_stability": "high",
                    "liquidity_trend": "improving"
                },
                "market_indicators": {
                    "industry_growth": 0.06,
                    "economic_outlook": "positive",
                    "competitive_pressure": "moderate"
                }
            }
            
            state.metadata["trend_analysis"] = trend_analysis
            state.completed_steps.append("perform_trend_analysis")
            
            logger.info("Trend analysis completed", agent_id=self.agent_id)
            return state
    
    async def _generate_forecasts(self, state: AgentState) -> AgentState:
        """Generate financial forecasts."""
        with self.tracer.start_as_current_span("forecasting.generate_forecasts"):
            # Mock forecasts
            forecasts = {
                "revenue_forecast": [
                    {"period": "2025-Q1", "value": 1404000, "growth": 0.08, "confidence": 0.85},
                    {"period": "2025-Q2", "value": 1516320, "growth": 0.08, "confidence": 0.80},
                    {"period": "2025-Q3", "value": 1637626, "growth": 0.08, "confidence": 0.75},
                    {"period": "2025-Q4", "value": 1768636, "growth": 0.08, "confidence": 0.70}
                ],
                "expense_forecast": [
                    {"period": "2025-Q1", "value": 1123200, "ratio": 0.80, "confidence": 0.90},
                    {"period": "2025-Q2", "value": 1213056, "ratio": 0.80, "confidence": 0.85},
                    {"period": "2025-Q3", "value": 1310100, "ratio": 0.80, "confidence": 0.80},
                    {"period": "2025-Q4", "value": 1414909, "ratio": 0.80, "confidence": 0.75}
                ],
                "cash_flow_forecast": [
                    {"period": "2025-Q1", "operating": 280800, "investing": -90000, "financing": -70000},
                    {"period": "2025-Q2", "operating": 303264, "investing": -100000, "financing": -80000},
                    {"period": "2025-Q3", "operating": 327525, "investing": -110000, "financing": -90000},
                    {"period": "2025-Q4", "operating": 353727, "investing": -120000, "financing": -100000}
                ],
                "key_metrics": {
                    "projected_annual_revenue": 6326602,
                    "projected_annual_expenses": 5061281,
                    "projected_net_income": 1265321,
                    "projected_cash_flow": 1265316
                }
            }
            
            state.metadata["forecasts"] = forecasts
            state.completed_steps.append("generate_forecasts")
            
            logger.info("Forecasts generated", agent_id=self.agent_id)
            return state
    
    async def _create_scenarios(self, state: AgentState) -> AgentState:
        """Create different forecast scenarios."""
        with self.tracer.start_as_current_span("forecasting.create_scenarios"):
            # Mock scenarios
            scenarios = {
                "optimistic_scenario": {
                    "description": "High growth market conditions",
                    "revenue_multiplier": 1.2,
                    "probability": 0.25,
                    "key_assumptions": ["Market expansion", "New product success", "Economic boom"]
                },
                "base_scenario": {
                    "description": "Current trend continuation",
                    "revenue_multiplier": 1.0,
                    "probability": 0.50,
                    "key_assumptions": ["Stable market", "Normal competition", "Steady growth"]
                },
                "pessimistic_scenario": {
                    "description": "Economic downturn impact",
                    "revenue_multiplier": 0.8,
                    "probability": 0.25,
                    "key_assumptions": ["Market contraction", "Increased competition", "Economic recession"]
                }
            }
            
            state.metadata["scenarios"] = scenarios
            state.completed_steps.append("create_scenarios")
            
            logger.info("Scenarios created", agent_id=self.agent_id)
            return state
    
    async def _assess_forecast_risks(self, state: AgentState) -> AgentState:
        """Assess risks associated with forecasts."""
        with self.tracer.start_as_current_span("forecasting.assess_risks"):
            # Mock risk assessment
            risk_assessment = {
                "forecast_risks": {
                    "market_risk": {
                        "level": "medium",
                        "impact": "revenue_volatility",
                        "mitigation": "diversification"
                    },
                    "operational_risk": {
                        "level": "low",
                        "impact": "cost_increases",
                        "mitigation": "efficiency_improvements"
                    },
                    "financial_risk": {
                        "level": "low",
                        "impact": "cash_flow_disruption",
                        "mitigation": "credit_facilities"
                    }
                },
                "sensitivity_analysis": {
                    "revenue_sensitivity": 0.15,
                    "cost_sensitivity": 0.10,
                    "market_sensitivity": 0.20
                },
                "confidence_intervals": {
                    "revenue_ci_95": [5800000, 6900000],
                    "expense_ci_95": [4600000, 5500000],
                    "cash_flow_ci_95": [1000000, 1500000]
                }
            }
            
            state.metadata["risk_assessment"] = risk_assessment
            state.completed_steps.append("assess_forecast_risks")
            
            logger.info("Forecast risks assessed", agent_id=self.agent_id)
            return state
    
    async def _format_forecast_response(self, state: AgentState) -> AgentState:
        """Format the final forecast response."""
        with self.tracer.start_as_current_span("forecasting.format_response"):
            forecasts = state.metadata.get("forecasts", {})
            scenarios = state.metadata.get("scenarios", {})
            risk_assessment = state.metadata.get("risk_assessment", {})
            
            # Create comprehensive forecast report
            forecast_report = f"""# Financial Forecasting Report

## Executive Summary
Based on historical data analysis and trend modeling, we project strong financial performance for the next 12 months.

## Revenue Forecast
- **Q1 2025**: $1,404,000 (8% growth)
- **Q2 2025**: $1,516,320 (8% growth)  
- **Q3 2025**: $1,637,626 (8% growth)
- **Q4 2025**: $1,768,636 (8% growth)
- **Annual Total**: $6,326,602

## Expense Forecast
- **Q1 2025**: $1,123,200 (80% ratio)
- **Q2 2025**: $1,213,056 (80% ratio)
- **Q3 2025**: $1,310,100 (80% ratio)
- **Q4 2025**: $1,414,909 (80% ratio)
- **Annual Total**: $5,061,281

## Cash Flow Projections
- **Operating Cash Flow**: $1,265,316 annually
- **Net Cash Position**: Strong liquidity maintained
- **Investment Capacity**: $420,000 annually

## Scenario Analysis
### Optimistic Scenario (25% probability)
- Revenue: +20% above base case
- Key drivers: Market expansion, new products

### Base Scenario (50% probability)  
- Revenue: Current trend continuation
- Most likely outcome

### Pessimistic Scenario (25% probability)
- Revenue: -20% below base case
- Risk factors: Economic downturn, competition

## Risk Assessment
- **Market Risk**: Medium - Revenue volatility possible
- **Operational Risk**: Low - Stable cost structure
- **Financial Risk**: Low - Strong cash position

## Key Recommendations
1. **Monitor Market Conditions**: Track industry trends closely
2. **Maintain Cost Discipline**: Keep expense ratio at 80%
3. **Invest in Growth**: Use strong cash flow for expansion
4. **Risk Mitigation**: Maintain credit facilities for contingencies

## Confidence Levels
- **Q1-Q2 Forecasts**: 80-85% confidence
- **Q3-Q4 Forecasts**: 70-75% confidence
- **Annual Projections**: 75% confidence

---
*Report generated by Financial Forecasting Agent on {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC*
*Forecasts based on historical data and trend analysis*
"""
            
            # Add AI message to state
            ai_message = AIMessage(content=forecast_report)
            state.messages.append(ai_message)
            state.completed_steps.append("format_forecast_response")
            
            logger.info("Forecast response formatted", agent_id=self.agent_id)
            return state
    
    async def _format_response(self, state: AgentState) -> Dict[str, Any]:
        """Format the final response from graph execution."""
        with self.tracer.start_as_current_span("forecasting.format_response"):
            try:
                # Get the last AI message
                ai_messages = [msg for msg in state.messages if hasattr(msg, 'content') and getattr(msg, '__class__', None) and getattr(msg.__class__, '__name__', '') == 'AIMessage']
                last_message = ai_messages[-1] if ai_messages else None
                
                return {
                    "agent_id": self.agent_id,
                    "session_id": getattr(state.context, 'session_id', None) if state.context else None,
                    "response": getattr(last_message, 'content', "No forecast generated") if last_message else "No forecast generated",
                    "metadata": state.metadata,
                    "completed_steps": state.completed_steps,
                    "error": state.error,
                }
                
            except Exception as e:
                logger.error("Response formatting failed", error=str(e))
                return {
                    "agent_id": self.agent_id,
                    "session_id": getattr(state.context, 'session_id', None) if state.context else None,
                    "response": "Error occurred during forecasting",
                    "metadata": state.metadata,
                    "completed_steps": state.completed_steps,
                    "error": f"Response formatting failed: {str(e)}",
                }
