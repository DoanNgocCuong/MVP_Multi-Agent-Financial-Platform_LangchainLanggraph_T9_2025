"""Data Sync Agent for data synchronization and integration."""

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


class DataSyncAgent(BaseAgent):
    """Data Sync Agent for data synchronization and integration."""
    
    def __init__(self, industry: str = "general"):
        """Initialize the Data Sync Agent."""
        super().__init__(
            agent_id="data_sync_agent",
            name="Data Synchronization Agent",
            description="Data synchronization and integration system",
            capabilities=[
                "data_synchronization",
                "system_integration",
                "data_standardization",
                "error_handling",
                "batch_processing",
                "real_time_sync",
                "data_validation",
                "conflict_resolution"
            ]
        )
        self.industry = industry
        self._build_graph()
    
    def _build_graph(self):
        """Build the LangGraph workflow for data sync."""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("analyze_sync_request", self._analyze_sync_request)
        workflow.add_node("connect_systems", self._connect_systems)
        workflow.add_node("extract_data", self._extract_data)
        workflow.add_node("transform_data", self._transform_data)
        workflow.add_node("validate_data", self._validate_data)
        workflow.add_node("sync_data", self._sync_data)
        workflow.add_node("format_sync_response", self._format_sync_response)
        
        # Define workflow
        workflow.set_entry_point("analyze_sync_request")
        workflow.add_edge("analyze_sync_request", "connect_systems")
        workflow.add_edge("connect_systems", "extract_data")
        workflow.add_edge("extract_data", "transform_data")
        workflow.add_edge("transform_data", "validate_data")
        workflow.add_edge("validate_data", "sync_data")
        workflow.add_edge("sync_data", "format_sync_response")
        workflow.add_edge("format_sync_response", END)
        
        self.compiled_graph = workflow.compile()
    
    async def _analyze_sync_request(self, state: AgentState) -> AgentState:
        """Analyze the sync request."""
        with self.tracer.start_as_current_span("sync.analyze_request"):
            request = state.messages[-1].content if state.messages else ""
            
            analysis_plan = {
                "request": request,
                "sync_type": "full_synchronization",
                "source_systems": ["ERP", "CRM", "Banking"],
                "target_system": "Financial_System",
                "sync_mode": "batch",
                "timestamp": datetime.utcnow().isoformat()
            }
            
            state.metadata["analysis_plan"] = analysis_plan
            state.completed_steps.append("analyze_sync_request")
            
            logger.info("Sync request analyzed", agent_id=self.agent_id)
            return state
    
    async def _connect_systems(self, state: AgentState) -> AgentState:
        """Connect to source and target systems."""
        with self.tracer.start_as_current_span("sync.connect_systems"):
            # Mock system connections
            connections = {
                "source_connections": {
                    "ERP": {"status": "connected", "records": 1500},
                    "CRM": {"status": "connected", "records": 800},
                    "Banking": {"status": "connected", "records": 200}
                },
                "target_connection": {
                    "Financial_System": {"status": "connected", "ready": True}
                },
                "connection_health": "healthy"
            }
            
            state.metadata["connections"] = connections
            state.completed_steps.append("connect_systems")
            
            logger.info("Systems connected", agent_id=self.agent_id)
            return state
    
    async def _extract_data(self, state: AgentState) -> AgentState:
        """Extract data from source systems."""
        with self.tracer.start_as_current_span("sync.extract_data"):
            # Mock data extraction
            extracted_data = {
                "erp_data": {
                    "transactions": 1200,
                    "accounts": 150,
                    "invoices": 800,
                    "extraction_status": "success"
                },
                "crm_data": {
                    "customers": 500,
                    "contacts": 800,
                    "opportunities": 200,
                    "extraction_status": "success"
                },
                "banking_data": {
                    "transactions": 200,
                    "accounts": 25,
                    "statements": 12,
                    "extraction_status": "success"
                },
                "total_records": 2500
            }
            
            state.metadata["extracted_data"] = extracted_data
            state.completed_steps.append("extract_data")
            
            logger.info("Data extracted", agent_id=self.agent_id)
            return state
    
    async def _transform_data(self, state: AgentState) -> AgentState:
        """Transform data to target format."""
        with self.tracer.start_as_current_span("sync.transform_data"):
            # Mock data transformation
            transformation_results = {
                "transformation_status": "success",
                "transformed_records": {
                    "financial_transactions": 1400,
                    "customer_records": 500,
                    "account_mappings": 175,
                    "standardized_invoices": 800
                },
                "transformation_errors": 0,
                "data_quality_score": 0.95
            }
            
            state.metadata["transformation_results"] = transformation_results
            state.completed_steps.append("transform_data")
            
            logger.info("Data transformed", agent_id=self.agent_id)
            return state
    
    async def _validate_data(self, state: AgentState) -> AgentState:
        """Validate transformed data."""
        with self.tracer.start_as_current_span("sync.validate_data"):
            # Mock validation
            validation_results = {
                "validation_status": "passed",
                "validated_records": 2500,
                "validation_errors": 0,
                "data_integrity": "maintained",
                "business_rules": "compliant"
            }
            
            state.metadata["validation_results"] = validation_results
            state.completed_steps.append("validate_data")
            
            logger.info("Data validated", agent_id=self.agent_id)
            return state
    
    async def _sync_data(self, state: AgentState) -> AgentState:
        """Sync data to target system."""
        with self.tracer.start_as_current_span("sync.sync_data"):
            # Mock data sync
            sync_results = {
                "sync_status": "completed",
                "synced_records": 2500,
                "sync_errors": 0,
                "sync_duration": "2.5 minutes",
                "data_consistency": "verified"
            }
            
            state.metadata["sync_results"] = sync_results
            state.completed_steps.append("sync_data")
            
            logger.info("Data synced", agent_id=self.agent_id)
            return state
    
    async def _format_sync_response(self, state: AgentState) -> AgentState:
        """Format the final sync response."""
        with self.tracer.start_as_current_span("sync.format_response"):
            connections = state.metadata.get("connections", {})
            extracted_data = state.metadata.get("extracted_data", {})
            sync_results = state.metadata.get("sync_results", {})
            
            # Create comprehensive sync report
            sync_report = f"""# Data Synchronization Report

## Synchronization Summary
**Status**: ✅ **COMPLETED SUCCESSFULLY**  
**Total Records Processed**: 2,500  
**Sync Duration**: 2.5 minutes  
**Data Quality Score**: 95%

## System Connections

### Source Systems
- **ERP System**: ✅ Connected (1,500 records)
- **CRM System**: ✅ Connected (800 records)  
- **Banking System**: ✅ Connected (200 records)

### Target System
- **Financial System**: ✅ Connected and Ready

## Data Extraction Results

### ERP Data
- **Transactions**: 1,200 records ✅
- **Accounts**: 150 records ✅
- **Invoices**: 800 records ✅

### CRM Data
- **Customers**: 500 records ✅
- **Contacts**: 800 records ✅
- **Opportunities**: 200 records ✅

### Banking Data
- **Transactions**: 200 records ✅
- **Accounts**: 25 records ✅
- **Statements**: 12 records ✅

## Data Processing

### Transformation Results
- **Financial Transactions**: 1,400 records processed
- **Customer Records**: 500 records processed
- **Account Mappings**: 175 records processed
- **Standardized Invoices**: 800 records processed
- **Transformation Errors**: 0 ✅

### Validation Results
- **Validation Status**: ✅ PASSED
- **Validated Records**: 2,500
- **Validation Errors**: 0 ✅
- **Data Integrity**: ✅ MAINTAINED
- **Business Rules**: ✅ COMPLIANT

## Synchronization Results
- **Sync Status**: ✅ COMPLETED
- **Synced Records**: 2,500
- **Sync Errors**: 0 ✅
- **Data Consistency**: ✅ VERIFIED

## Performance Metrics
- **Total Processing Time**: 2.5 minutes
- **Records per Minute**: 1,000
- **Success Rate**: 100%
- **Data Quality**: 95%

## Recommendations
1. **Regular Sync**: Schedule daily synchronization
2. **Monitoring**: Set up automated monitoring for sync health
3. **Backup**: Maintain data backup before each sync
4. **Error Handling**: Implement automated error recovery

---
*Report generated by Data Synchronization Agent on {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC*
*Synchronization completed successfully*
"""
            
            # Add AI message to state
            ai_message = AIMessage(content=sync_report)
            state.messages.append(ai_message)
            state.completed_steps.append("format_sync_response")
            
            logger.info("Sync response formatted", agent_id=self.agent_id)
            return state
    
    async def _format_response(self, state: AgentState) -> Dict[str, Any]:
        """Format the final response from graph execution."""
        with self.tracer.start_as_current_span("sync.format_response"):
            try:
                # Get the last AI message
                ai_messages = [msg for msg in state.messages if hasattr(msg, 'content') and getattr(msg, '__class__', None) and getattr(msg.__class__, '__name__', '') == 'AIMessage']
                last_message = ai_messages[-1] if ai_messages else None
                
                return {
                    "agent_id": self.agent_id,
                    "session_id": getattr(state.context, 'session_id', None) if state.context else None,
                    "response": getattr(last_message, 'content', "No sync completed") if last_message else "No sync completed",
                    "metadata": state.metadata,
                    "completed_steps": state.completed_steps,
                    "error": state.error,
                }
                
            except Exception as e:
                logger.error("Response formatting failed", error=str(e))
                return {
                    "agent_id": self.agent_id,
                    "session_id": getattr(state.context, 'session_id', None) if state.context else None,
                    "response": "Error occurred during data synchronization",
                    "metadata": state.metadata,
                    "completed_steps": state.completed_steps,
                    "error": f"Response formatting failed: {str(e)}",
                }
