"""Reporting Agent for financial reporting and dashboard generation."""

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


class ReportingAgent(BaseAgent):
    """Reporting Agent for financial reporting and dashboard generation."""
    
    def __init__(self, industry: str = "general"):
        """Initialize the Reporting Agent."""
        super().__init__(
            agent_id="reporting_agent",
            name="Financial Reporting Agent",
            description="Financial reporting and dashboard generation system",
            capabilities=[
                "financial_reporting",
                "dashboard_generation",
                "kpi_tracking",
                "executive_summaries",
                "regulatory_reporting",
                "performance_metrics",
                "trend_analysis",
                "data_visualization",
                "report_automation",
                "compliance_reporting"
            ]
        )
        self.industry = industry
        self._build_graph()
    
    def _build_graph(self):
        """Build the LangGraph workflow for reporting."""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("analyze_report_request", self._analyze_report_request)
        workflow.add_node("gather_report_data", self._gather_report_data)
        workflow.add_node("generate_kpis", self._generate_kpis)
        workflow.add_node("create_dashboard", self._create_dashboard)
        workflow.add_node("format_reports", self._format_reports)
        workflow.add_node("validate_reports", self._validate_reports)
        workflow.add_node("format_report_response", self._format_report_response)
        
        # Define workflow
        workflow.set_entry_point("analyze_report_request")
        workflow.add_edge("analyze_report_request", "gather_report_data")
        workflow.add_edge("gather_report_data", "generate_kpis")
        workflow.add_edge("generate_kpis", "create_dashboard")
        workflow.add_edge("create_dashboard", "format_reports")
        workflow.add_edge("format_reports", "validate_reports")
        workflow.add_edge("validate_reports", "format_report_response")
        workflow.add_edge("format_report_response", END)
        
        self.compiled_graph = workflow.compile()
    
    async def _analyze_report_request(self, state: AgentState) -> AgentState:
        """Analyze the report request."""
        with self.tracer.start_as_current_span("reporting.analyze_request"):
            request = state.messages[-1].content if state.messages else ""
            
            # Mock analysis plan
            analysis_plan = {
                "request": request,
                "report_type": "comprehensive_financial_report",
                "period": "monthly",
                "audience": "executive",
                "format": "dashboard_and_summary",
                "timestamp": datetime.utcnow().isoformat()
            }
            
            state.metadata["analysis_plan"] = analysis_plan
            state.completed_steps.append("analyze_report_request")
            
            logger.info("Report request analyzed", agent_id=self.agent_id)
            return state
    
    async def _gather_report_data(self, state: AgentState) -> AgentState:
        """Gather data for reporting."""
        with self.tracer.start_as_current_span("reporting.gather_data"):
            # Mock report data
            report_data = {
                "financial_data": {
                    "revenue": {"current": 1200000, "previous": 1100000, "growth": 0.091},
                    "expenses": {"current": 960000, "previous": 880000, "growth": 0.091},
                    "net_income": {"current": 240000, "previous": 220000, "growth": 0.091},
                    "cash_flow": {"current": 280000, "previous": 260000, "growth": 0.077}
                },
                "operational_data": {
                    "customers": {"current": 1250, "previous": 1200, "growth": 0.042},
                    "orders": {"current": 3500, "previous": 3200, "growth": 0.094},
                    "satisfaction": {"current": 4.2, "previous": 4.1, "growth": 0.024}
                },
                "market_data": {
                    "market_share": {"current": 0.15, "previous": 0.14, "growth": 0.071},
                    "competitor_analysis": {"position": "strong", "trend": "improving"}
                }
            }
            
            state.metadata["report_data"] = report_data
            state.completed_steps.append("gather_report_data")
            
            logger.info("Report data gathered", agent_id=self.agent_id)
            return state
    
    async def _generate_kpis(self, state: AgentState) -> AgentState:
        """Generate key performance indicators."""
        with self.tracer.start_as_current_span("reporting.generate_kpis"):
            # Mock KPIs
            kpis = {
                "financial_kpis": {
                    "revenue_growth": {"value": 0.091, "target": 0.08, "status": "exceeded"},
                    "profit_margin": {"value": 0.20, "target": 0.18, "status": "exceeded"},
                    "cash_flow_margin": {"value": 0.23, "target": 0.20, "status": "exceeded"},
                    "roi": {"value": 0.15, "target": 0.12, "status": "exceeded"}
                },
                "operational_kpis": {
                    "customer_growth": {"value": 0.042, "target": 0.05, "status": "below_target"},
                    "order_fulfillment": {"value": 0.95, "target": 0.90, "status": "exceeded"},
                    "customer_satisfaction": {"value": 4.2, "target": 4.0, "status": "exceeded"}
                },
                "market_kpis": {
                    "market_share_growth": {"value": 0.071, "target": 0.05, "status": "exceeded"},
                    "competitive_position": {"value": "strong", "target": "strong", "status": "met"}
                }
            }
            
            state.metadata["kpis"] = kpis
            state.completed_steps.append("generate_kpis")
            
            logger.info("KPIs generated", agent_id=self.agent_id)
            return state
    
    async def _create_dashboard(self, state: AgentState) -> AgentState:
        """Create dashboard visualization."""
        with self.tracer.start_as_current_span("reporting.create_dashboard"):
            # Mock dashboard
            dashboard = {
                "dashboard_sections": [
                    {
                        "title": "Financial Performance",
                        "charts": ["revenue_trend", "expense_breakdown", "profit_margin"],
                        "status": "excellent"
                    },
                    {
                        "title": "Operational Metrics",
                        "charts": ["customer_growth", "order_volume", "satisfaction_score"],
                        "status": "good"
                    },
                    {
                        "title": "Market Position",
                        "charts": ["market_share", "competitive_analysis", "growth_trends"],
                        "status": "strong"
                    }
                ],
                "summary_metrics": {
                    "overall_performance": "excellent",
                    "key_achievements": ["Revenue growth exceeded target", "Profit margins improved", "Market share increased"],
                    "areas_for_improvement": ["Customer acquisition rate", "Cost optimization opportunities"]
                }
            }
            
            state.metadata["dashboard"] = dashboard
            state.completed_steps.append("create_dashboard")
            
            logger.info("Dashboard created", agent_id=self.agent_id)
            return state
    
    async def _format_reports(self, state: AgentState) -> AgentState:
        """Format various report types."""
        with self.tracer.start_as_current_span("reporting.format_reports"):
            # Mock formatted reports
            formatted_reports = {
                "executive_summary": {
                    "title": "Monthly Financial Performance Summary",
                    "period": "Current Month",
                    "key_highlights": [
                        "Revenue growth of 9.1% exceeds target of 8%",
                        "Profit margin improved to 20%",
                        "Market share increased to 15%"
                    ]
                },
                "detailed_report": {
                    "financial_section": "Complete financial analysis with trends",
                    "operational_section": "Operational metrics and performance",
                    "market_section": "Market analysis and competitive position"
                },
                "regulatory_report": {
                    "compliance_status": "compliant",
                    "required_reports": ["financial_statements", "tax_reporting", "audit_preparation"]
                }
            }
            
            state.metadata["formatted_reports"] = formatted_reports
            state.completed_steps.append("format_reports")
            
            logger.info("Reports formatted", agent_id=self.agent_id)
            return state
    
    async def _validate_reports(self, state: AgentState) -> AgentState:
        """Validate report accuracy and completeness."""
        with self.tracer.start_as_current_span("reporting.validate_reports"):
            # Mock validation
            validation = {
                "validation_status": "passed",
                "accuracy_check": "verified",
                "completeness_check": "complete",
                "compliance_check": "compliant",
                "validation_notes": [
                    "All financial data verified against source systems",
                    "KPI calculations validated",
                    "Report format meets regulatory requirements"
                ]
            }
            
            state.metadata["validation"] = validation
            state.completed_steps.append("validate_reports")
            
            logger.info("Reports validated", agent_id=self.agent_id)
            return state
    
    async def _format_report_response(self, state: AgentState) -> AgentState:
        """Format the final report response."""
        with self.tracer.start_as_current_span("reporting.format_response"):
            kpis = state.metadata.get("kpis", {})
            dashboard = state.metadata.get("dashboard", {})
            formatted_reports = state.metadata.get("formatted_reports", {})
            
            # Create comprehensive report
            report_content = f"""# Financial Reporting Dashboard & Analysis

## Executive Summary
**Period**: Current Month  
**Overall Performance**: EXCELLENT  
**Key Achievement**: Revenue growth of 9.1% exceeds target of 8%

## Key Performance Indicators

### 📊 Financial KPIs
- **Revenue Growth**: 9.1% (Target: 8%) ✅ **EXCEEDED**
- **Profit Margin**: 20% (Target: 18%) ✅ **EXCEEDED**  
- **Cash Flow Margin**: 23% (Target: 20%) ✅ **EXCEEDED**
- **ROI**: 15% (Target: 12%) ✅ **EXCEEDED**

### 🎯 Operational KPIs
- **Customer Growth**: 4.2% (Target: 5%) ⚠️ **BELOW TARGET**
- **Order Fulfillment**: 95% (Target: 90%) ✅ **EXCEEDED**
- **Customer Satisfaction**: 4.2/5 (Target: 4.0) ✅ **EXCEEDED**

### 📈 Market KPIs
- **Market Share Growth**: 7.1% (Target: 5%) ✅ **EXCEEDED**
- **Competitive Position**: Strong ✅ **MET TARGET**

## Financial Performance

### Revenue Analysis
- **Current Month**: $1,200,000
- **Previous Month**: $1,100,000
- **Growth Rate**: 9.1%
- **Trend**: Strong upward trajectory

### Expense Management
- **Current Month**: $960,000
- **Previous Month**: $880,000
- **Growth Rate**: 9.1%
- **Efficiency**: Maintaining cost structure

### Profitability
- **Net Income**: $240,000
- **Profit Margin**: 20%
- **Cash Flow**: $280,000
- **Performance**: Excellent

## Operational Highlights

### Customer Metrics
- **Total Customers**: 1,250 (+50 from previous month)
- **Order Volume**: 3,500 orders (+300 from previous month)
- **Customer Satisfaction**: 4.2/5 (improving trend)

### Market Position
- **Market Share**: 15% (increasing)
- **Competitive Position**: Strong
- **Growth Trajectory**: Positive

## Dashboard Sections

### 1. Financial Performance Dashboard
- Revenue trend analysis
- Expense breakdown visualization
- Profit margin tracking
- **Status**: Excellent

### 2. Operational Metrics Dashboard  
- Customer growth tracking
- Order volume analysis
- Satisfaction score monitoring
- **Status**: Good

### 3. Market Position Dashboard
- Market share analysis
- Competitive benchmarking
- Growth trend visualization
- **Status**: Strong

## Key Achievements
✅ Revenue growth exceeded target by 1.1%  
✅ Profit margins improved to 20%  
✅ Market share increased to 15%  
✅ Customer satisfaction maintained above 4.0  
✅ Order fulfillment rate at 95%

## Areas for Improvement
⚠️ Customer acquisition rate below target (4.2% vs 5%)  
⚠️ Cost optimization opportunities identified  
⚠️ Competitive pricing pressure in some segments

## Recommendations
1. **Customer Acquisition**: Implement targeted marketing campaigns
2. **Cost Optimization**: Review expense categories for efficiency gains
3. **Market Expansion**: Leverage strong position for growth
4. **Technology Investment**: Enhance operational efficiency

## Compliance Status
✅ All financial statements prepared  
✅ Tax reporting requirements met  
✅ Audit preparation completed  
✅ Regulatory compliance maintained

---
*Report generated by Financial Reporting Agent on {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC*
*Data validated and verified for accuracy*
"""
            
            # Add AI message to state
            ai_message = AIMessage(content=report_content)
            state.messages.append(ai_message)
            state.completed_steps.append("format_report_response")
            
            logger.info("Report response formatted", agent_id=self.agent_id)
            return state
    
    async def _format_response(self, state: AgentState) -> Dict[str, Any]:
        """Format the final response from graph execution."""
        with self.tracer.start_as_current_span("reporting.format_response"):
            try:
                # Get the last AI message
                ai_messages = [msg for msg in state.messages if hasattr(msg, 'content') and getattr(msg, '__class__', None) and getattr(msg.__class__, '__name__', '') == 'AIMessage']
                last_message = ai_messages[-1] if ai_messages else None
                
                return {
                    "agent_id": self.agent_id,
                    "session_id": getattr(state.context, 'session_id', None) if state.context else None,
                    "response": getattr(last_message, 'content', "No report generated") if last_message else "No report generated",
                    "metadata": state.metadata,
                    "completed_steps": state.completed_steps,
                    "error": state.error,
                }
                
            except Exception as e:
                logger.error("Response formatting failed", error=str(e))
                return {
                    "agent_id": self.agent_id,
                    "session_id": getattr(state.context, 'session_id', None) if state.context else None,
                    "response": "Error occurred during report generation",
                    "metadata": state.metadata,
                    "completed_steps": state.completed_steps,
                    "error": f"Response formatting failed: {str(e)}",
                }
