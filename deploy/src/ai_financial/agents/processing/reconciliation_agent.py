"""Reconciliation Agent for financial reconciliation and matching."""

import asyncio
from datetime import datetime
from typing import Dict, Any, List, Optional
from uuid import uuid4

from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END

from ai_financial.core.base_agent import BaseAgent
from ai_financial.models.agent_models import AgentState, AgentContext
from ai_financial.core.logging import get_logger

logger = get_logger(__name__)


class ReconciliationAgent(BaseAgent):
    """Reconciliation Agent for financial reconciliation and matching."""
    
    def __init__(self, industry: str = "general"):
        """Initialize the Reconciliation Agent."""
        super().__init__(
            agent_id="reconciliation_agent",
            name="Financial Reconciliation Agent",
            description="Financial reconciliation and matching system",
            capabilities=[
                "bank_reconciliation",
                "account_matching",
                "variance_analysis",
                "exception_handling",
                "automated_matching",
                "manual_review",
                "discrepancy_resolution",
                "audit_trail"
            ]
        )
        self.industry = industry
        self._build_graph()
    
    def _build_graph(self):
        """Build the LangGraph workflow for reconciliation."""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("analyze_reconciliation_request", self._analyze_reconciliation_request)
        workflow.add_node("load_data", self._load_data)
        workflow.add_node("perform_matching", self._perform_matching)
        workflow.add_node("identify_discrepancies", self._identify_discrepancies)
        workflow.add_node("resolve_exceptions", self._resolve_exceptions)
        workflow.add_node("generate_reconciliation_report", self._generate_reconciliation_report)
        workflow.add_node("format_reconciliation_response", self._format_reconciliation_response)
        
        # Define workflow
        workflow.set_entry_point("analyze_reconciliation_request")
        workflow.add_edge("analyze_reconciliation_request", "load_data")
        workflow.add_edge("load_data", "perform_matching")
        workflow.add_edge("perform_matching", "identify_discrepancies")
        workflow.add_edge("identify_discrepancies", "resolve_exceptions")
        workflow.add_edge("resolve_exceptions", "generate_reconciliation_report")
        workflow.add_edge("generate_reconciliation_report", "format_reconciliation_response")
        workflow.add_edge("format_reconciliation_response", END)
        
        self.compiled_graph = workflow.compile()
    
    async def _analyze_reconciliation_request(self, state: AgentState) -> AgentState:
        """Analyze the reconciliation request."""
        with self.tracer.start_as_current_span("reconciliation.analyze_request"):
            request = state.messages[-1].content if state.messages else ""
            
            analysis_plan = {
                "request": request,
                "reconciliation_type": "bank_reconciliation",
                "period": "current_month",
                "accounts": ["checking", "savings", "credit"],
                "matching_criteria": ["amount", "date", "reference"],
                "timestamp": datetime.utcnow().isoformat()
            }
            
            state.metadata["analysis_plan"] = analysis_plan
            state.completed_steps.append("analyze_reconciliation_request")
            
            logger.info("Reconciliation request analyzed", agent_id=self.agent_id)
            return state
    
    async def _load_data(self, state: AgentState) -> AgentState:
        """Load reconciliation data."""
        with self.tracer.start_as_current_span("reconciliation.load_data"):
            # Mock data loading
            loaded_data = {
                "bank_statements": {
                    "checking": {"transactions": 150, "total_amount": 125000},
                    "savings": {"transactions": 25, "total_amount": 50000},
                    "credit": {"transactions": 80, "total_amount": 25000}
                },
                "general_ledger": {
                    "cash_accounts": {"transactions": 200, "total_amount": 175000},
                    "bank_accounts": {"transactions": 180, "total_amount": 170000}
                },
                "data_quality": "high",
                "load_status": "success"
            }
            
            state.metadata["loaded_data"] = loaded_data
            state.completed_steps.append("load_data")
            
            logger.info("Data loaded", agent_id=self.agent_id)
            return state
    
    async def _perform_matching(self, state: AgentState) -> AgentState:
        """Perform automated matching."""
        with self.tracer.start_as_current_span("reconciliation.perform_matching"):
            # Mock matching results
            matching_results = {
                "matched_transactions": {
                    "exact_matches": 180,
                    "fuzzy_matches": 15,
                    "manual_matches": 5,
                    "total_matched": 200
                },
                "unmatched_transactions": {
                    "bank_unmatched": 5,
                    "ledger_unmatched": 8,
                    "total_unmatched": 13
                },
                "matching_accuracy": 0.94,
                "matching_status": "completed"
            }
            
            state.metadata["matching_results"] = matching_results
            state.completed_steps.append("perform_matching")
            
            logger.info("Matching completed", agent_id=self.agent_id)
            return state
    
    async def _identify_discrepancies(self, state: AgentState) -> AgentState:
        """Identify discrepancies and exceptions."""
        with self.tracer.start_as_current_span("reconciliation.identify_discrepancies"):
            # Mock discrepancy identification
            discrepancies = {
                "discrepancy_summary": {
                    "total_discrepancies": 13,
                    "amount_discrepancies": 8,
                    "date_discrepancies": 3,
                    "reference_discrepancies": 2
                },
                "exception_details": [
                    {
                        "type": "amount_mismatch",
                        "bank_amount": 1250.00,
                        "ledger_amount": 1200.00,
                        "difference": 50.00,
                        "status": "unresolved"
                    },
                    {
                        "type": "missing_transaction",
                        "bank_reference": "TXN-001",
                        "ledger_status": "missing",
                        "amount": 500.00,
                        "status": "unresolved"
                    }
                ],
                "discrepancy_analysis": {
                    "high_priority": 3,
                    "medium_priority": 7,
                    "low_priority": 3
                }
            }
            
            state.metadata["discrepancies"] = discrepancies
            state.completed_steps.append("identify_discrepancies")
            
            logger.info("Discrepancies identified", agent_id=self.agent_id)
            return state
    
    async def _resolve_exceptions(self, state: AgentState) -> AgentState:
        """Resolve exceptions and discrepancies."""
        with self.tracer.start_as_current_span("reconciliation.resolve_exceptions"):
            # Mock exception resolution
            resolution_results = {
                "resolved_exceptions": {
                    "automatically_resolved": 8,
                    "manually_resolved": 3,
                    "total_resolved": 11
                },
                "remaining_exceptions": {
                    "unresolved": 2,
                    "requires_manual_review": 2
                },
                "resolution_summary": {
                    "resolution_rate": 0.85,
                    "auto_resolution_rate": 0.62,
                    "manual_resolution_rate": 0.23
                }
            }
            
            state.metadata["resolution_results"] = resolution_results
            state.completed_steps.append("resolve_exceptions")
            
            logger.info("Exceptions resolved", agent_id=self.agent_id)
            return state
    
    async def _generate_reconciliation_report(self, state: AgentState) -> AgentState:
        """Generate reconciliation report."""
        with self.tracer.start_as_current_span("reconciliation.generate_report"):
            # Mock report generation
            reconciliation_report = {
                "report_summary": {
                    "reconciliation_status": "completed",
                    "total_transactions": 213,
                    "matched_transactions": 200,
                    "unmatched_transactions": 13,
                    "reconciliation_rate": 0.94
                },
                "account_summaries": {
                    "checking": {"matched": 140, "unmatched": 3, "status": "reconciled"},
                    "savings": {"matched": 25, "unmatched": 0, "status": "reconciled"},
                    "credit": {"matched": 35, "unmatched": 10, "status": "partial"}
                },
                "variance_analysis": {
                    "total_variance": 150.00,
                    "explained_variance": 100.00,
                    "unexplained_variance": 50.00
                }
            }
            
            state.metadata["reconciliation_report"] = reconciliation_report
            state.completed_steps.append("generate_reconciliation_report")
            
            logger.info("Reconciliation report generated", agent_id=self.agent_id)
            return state
    
    async def _format_reconciliation_response(self, state: AgentState) -> AgentState:
        """Format the final reconciliation response."""
        with self.tracer.start_as_current_span("reconciliation.format_response"):
            matching_results = state.metadata.get("matching_results", {})
            discrepancies = state.metadata.get("discrepancies", {})
            resolution_results = state.metadata.get("resolution_results", {})
            reconciliation_report = state.metadata.get("reconciliation_report", {})
            
            # Create comprehensive reconciliation report
            reconciliation_content = f"""# Financial Reconciliation Report

## Reconciliation Summary
**Status**: ✅ **COMPLETED**  
**Total Transactions**: 213  
**Matched Transactions**: 200 (94%)  
**Unmatched Transactions**: 13 (6%)  
**Reconciliation Rate**: 94%

## Account Reconciliation Results

### Checking Account
- **Matched**: 140 transactions ✅
- **Unmatched**: 3 transactions ⚠️
- **Status**: Reconciled

### Savings Account  
- **Matched**: 25 transactions ✅
- **Unmatched**: 0 transactions ✅
- **Status**: Fully Reconciled

### Credit Account
- **Matched**: 35 transactions ✅
- **Unmatched**: 10 transactions ⚠️
- **Status**: Partially Reconciled

## Matching Analysis

### Automated Matching Results
- **Exact Matches**: 180 transactions ✅
- **Fuzzy Matches**: 15 transactions ✅
- **Manual Matches**: 5 transactions ✅
- **Total Matched**: 200 transactions
- **Matching Accuracy**: 94%

### Unmatched Transactions
- **Bank Unmatched**: 5 transactions
- **Ledger Unmatched**: 8 transactions
- **Total Unmatched**: 13 transactions

## Discrepancy Analysis

### Discrepancy Summary
- **Total Discrepancies**: 13
- **Amount Discrepancies**: 8
- **Date Discrepancies**: 3
- **Reference Discrepancies**: 2

### Priority Breakdown
- **High Priority**: 3 discrepancies
- **Medium Priority**: 7 discrepancies
- **Low Priority**: 3 discrepancies

## Exception Resolution

### Resolution Results
- **Automatically Resolved**: 8 exceptions ✅
- **Manually Resolved**: 3 exceptions ✅
- **Total Resolved**: 11 exceptions
- **Remaining Unresolved**: 2 exceptions ⚠️

### Resolution Rates
- **Overall Resolution Rate**: 85%
- **Auto Resolution Rate**: 62%
- **Manual Resolution Rate**: 23%

## Variance Analysis

### Financial Variances
- **Total Variance**: $150.00
- **Explained Variance**: $100.00
- **Unexplained Variance**: $50.00

### Key Discrepancies
1. **Amount Mismatch**: Bank $1,250.00 vs Ledger $1,200.00 (Difference: $50.00)
2. **Missing Transaction**: Bank TXN-001 ($500.00) not in ledger

## Recommendations

### Immediate Actions
1. **Review Unmatched Transactions**: Investigate 13 unmatched items
2. **Resolve High Priority Discrepancies**: Address 3 high-priority issues
3. **Manual Review**: Complete review of 2 remaining exceptions

### Process Improvements
1. **Enhance Matching Rules**: Improve fuzzy matching algorithms
2. **Automated Exception Handling**: Implement auto-resolution for common discrepancies
3. **Real-time Monitoring**: Set up alerts for significant variances

### Quality Assurance
1. **Daily Reconciliation**: Implement daily reconciliation process
2. **Exception Reporting**: Create automated exception reports
3. **Audit Trail**: Maintain comprehensive audit trail

## Compliance Status
✅ **Reconciliation completed within SLA**  
✅ **Audit trail maintained**  
✅ **Exception handling documented**  
⚠️ **2 exceptions require manual review**

---
*Report generated by Financial Reconciliation Agent on {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC*
*Reconciliation process completed successfully*
"""
            
            # Add AI message to state
            ai_message = AIMessage(content=reconciliation_content)
            state.messages.append(ai_message)
            state.completed_steps.append("format_reconciliation_response")
            
            logger.info("Reconciliation response formatted", agent_id=self.agent_id)
            return state
    
    async def _format_response(self, state: AgentState) -> Dict[str, Any]:
        """Format the final response from graph execution."""
        with self.tracer.start_as_current_span("reconciliation.format_response"):
            try:
                # Get the last AI message
                ai_messages = [msg for msg in state.messages if hasattr(msg, 'content') and getattr(msg, '__class__', None) and getattr(msg.__class__, '__name__', '') == 'AIMessage']
                last_message = ai_messages[-1] if ai_messages else None
                
                return {
                    "agent_id": self.agent_id,
                    "session_id": getattr(state.context, 'session_id', None) if state.context else None,
                    "response": getattr(last_message, 'content', "No reconciliation completed") if last_message else "No reconciliation completed",
                    "metadata": state.metadata,
                    "completed_steps": state.completed_steps,
                    "error": state.error,
                }
                
            except Exception as e:
                logger.error("Response formatting failed", error=str(e))
                return {
                    "agent_id": self.agent_id,
                    "session_id": getattr(state.context, 'session_id', None) if state.context else None,
                    "response": "Error occurred during reconciliation",
                    "metadata": state.metadata,
                    "completed_steps": state.completed_steps,
                    "error": f"Response formatting failed: {str(e)}",
                }
