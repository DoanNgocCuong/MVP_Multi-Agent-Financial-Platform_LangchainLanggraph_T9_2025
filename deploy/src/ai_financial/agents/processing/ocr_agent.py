"""OCR Agent for document processing and data extraction."""

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


class OCRAgent(BaseAgent):
    """OCR Agent for document processing and data extraction."""
    
    def __init__(self, industry: str = "general"):
        """Initialize the OCR Agent."""
        super().__init__(
            agent_id="ocr_agent",
            name="Document Processing Agent",
            description="OCR and document processing for financial documents",
            capabilities=[
                "document_ocr",
                "invoice_processing",
                "receipt_extraction",
                "data_validation",
                "format_standardization",
                "error_detection",
                "batch_processing",
                "quality_assurance"
            ]
        )
        self.industry = industry
        self._build_graph()
    
    def _build_graph(self):
        """Build the LangGraph workflow for OCR processing."""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("analyze_document", self._analyze_document)
        workflow.add_node("extract_text", self._extract_text)
        workflow.add_node("validate_data", self._validate_data)
        workflow.add_node("standardize_format", self._standardize_format)
        workflow.add_node("quality_check", self._quality_check)
        workflow.add_node("format_ocr_response", self._format_ocr_response)
        
        # Define workflow
        workflow.set_entry_point("analyze_document")
        workflow.add_edge("analyze_document", "extract_text")
        workflow.add_edge("extract_text", "validate_data")
        workflow.add_edge("validate_data", "standardize_format")
        workflow.add_edge("standardize_format", "quality_check")
        workflow.add_edge("quality_check", "format_ocr_response")
        workflow.add_edge("format_ocr_response", END)
        
        self.compiled_graph = workflow.compile()
    
    async def _analyze_document(self, state: AgentState) -> AgentState:
        """Analyze the document type and requirements."""
        with self.tracer.start_as_current_span("ocr.analyze_document"):
            request = state.messages[-1].content if state.messages else ""
            
            analysis_plan = {
                "request": request,
                "document_type": "invoice",
                "processing_mode": "standard",
                "extraction_fields": ["amount", "date", "vendor", "description"],
                "timestamp": datetime.utcnow().isoformat()
            }
            
            state.metadata["analysis_plan"] = analysis_plan
            state.completed_steps.append("analyze_document")
            
            logger.info("Document analyzed", agent_id=self.agent_id)
            return state
    
    async def _extract_text(self, state: AgentState) -> AgentState:
        """Extract text from document."""
        with self.tracer.start_as_current_span("ocr.extract_text"):
            # Mock OCR extraction
            extracted_data = {
                "raw_text": "Invoice #INV-2025-001\nVendor: ABC Corp\nDate: 2025-01-15\nAmount: $1,250.00\nDescription: Consulting Services",
                "structured_data": {
                    "invoice_number": "INV-2025-001",
                    "vendor": "ABC Corp",
                    "date": "2025-01-15",
                    "amount": 1250.00,
                    "description": "Consulting Services"
                },
                "confidence_scores": {
                    "invoice_number": 0.95,
                    "vendor": 0.90,
                    "date": 0.98,
                    "amount": 0.92,
                    "description": 0.85
                }
            }
            
            state.metadata["extracted_data"] = extracted_data
            state.completed_steps.append("extract_text")
            
            logger.info("Text extracted", agent_id=self.agent_id)
            return state
    
    async def _validate_data(self, state: AgentState) -> AgentState:
        """Validate extracted data."""
        with self.tracer.start_as_current_span("ocr.validate_data"):
            # Mock validation
            validation_results = {
                "validation_status": "passed",
                "validated_fields": {
                    "invoice_number": {"status": "valid", "format": "correct"},
                    "vendor": {"status": "valid", "format": "correct"},
                    "date": {"status": "valid", "format": "correct"},
                    "amount": {"status": "valid", "format": "correct"},
                    "description": {"status": "valid", "format": "correct"}
                },
                "validation_errors": [],
                "data_quality_score": 0.92
            }
            
            state.metadata["validation_results"] = validation_results
            state.completed_steps.append("validate_data")
            
            logger.info("Data validated", agent_id=self.agent_id)
            return state
    
    async def _standardize_format(self, state: AgentState) -> AgentState:
        """Standardize data format."""
        with self.tracer.start_as_current_span("ocr.standardize_format"):
            # Mock standardization
            standardized_data = {
                "standardized_fields": {
                    "invoice_number": "INV-2025-001",
                    "vendor_name": "ABC Corp",
                    "invoice_date": "2025-01-15",
                    "total_amount": 1250.00,
                    "currency": "USD",
                    "line_items": [
                        {
                            "description": "Consulting Services",
                            "amount": 1250.00,
                            "quantity": 1,
                            "unit_price": 1250.00
                        }
                    ]
                },
                "format_compliance": "compliant",
                "standardization_notes": "All fields successfully standardized"
            }
            
            state.metadata["standardized_data"] = standardized_data
            state.completed_steps.append("standardize_format")
            
            logger.info("Format standardized", agent_id=self.agent_id)
            return state
    
    async def _quality_check(self, state: AgentState) -> AgentState:
        """Perform quality check."""
        with self.tracer.start_as_current_span("ocr.quality_check"):
            # Mock quality check
            quality_results = {
                "overall_quality": "high",
                "quality_metrics": {
                    "accuracy": 0.92,
                    "completeness": 1.0,
                    "consistency": 0.95,
                    "reliability": 0.90
                },
                "quality_issues": [],
                "recommendations": ["Data quality is excellent", "No manual review required"]
            }
            
            state.metadata["quality_results"] = quality_results
            state.completed_steps.append("quality_check")
            
            logger.info("Quality check completed", agent_id=self.agent_id)
            return state
    
    async def _format_ocr_response(self, state: AgentState) -> AgentState:
        """Format the final OCR response."""
        with self.tracer.start_as_current_span("ocr.format_response"):
            extracted_data = state.metadata.get("extracted_data", {})
            standardized_data = state.metadata.get("standardized_data", {})
            quality_results = state.metadata.get("quality_results", {})
            
            # Create comprehensive OCR report
            ocr_report = f"""# Document Processing & OCR Report

## Document Analysis Summary
**Document Type**: Invoice  
**Processing Status**: ✅ **SUCCESS**  
**Data Quality Score**: 92%  
**Overall Quality**: High

## Extracted Information

### Invoice Details
- **Invoice Number**: INV-2025-001
- **Vendor**: ABC Corp
- **Date**: 2025-01-15
- **Total Amount**: $1,250.00
- **Currency**: USD

### Line Items
| Description | Quantity | Unit Price | Amount |
|-------------|----------|------------|---------|
| Consulting Services | 1 | $1,250.00 | $1,250.00 |

## Data Quality Assessment

### Confidence Scores
- **Invoice Number**: 95% ✅
- **Vendor**: 90% ✅
- **Date**: 98% ✅
- **Amount**: 92% ✅
- **Description**: 85% ✅

### Quality Metrics
- **Accuracy**: 92% ✅
- **Completeness**: 100% ✅
- **Consistency**: 95% ✅
- **Reliability**: 90% ✅

## Validation Results
✅ **All fields validated successfully**  
✅ **Format compliance verified**  
✅ **No data quality issues detected**  
✅ **Ready for financial processing**

## Processing Notes
- Document processed using standard OCR pipeline
- All required fields successfully extracted
- Data standardized to company format
- No manual review required

## Recommendations
1. **Data Quality**: Excellent - no issues detected
2. **Processing**: Document ready for financial system integration
3. **Automation**: Suitable for automated processing pipeline

---
*Report generated by Document Processing Agent on {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC*
*OCR processing completed successfully*
"""
            
            # Add AI message to state
            ai_message = AIMessage(content=ocr_report)
            state.messages.append(ai_message)
            state.completed_steps.append("format_ocr_response")
            
            logger.info("OCR response formatted", agent_id=self.agent_id)
            return state
    
    async def _format_response(self, state: AgentState) -> Dict[str, Any]:
        """Format the final response from graph execution."""
        with self.tracer.start_as_current_span("ocr.format_response"):
            try:
                # Get the last AI message
                ai_messages = [msg for msg in state.messages if hasattr(msg, 'content') and getattr(msg, '__class__', None) and getattr(msg.__class__, '__name__', '') == 'AIMessage']
                last_message = ai_messages[-1] if ai_messages else None
                
                return {
                    "agent_id": self.agent_id,
                    "session_id": getattr(state.context, 'session_id', None) if state.context else None,
                    "response": getattr(last_message, 'content', "No OCR processing completed") if last_message else "No OCR processing completed",
                    "metadata": state.metadata,
                    "completed_steps": state.completed_steps,
                    "error": state.error,
                }
                
            except Exception as e:
                logger.error("Response formatting failed", error=str(e))
                return {
                    "agent_id": self.agent_id,
                    "session_id": getattr(state.context, 'session_id', None) if state.context else None,
                    "response": "Error occurred during OCR processing",
                    "metadata": state.metadata,
                    "completed_steps": state.completed_steps,
                    "error": f"Response formatting failed: {str(e)}",
                }
