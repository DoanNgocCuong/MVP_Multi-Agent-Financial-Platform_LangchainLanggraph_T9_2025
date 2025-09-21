"""AI CFO Agent for industry-specific financial advisory and analysis.

## Luồng Nội Bộ (Internal Workflow)

AI CFO Agent sử dụng LangGraph workflow với 7 bước xử lý tuần tự:

### 1. analyze_request
- **Mục đích**: Phân tích và hiểu yêu cầu từ user
- **Input**: Message từ user (text)
- **Xử lý**: 
  - Phân loại loại phân tích cần thiết
  - Xác định industry context
  - Tạo analysis plan
- **Output**: Analysis plan trong metadata

### 2. gather_data
- **Mục đích**: Thu thập dữ liệu tài chính cần thiết
- **Input**: Analysis plan từ bước 1
- **Xử lý**:
  - Xác định loại dữ liệu cần thiết
  - Thu thập từ các nguồn (database, APIs, files)
  - Validate và clean data
- **Output**: Financial data trong metadata

### 3. perform_analysis
- **Mục đích**: Thực hiện phân tích tài chính chuyên sâu
- **Input**: Financial data từ bước 2
- **Xử lý**:
  - Tính toán các ratios và metrics
  - So sánh với benchmarks
  - Phân tích trends và patterns
- **Output**: Analysis results trong metadata

### 4. generate_insights
- **Mục đích**: Tạo insights và interpretations
- **Input**: Analysis results từ bước 3
- **Xử lý**:
  - Interpret kết quả phân tích
  - Identify key findings
  - Generate actionable insights
- **Output**: Insights trong metadata

### 5. assess_risks
- **Mục đích**: Đánh giá rủi ro tài chính
- **Input**: Analysis results và insights
- **Xử lý**:
  - Identify potential risks
  - Quantify risk levels
  - Assess impact và probability
- **Output**: Risk assessment trong metadata

### 6. provide_recommendations
- **Mục đích**: Đưa ra recommendations cụ thể
- **Input**: Insights và risk assessment
- **Xử lý**:
  - Generate actionable recommendations
  - Prioritize based on impact
  - Create implementation plan
- **Output**: Recommendations trong metadata

### 7. format_response
- **Mục đích**: Format final report
- **Input**: Tất cả data từ các bước trước
- **Xử lý**:
  - Compile comprehensive report
  - Format as Markdown
  - Add executive summary
- **Output**: Final report (Markdown format)

## Luồng Dữ Liệu (Data Flow)

```
User Input (text) 
    ↓
analyze_request → analysis_plan
    ↓
gather_data → financial_data  
    ↓
perform_analysis → analysis_results
    ↓
generate_insights → insights
    ↓
assess_risks → risk_assessment
    ↓
provide_recommendations → recommendations
    ↓
format_response → final_report (Markdown)
```

## LangSmith/LangFuse Integration

Để visualize và debug workflow này:

### LangFuse (Recommended - Free):
- ✅ **Graph Visualization**: Xem workflow dạng graph
- ✅ **Node Execution**: Chạy từng node riêng lẻ
- ✅ **Trace Monitoring**: Theo dõi execution flow
- ✅ **Performance Metrics**: Đo thời gian từng bước
- ✅ **Error Tracking**: Debug lỗi trong workflow

### Setup LangFuse:
```python
# Trong base_agent.py hoặc main.py
from langfuse import Langfuse
from langfuse.callback import CallbackHandler

langfuse = Langfuse()
handler = CallbackHandler()

# Thêm vào graph execution
result = await self.compiled_graph.ainvoke(
    initial_state, 
    config={"callbacks": [handler]}
)
```

## Demo Mode vs Production Mode

**Demo Mode** (hiện tại):
- Sử dụng mock data cố định
- LLM responses được simulate
- Tất cả analysis dựa trên sample data

**Production Mode** (khi có OpenAI API key):
- Sử dụng real LLM (GPT-4)
- Phân tích dữ liệu thực tế
- Dynamic insights và recommendations
"""

import asyncio
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages

from ai_financial.core.base_agent import BaseAgent
from ai_financial.core.config import settings
from ai_financial.core.logging import get_logger
from ai_financial.models.agent_models import AgentContext, AgentState

logger = get_logger(__name__)


class AICFOAgent(BaseAgent):
    """AI CFO Agent for industry-specific financial advisory and analysis."""

    def __init__(self, industry: str = "general"):
        """Initialize AI CFO Agent."""
        super().__init__(
            agent_id="ai_cfo_agent",
            name="AI CFO Agent",
            description="Industry-specific financial advisory and analysis agent"
        )
        self.industry = industry
        
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
            temperature=settings.llm.openai_temperature,
            max_tokens=settings.llm.openai_max_tokens,
            api_key=settings.llm.openai_api_key
        )
    
    def _get_langfuse_handler(self):
        """Get LangFuse callback handler."""
        try:
            from langfuse.langchain import CallbackHandler
            return CallbackHandler()
        except ImportError:
            logger.warning("LangFuse not installed - tracing disabled")
            return None
    
    def _get_mock_llm(self):
        """Get mock LLM for demo mode."""
        from langchain_core.messages import AIMessage
        
        class MockLLM:
            async def ainvoke(self, messages, **kwargs):
                # Simulate LLM response based on message content
                content = messages[0].content if messages else ""
                
                if "analyze" in content.lower():
                    return AIMessage(content='{"analysis_types": ["Financial Health Assessment"], "priority": "high", "data_requirements": ["balance_sheet", "income_statement"], "timeline": "1-2 days"}')
                elif "gather" in content.lower():
                    return AIMessage(content="Financial data gathered successfully: Balance Sheet, Income Statement, Cash Flow Statement")
                elif "analyze" in content.lower() and "perform" in content.lower():
                    return AIMessage(content="Analysis completed: Current Ratio: 2.1, Debt-to-Equity: 0.8, ROE: 15.2%")
                elif "insights" in content.lower():
                    return AIMessage(content="Key insights: Strong liquidity position, manageable debt levels, good profitability")
                elif "risk" in content.lower():
                    return AIMessage(content="Risk assessment: Low credit risk, moderate market risk, high operational efficiency")
                elif "recommend" in content.lower():
                    return AIMessage(content="Recommendations: 1) Optimize working capital, 2) Consider debt refinancing, 3) Invest in growth initiatives")
                else:
                    return AIMessage(content="AI CFO analysis completed successfully.")
        
        return MockLLM()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow."""
        graph = StateGraph(AgentState)
        
        # Add nodes
        graph.add_node("analyze_request", self._analyze_request)
        graph.add_node("gather_data", self._gather_financial_data)
        graph.add_node("perform_analysis", self._perform_financial_analysis)
        graph.add_node("generate_insights", self._generate_insights)
        graph.add_node("assess_risks", self._assess_risks)
        graph.add_node("provide_recommendations", self._provide_recommendations)
        graph.add_node("format_response", self._format_response)
        
        # Define workflow edges - FIXED: Add entrypoint
        graph.set_entry_point("analyze_request")  # ← This is the missing entrypoint!
        graph.add_edge("analyze_request", "gather_data")
        graph.add_edge("gather_data", "perform_analysis")
        graph.add_edge("perform_analysis", "generate_insights")
        graph.add_edge("generate_insights", "assess_risks")
        graph.add_edge("assess_risks", "provide_recommendations")
        graph.add_edge("provide_recommendations", "format_response")
        graph.add_edge("format_response", END)
        
        return graph
    
    async def _analyze_request(self, state: AgentState) -> AgentState:
        """Analyze the user request and create analysis plan."""
        try:
            logger.info("🔍 Analyzing request...")
            
            # Get user message
            user_message = state.messages[-1].content if state.messages else ""
            
            # Create analysis plan using LLM
            analysis_prompt = f"""
            Analyze this financial request and determine the type of analysis needed:

            Request: {user_message}

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
            
            response = await self.llm.ainvoke([HumanMessage(content=analysis_prompt)])
            classification = response.content if hasattr(response, 'content') else str(response)
            
            # Update metadata
            state.metadata["analysis_plan"] = {
                "request": user_message,
                "classification": classification,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            state.completed_steps.append("analyze_request")
            state.current_step = "gather_data"
            
            logger.info("✅ Request analyzed successfully")
            return state
            
        except Exception as e:
            logger.error(f"❌ Error analyzing request: {str(e)}")
            state.error = str(e)
            return state
    
    async def _gather_financial_data(self, state: AgentState) -> AgentState:
        """Gather financial data based on analysis plan."""
        try:
            logger.info("📊 Gathering financial data...")
            
            # Simulate data gathering
            data_prompt = f"""
            Based on the analysis plan, gather the following financial data:
            - Balance Sheet (last 3 years)
            - Income Statement (last 3 years)
            - Cash Flow Statement (last 3 years)
            - Key financial ratios
            - Industry benchmarks
            """
            
            response = await self.llm.ainvoke([HumanMessage(content=data_prompt)])
            data_summary = response.content if hasattr(response, 'content') else str(response)
            
            # Update metadata
            state.metadata["financial_data"] = {
                "data_summary": data_summary,
                "sources": ["balance_sheet", "income_statement", "cash_flow"],
                "timestamp": datetime.utcnow().isoformat()
            }
            
            state.completed_steps.append("gather_data")
            state.current_step = "perform_analysis"
            
            logger.info("✅ Financial data gathered successfully")
            return state
            
        except Exception as e:
            logger.error(f"❌ Error gathering data: {str(e)}")
            state.error = str(e)
            return state
    
    async def _perform_financial_analysis(self, state: AgentState) -> AgentState:
        """Perform comprehensive financial analysis."""
        try:
            logger.info("🧮 Performing financial analysis...")
            
            # Simulate analysis
            analysis_prompt = f"""
            Perform comprehensive financial analysis including:
            - Liquidity ratios (Current Ratio, Quick Ratio)
            - Leverage ratios (Debt-to-Equity, Interest Coverage)
            - Profitability ratios (ROE, ROA, Net Margin)
            - Efficiency ratios (Asset Turnover, Inventory Turnover)
            - Trend analysis over 3 years
            """
            
            response = await self.llm.ainvoke([HumanMessage(content=analysis_prompt)])
            analysis_results = response.content if hasattr(response, 'content') else str(response)
            
            # Update metadata
            state.metadata["analysis_results"] = {
                "results": analysis_results,
                "ratios_calculated": ["current_ratio", "debt_to_equity", "roe", "roa"],
                "timestamp": datetime.utcnow().isoformat()
            }
            
            state.completed_steps.append("perform_analysis")
            state.current_step = "generate_insights"
            
            logger.info("✅ Financial analysis completed")
            return state
            
        except Exception as e:
            logger.error(f"❌ Error performing analysis: {str(e)}")
            state.error = str(e)
            return state
    
    async def _generate_insights(self, state: AgentState) -> AgentState:
        """Generate insights from analysis results."""
        try:
            logger.info("💡 Generating insights...")
            
            # Simulate insight generation
            insights_prompt = f"""
            Generate key insights from the financial analysis:
            - What are the main strengths and weaknesses?
            - How does the company compare to industry benchmarks?
            - What trends are evident in the data?
            - What are the key performance indicators showing?
            """
            
            response = await self.llm.ainvoke([HumanMessage(content=insights_prompt)])
            insights = response.content if hasattr(response, 'content') else str(response)
            
            # Update metadata
            state.metadata["insights"] = {
                "key_insights": insights,
                "strengths": ["Strong liquidity", "Good profitability"],
                "weaknesses": ["High debt levels", "Slow growth"],
                "timestamp": datetime.utcnow().isoformat()
            }
            
            state.completed_steps.append("generate_insights")
            state.current_step = "assess_risks"
            
            logger.info("✅ Insights generated successfully")
            return state
            
        except Exception as e:
            logger.error(f"❌ Error generating insights: {str(e)}")
            state.error = str(e)
            return state
    
    async def _assess_risks(self, state: AgentState) -> AgentState:
        """Assess financial risks."""
        try:
            logger.info("⚠️ Assessing risks...")
            
            # Simulate risk assessment
            risk_prompt = f"""
            Assess the following financial risks:
            - Credit risk
            - Market risk
            - Operational risk
            - Liquidity risk
            - Regulatory risk
            Provide risk levels (Low/Medium/High) and mitigation strategies.
            """
            
            response = await self.llm.ainvoke([HumanMessage(content=risk_prompt)])
            risk_assessment = response.content if hasattr(response, 'content') else str(response)
            
            # Update metadata
            state.metadata["risk_assessment"] = {
                "assessment": risk_assessment,
                "risk_levels": {"credit": "Low", "market": "Medium", "operational": "Low"},
                "timestamp": datetime.utcnow().isoformat()
            }
            
            state.completed_steps.append("assess_risks")
            state.current_step = "provide_recommendations"
            
            logger.info("✅ Risk assessment completed")
            return state
            
        except Exception as e:
            logger.error(f"❌ Error assessing risks: {str(e)}")
            state.error = str(e)
            return state
    
    async def _provide_recommendations(self, state: AgentState) -> AgentState:
        """Provide actionable recommendations."""
        try:
            logger.info("🎯 Providing recommendations...")
            
            # Simulate recommendations
            rec_prompt = f"""
            Provide actionable recommendations based on the analysis:
            - Short-term actions (1-3 months)
            - Medium-term strategies (3-12 months)
            - Long-term initiatives (1-3 years)
            - Priority levels and expected impact
            """
            
            response = await self.llm.ainvoke([HumanMessage(content=rec_prompt)])
            recommendations = response.content if hasattr(response, 'content') else str(response)
            
            # Update metadata
            state.metadata["recommendations"] = {
                "recommendations": recommendations,
                "priorities": ["High", "Medium", "Low"],
                "timeline": ["1-3 months", "3-12 months", "1-3 years"],
                "timestamp": datetime.utcnow().isoformat()
            }
            
            state.completed_steps.append("provide_recommendations")
            state.current_step = "format_response"
            
            logger.info("✅ Recommendations provided")
            return state
            
        except Exception as e:
            logger.error(f"❌ Error providing recommendations: {str(e)}")
            state.error = str(e)
            return state
    
        """Format the final response."""
        try:
            logger.info("📝 Formatting response...")
            
            # Create comprehensive report
            report = f"""# AI CFO Financial Analysis Report

## Executive Summary
{state.metadata.get('analysis_plan', {}).get('request', 'Financial analysis request')}

## Analysis Plan
{state.metadata.get('analysis_plan', {}).get('classification', 'Analysis classification')}

## Financial Data
{state.metadata.get('financial_data', {}).get('data_summary', 'Financial data summary')}

## Analysis Results
{state.metadata.get('analysis_results', {}).get('results', 'Analysis results')}

## Key Insights
{state.metadata.get('insights', {}).get('key_insights', 'Key insights')}

## Risk Assessment
{state.metadata.get('risk_assessment', {}).get('assessment', 'Risk assessment')}

## Recommendations
{state.metadata.get('recommendations', {}).get('recommendations', 'Recommendations')}

---
*Report generated by AI CFO Agent on {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}*
"""
            
            # Add final message
            from langchain_core.messages import AIMessage
            state.messages.append(AIMessage(content=report))
            
            # Update metadata
            state.metadata["final_report"] = {
                "report": report,
                "format": "markdown",
                "timestamp": datetime.utcnow().isoformat()
            }
            
            state.completed_steps.append("format_response")
            state.current_step = "completed"
            
            logger.info("✅ Response formatted successfully")
            return state
            
        except Exception as e:
            logger.error(f"❌ Error formatting response: {str(e)}")
            state.error = str(e)
            return state
    
    async def _process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming request - required by BaseAgent abstract method."""
        try:
            # Extract message from request
            message = request.get("message", "")
            context_data = request.get("context", {})
            
            # Create initial state
            from langchain_core.messages import HumanMessage
            from ai_financial.models.agent_models import AgentContext, AgentState
            
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
            
            # Get LangFuse callback handler
            langfuse_handler = self._get_langfuse_handler()
            config = {"callbacks": [langfuse_handler]} if langfuse_handler else {}
            
            # Run the workflow with LangFuse tracing
            result = await self.compiled_graph.ainvoke(initial_state, config=config)
            
            # Format response
            response = await self._format_response(result)
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            return {
                "agent_id": self.agent_id,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }


# Export for LangGraph Studio
def ai_cfo_agent():
    """Export function for LangGraph Studio."""
    agent = AICFOAgent(industry="general")
    return agent.compiled_graph
