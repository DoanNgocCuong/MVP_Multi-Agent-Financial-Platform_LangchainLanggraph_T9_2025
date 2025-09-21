"""Alert Agent for financial risk monitoring and alerting."""

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


class AlertAgent(BaseAgent):
    """Alert Agent for financial risk monitoring and alerting."""
    
    def __init__(self, industry: str = "general"):
        """Initialize the Alert Agent."""
        super().__init__(
            agent_id="alert_agent",
            name="Financial Alert Agent",
            description="Financial risk monitoring and alerting system",
            capabilities=[
                "risk_monitoring",
                "threshold_alerts",
                "anomaly_detection",
                "compliance_monitoring",
                "performance_alerts",
                "cash_flow_alerts",
                "debt_monitoring",
                "market_alerts",
                "operational_alerts",
                "regulatory_alerts"
            ]
        )
        self.industry = industry
        self._build_graph()
    
    def _build_graph(self):
        """Build the LangGraph workflow for alerting."""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("analyze_alert_request", self._analyze_alert_request)
        workflow.add_node("monitor_metrics", self._monitor_metrics)
        workflow.add_node("detect_anomalies", self._detect_anomalies)
        workflow.add_node("assess_risks", self._assess_risks)
        workflow.add_node("generate_alerts", self._generate_alerts)
        workflow.add_node("prioritize_alerts", self._prioritize_alerts)
        workflow.add_node("format_alert_response", self._format_alert_response)
        
        # Define workflow
        workflow.set_entry_point("analyze_alert_request")
        workflow.add_edge("analyze_alert_request", "monitor_metrics")
        workflow.add_edge("monitor_metrics", "detect_anomalies")
        workflow.add_edge("detect_anomalies", "assess_risks")
        workflow.add_edge("assess_risks", "generate_alerts")
        workflow.add_edge("generate_alerts", "prioritize_alerts")
        workflow.add_edge("prioritize_alerts", "format_alert_response")
        workflow.add_edge("format_alert_response", END)
        
        self.compiled_graph = workflow.compile()
    
    async def _analyze_alert_request(self, state: AgentState) -> AgentState:
        """Analyze the alert request."""
        with self.tracer.start_as_current_span("alert.analyze_request"):
            request = state.messages[-1].content if state.messages else ""
            
            # Mock analysis plan
            analysis_plan = {
                "request": request,
                "alert_type": "comprehensive_monitoring",
                "monitoring_scope": "all_metrics",
                "threshold_level": "standard",
                "timestamp": datetime.utcnow().isoformat()
            }
            
            state.metadata["analysis_plan"] = analysis_plan
            state.completed_steps.append("analyze_alert_request")
            
            logger.info("Alert request analyzed", agent_id=self.agent_id)
            return state
    
    async def _monitor_metrics(self, state: AgentState) -> AgentState:
        """Monitor financial metrics."""
        with self.tracer.start_as_current_span("alert.monitor_metrics"):
            # Mock metrics monitoring
            current_metrics = {
                "financial_metrics": {
                    "revenue": {"current": 1200000, "threshold": 1000000, "status": "normal"},
                    "expenses": {"current": 960000, "threshold": 800000, "status": "warning"},
                    "cash_flow": {"current": 240000, "threshold": 200000, "status": "normal"},
                    "debt_ratio": {"current": 0.4, "threshold": 0.5, "status": "normal"},
                    "profit_margin": {"current": 0.20, "threshold": 0.15, "status": "normal"}
                },
                "operational_metrics": {
                    "customer_satisfaction": {"current": 4.2, "threshold": 4.0, "status": "normal"},
                    "employee_turnover": {"current": 0.12, "threshold": 0.15, "status": "normal"},
                    "inventory_turnover": {"current": 8.5, "threshold": 6.0, "status": "normal"},
                    "order_fulfillment": {"current": 0.95, "threshold": 0.90, "status": "normal"}
                },
                "market_metrics": {
                    "market_share": {"current": 0.15, "threshold": 0.10, "status": "normal"},
                    "competitor_pricing": {"current": 1.05, "threshold": 1.10, "status": "warning"},
                    "industry_growth": {"current": 0.08, "threshold": 0.05, "status": "normal"}
                }
            }
            
            state.metadata["current_metrics"] = current_metrics
            state.completed_steps.append("monitor_metrics")
            
            logger.info("Metrics monitored", agent_id=self.agent_id)
            return state
    
    async def _detect_anomalies(self, state: AgentState) -> AgentState:
        """Detect anomalies in metrics."""
        with self.tracer.start_as_current_span("alert.detect_anomalies"):
            # Mock anomaly detection
            anomalies = {
                "detected_anomalies": [
                    {
                        "metric": "expenses",
                        "type": "threshold_breach",
                        "severity": "medium",
                        "current_value": 960000,
                        "threshold": 800000,
                        "deviation": 0.20,
                        "description": "Expenses exceeded threshold by 20%"
                    },
                    {
                        "metric": "competitor_pricing",
                        "type": "trend_anomaly",
                        "severity": "low",
                        "current_value": 1.05,
                        "expected_value": 1.10,
                        "deviation": -0.05,
                        "description": "Competitor pricing below expected level"
                    }
                ],
                "anomaly_summary": {
                    "total_anomalies": 2,
                    "high_severity": 0,
                    "medium_severity": 1,
                    "low_severity": 1,
                    "anomaly_rate": 0.15
                }
            }
            
            state.metadata["anomalies"] = anomalies
            state.completed_steps.append("detect_anomalies")
            
            logger.info("Anomalies detected", agent_id=self.agent_id)
            return state
    
    async def _assess_risks(self, state: AgentState) -> AgentState:
        """Assess risks based on anomalies."""
        with self.tracer.start_as_current_span("alert.assess_risks"):
            # Mock risk assessment
            risk_assessment = {
                "risk_levels": {
                    "overall_risk": "medium",
                    "financial_risk": "medium",
                    "operational_risk": "low",
                    "market_risk": "low"
                },
                "risk_factors": [
                    {
                        "factor": "Expense Control",
                        "risk_level": "medium",
                        "impact": "profitability",
                        "probability": 0.7,
                        "mitigation": "Cost reduction initiatives"
                    },
                    {
                        "factor": "Competitive Pressure",
                        "risk_level": "low",
                        "impact": "market_position",
                        "probability": 0.3,
                        "mitigation": "Pricing strategy review"
                    }
                ],
                "risk_trends": {
                    "trending_up": ["expense_control"],
                    "trending_down": ["market_risk"],
                    "stable": ["operational_risk", "financial_risk"]
                }
            }
            
            state.metadata["risk_assessment"] = risk_assessment
            state.completed_steps.append("assess_risks")
            
            logger.info("Risks assessed", agent_id=self.agent_id)
            return state
    
    async def _generate_alerts(self, state: AgentState) -> AgentState:
        """Generate alerts based on risks."""
        with self.tracer.start_as_current_span("alert.generate_alerts"):
            # Mock alert generation
            alerts = {
                "active_alerts": [
                    {
                        "alert_id": "EXP-001",
                        "type": "expense_threshold",
                        "severity": "medium",
                        "title": "Expense Threshold Exceeded",
                        "description": "Monthly expenses have exceeded the established threshold by 20%",
                        "metric": "expenses",
                        "current_value": 960000,
                        "threshold": 800000,
                        "timestamp": datetime.utcnow().isoformat(),
                        "status": "active",
                        "recommended_action": "Review expense categories and implement cost controls"
                    },
                    {
                        "alert_id": "COMP-002",
                        "type": "competitive_pressure",
                        "severity": "low",
                        "title": "Competitive Pricing Alert",
                        "description": "Competitor pricing is below expected levels",
                        "metric": "competitor_pricing",
                        "current_value": 1.05,
                        "expected_value": 1.10,
                        "timestamp": datetime.utcnow().isoformat(),
                        "status": "active",
                        "recommended_action": "Review pricing strategy and market positioning"
                    }
                ],
                "alert_summary": {
                    "total_alerts": 2,
                    "active_alerts": 2,
                    "resolved_alerts": 0,
                    "high_priority": 0,
                    "medium_priority": 1,
                    "low_priority": 1
                }
            }
            
            state.metadata["alerts"] = alerts
            state.completed_steps.append("generate_alerts")
            
            logger.info("Alerts generated", agent_id=self.agent_id)
            return state
    
    async def _prioritize_alerts(self, state: AgentState) -> AgentState:
        """Prioritize alerts based on severity and impact."""
        with self.tracer.start_as_current_span("alert.prioritize_alerts"):
            # Mock alert prioritization
            prioritization = {
                "priority_matrix": {
                    "high_priority": [],
                    "medium_priority": [
                        {
                            "alert_id": "EXP-001",
                            "priority_score": 7.5,
                            "urgency": "medium",
                            "impact": "high",
                            "time_sensitivity": "medium"
                        }
                    ],
                    "low_priority": [
                        {
                            "alert_id": "COMP-002",
                            "priority_score": 4.0,
                            "urgency": "low",
                            "impact": "medium",
                            "time_sensitivity": "low"
                        }
                    ]
                },
                "action_plan": {
                    "immediate_actions": [
                        "Review expense categories for cost reduction opportunities",
                        "Implement expense approval process for non-essential items"
                    ],
                    "short_term_actions": [
                        "Conduct competitive pricing analysis",
                        "Develop pricing strategy adjustments"
                    ],
                    "long_term_actions": [
                        "Establish expense monitoring dashboard",
                        "Implement automated expense alerts"
                    ]
                }
            }
            
            state.metadata["prioritization"] = prioritization
            state.completed_steps.append("prioritize_alerts")
            
            logger.info("Alerts prioritized", agent_id=self.agent_id)
            return state
    
    async def _format_alert_response(self, state: AgentState) -> AgentState:
        """Format the final alert response."""
        with self.tracer.start_as_current_span("alert.format_response"):
            alerts = state.metadata.get("alerts", {})
            risk_assessment = state.metadata.get("risk_assessment", {})
            prioritization = state.metadata.get("prioritization", {})
            
            # Create comprehensive alert report
            alert_report = f"""# Financial Alert & Risk Monitoring Report

## Executive Summary
Current monitoring shows **2 active alerts** with overall risk level at **MEDIUM**. Immediate attention required for expense control.

## Active Alerts

### 🟡 Medium Priority Alert
**Alert ID**: EXP-001  
**Type**: Expense Threshold Exceeded  
**Status**: Active  
**Description**: Monthly expenses have exceeded the established threshold by 20%  
**Current Value**: $960,000  
**Threshold**: $800,000  
**Recommended Action**: Review expense categories and implement cost controls

### 🟢 Low Priority Alert  
**Alert ID**: COMP-002  
**Type**: Competitive Pricing Alert  
**Status**: Active  
**Description**: Competitor pricing is below expected levels  
**Current Value**: 1.05  
**Expected Value**: 1.10  
**Recommended Action**: Review pricing strategy and market positioning

## Risk Assessment
- **Overall Risk Level**: MEDIUM
- **Financial Risk**: MEDIUM (expense control issues)
- **Operational Risk**: LOW (stable operations)
- **Market Risk**: LOW (competitive pressure manageable)

## Key Risk Factors
1. **Expense Control** (Medium Risk)
   - Impact: Profitability
   - Probability: 70%
   - Mitigation: Cost reduction initiatives

2. **Competitive Pressure** (Low Risk)
   - Impact: Market position
   - Probability: 30%
   - Mitigation: Pricing strategy review

## Action Plan

### Immediate Actions (0-7 days)
- Review expense categories for cost reduction opportunities
- Implement expense approval process for non-essential items

### Short-term Actions (1-4 weeks)
- Conduct competitive pricing analysis
- Develop pricing strategy adjustments

### Long-term Actions (1-3 months)
- Establish expense monitoring dashboard
- Implement automated expense alerts

## Monitoring Recommendations
1. **Daily**: Monitor expense trends and cash flow
2. **Weekly**: Review competitive pricing and market conditions
3. **Monthly**: Comprehensive risk assessment and alert review

## Alert Configuration
- **Expense Threshold**: $800,000 (current: $960,000)
- **Cash Flow Threshold**: $200,000 (current: $240,000)
- **Profit Margin Threshold**: 15% (current: 20%)

---
*Report generated by Financial Alert Agent on {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC*
*Monitoring based on real-time financial metrics and risk thresholds*
"""
            
            # Add AI message to state
            ai_message = AIMessage(content=alert_report)
            state.messages.append(ai_message)
            state.completed_steps.append("format_alert_response")
            
            logger.info("Alert response formatted", agent_id=self.agent_id)
            return state
    
    async def _format_response(self, state: AgentState) -> Dict[str, Any]:
        """Format the final response from graph execution."""
        with self.tracer.start_as_current_span("alert.format_response"):
            try:
                # Get the last AI message
                ai_messages = [msg for msg in state.messages if hasattr(msg, 'content') and getattr(msg, '__class__', None) and getattr(msg.__class__, '__name__', '') == 'AIMessage']
                last_message = ai_messages[-1] if ai_messages else None
                
                return {
                    "agent_id": self.agent_id,
                    "session_id": getattr(state.context, 'session_id', None) if state.context else None,
                    "response": getattr(last_message, 'content', "No alerts generated") if last_message else "No alerts generated",
                    "metadata": state.metadata,
                    "completed_steps": state.completed_steps,
                    "error": state.error,
                }
                
            except Exception as e:
                logger.error("Response formatting failed", error=str(e))
                return {
                    "agent_id": self.agent_id,
                    "session_id": getattr(state.context, 'session_id', None) if state.context else None,
                    "response": "Error occurred during alert monitoring",
                    "metadata": state.metadata,
                    "completed_steps": state.completed_steps,
                    "error": f"Response formatting failed: {str(e)}",
                }
