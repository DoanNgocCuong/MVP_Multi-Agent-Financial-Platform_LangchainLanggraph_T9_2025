"""Main application entry point for the AI Financial Multi-Agent System."""

import asyncio
from typing import Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import uvicorn

from ai_financial.core.config import settings
from ai_financial.core.logging import get_logger, setup_logging, setup_tracing
from ai_financial.orchestrator.orchestrator import get_orchestrator
from ai_financial.mcp.hub import get_tool_hub
from ai_financial.agents.advisory.ai_cfo_agent import AICFOAgent
from ai_financial.mcp.tools.financial_tools import (
    FinancialRatioTool,
    CashFlowAnalysisTool,
    ProfitabilityAnalysisTool,
)

# Initialize logging and tracing
setup_logging()
setup_tracing()

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    logger.info("Starting AI Financial Multi-Agent System")
    
    # Check configuration
    if not settings.llm.has_openai_key:
        logger.warning("OpenAI API key not configured - running in demo mode")
    
    # Initialize components
    orchestrator = get_orchestrator()
    tool_hub = get_tool_hub()
    
    # Register agents
    try:
        ai_cfo = AICFOAgent(industry="general")
        orchestrator.register_agent(ai_cfo)
    except Exception as e:
        logger.warning(f"Failed to register AI CFO agent: {e}")
    
    # Register tools
    try:
        tool_hub.register_tool(FinancialRatioTool())
        tool_hub.register_tool(CashFlowAnalysisTool())
        tool_hub.register_tool(ProfitabilityAnalysisTool())
    except Exception as e:
        logger.warning(f"Failed to register tools: {e}")
    
    # Start services
    await orchestrator.start()
    
    logger.info(
        "System started successfully",
        agents_count=len(orchestrator.agents),
        tools_count=len(tool_hub.get_available_tools()),
        demo_mode=not settings.llm.has_openai_key,
    )
    
    yield
    
    # Shutdown
    logger.info("Shutting down AI Financial Multi-Agent System")
    await orchestrator.stop()


# Create FastAPI app
app = FastAPI(
    title="AI Financial Multi-Agent System",
    description="Comprehensive financial automation platform for SMBs",
    version="0.1.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# API Routes

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "AI Financial Multi-Agent System",
        "version": "0.1.0",
        "status": "running",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    orchestrator = get_orchestrator()
    tool_hub = get_tool_hub()
    
    return {
        "status": "healthy",
        "orchestrator": orchestrator.get_orchestrator_status(),
        "tool_hub": tool_hub.get_hub_status(),
    }


@app.post("/api/v1/agents/{agent_id}/invoke")
async def invoke_agent(
    agent_id: str,
    request: dict,
):
    """Invoke a specific agent."""
    orchestrator = get_orchestrator()
    
    try:
        # Extract message and context from request
        message = request.get("message", "")
        context_data = request.get("context", {})
        
        # Create enhanced request with context
        enhanced_request = {
            "message": message,
            "context": context_data
        }
        
        result = await orchestrator.route_request(
            request=enhanced_request,
            preferred_agent=agent_id,
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Agent invocation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/workflows/{workflow_type}/execute")
async def execute_workflow(
    workflow_type: str,
    request: dict,
):
    """Execute a workflow."""
    orchestrator = get_orchestrator()
    
    if workflow_type not in ["advisory", "transactional"]:
        raise HTTPException(status_code=400, detail="Invalid workflow type")
    
    try:
        result = await orchestrator.route_request(
            request=request.get("message", ""),
            workflow_type=workflow_type,
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Workflow execution failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/workflows/{workflow_type}/stream")
async def stream_workflow(
    workflow_type: str,
    message: str = "Execute workflow",
):
    """Stream workflow execution."""
    orchestrator = get_orchestrator()
    
    if workflow_type not in ["advisory", "transactional"]:
        raise HTTPException(status_code=400, detail="Invalid workflow type")
    
    async def generate_stream():
        try:
            async for update in orchestrator.stream_workflow(workflow_type, message):
                yield f"data: {update}\n\n"
        except Exception as e:
            logger.error(f"Workflow streaming failed: {str(e)}")
            yield f"data: {{'error': '{str(e)}'}}\n\n"
    
    return StreamingResponse(
        generate_stream(),
        media_type="text/plain",
        headers={"Cache-Control": "no-cache"},
    )


@app.get("/api/v1/tools")
async def list_tools():
    """List available tools."""
    tool_hub = get_tool_hub()
    
    tools = tool_hub.get_available_tools()
    
    return {
        "tools": [tool.model_dump() for tool in tools],
        "count": len(tools),
    }


@app.post("/api/v1/tools/{tool_name}/execute")
async def execute_tool(
    tool_name: str,
    request: dict,
):
    """Execute a tool."""
    tool_hub = get_tool_hub()
    
    try:
        result = await tool_hub.execute_tool(
            tool_name=tool_name,
            parameters=request.get("parameters", {}),
            context=request.get("context"),
        )
        
        return result.model_dump()
        
    except Exception as e:
        logger.error(f"Tool execution failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/status")
async def get_system_status():
    """Get comprehensive system status."""
    orchestrator = get_orchestrator()
    tool_hub = get_tool_hub()
    
    return {
        "system": {
            "version": "0.1.0",
            "environment": settings.environment,
            "debug": settings.debug,
        },
        "orchestrator": orchestrator.get_orchestrator_status(),
        "tool_hub": tool_hub.get_hub_status(),
        "configuration": {
            "max_concurrent_agents": settings.workflow.max_concurrent_agents,
            "api_host": settings.api_host,
            "api_port": settings.api_port,
        },
    }


@app.get("/api/v1/trace-test")
async def trace_test():
    """Test endpoint to demonstrate tracing."""
    from ai_financial.core.logging import get_tracer
    
    tracer = get_tracer(__name__)
    
    with tracer.start_as_current_span("trace_test_span") as span:
        span.set_attribute("test.type", "demo")
        span.set_attribute("test.message", "This is a test trace")
        
        # Simulate some work
        import asyncio
        await asyncio.sleep(0.1)
        
        span.add_event("work_completed", {"duration": 0.1})
        
        return {
            "message": "Trace test completed",
            "trace_id": format(span.get_span_context().trace_id, '032x'),
            "span_id": format(span.get_span_context().span_id, '016x'),
        }


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    return app


async def run_server():
    """Run the FastAPI server."""
    config = uvicorn.Config(
        app,
        host=settings.api_host,
        port=settings.api_port,
        log_level=settings.monitoring.log_level.lower(),
        reload=settings.debug,
    )
    
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(run_server())