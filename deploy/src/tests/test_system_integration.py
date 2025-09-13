"""Integration tests for the AI Financial Multi-Agent System."""

import pytest
import asyncio
from unittest.mock import patch, AsyncMock

from ai_financial.orchestrator.orchestrator import get_orchestrator
from ai_financial.mcp.hub import get_tool_hub
from ai_financial.agents.advisory.ai_cfo_agent import AICFOAgent
from ai_financial.mcp.tools.financial_tools import FinancialRatioTool


class TestSystemIntegration:
    """Test system integration and basic functionality."""
    
    @pytest.fixture
    async def setup_system(self):
        """Set up the system for testing."""
        orchestrator = get_orchestrator()
        tool_hub = get_tool_hub()
        
        # Register agents
        ai_cfo = AICFOAgent(industry="general")
        orchestrator.register_agent(ai_cfo)
        
        # Register tools
        tool_hub.register_tool(FinancialRatioTool())
        
        # Start system
        await orchestrator.start()
        
        yield orchestrator, tool_hub
        
        # Cleanup
        await orchestrator.stop()
        orchestrator.agents.clear()
        tool_hub._tools.clear()
    
    @pytest.mark.asyncio
    async def test_orchestrator_initialization(self, setup_system):
        """Test that orchestrator initializes correctly."""
        orchestrator, tool_hub = setup_system
        
        status = orchestrator.get_orchestrator_status()
        
        assert status["running"] is True
        assert status["registered_agents"] >= 1
        assert "ai_cfo_agent" in status["agent_list"]
    
    @pytest.mark.asyncio
    async def test_tool_hub_initialization(self, setup_system):
        """Test that tool hub initializes correctly."""
        orchestrator, tool_hub = setup_system
        
        status = tool_hub.get_hub_status()
        tools = tool_hub.get_available_tools()
        
        assert status["total_tools"] >= 1
        assert len(tools) >= 1
        assert any(tool.name == "financial_ratio_calculator" for tool in tools)
    
    @pytest.mark.asyncio
    @patch('ai_financial.agents.advisory.ai_cfo_agent.ChatOpenAI')
    async def test_agent_invocation(self, mock_llm, setup_system):
        """Test agent invocation through orchestrator."""
        orchestrator, tool_hub = setup_system
        
        # Mock LLM response
        mock_response = AsyncMock()
        mock_response.content = "This is a test financial analysis response."
        mock_llm.return_value.ainvoke = AsyncMock(return_value=mock_response)
        
        # Test agent invocation
        result = await orchestrator.route_request(
            request="Analyze our financial position",
            preferred_agent="ai_cfo_agent"
        )
        
        assert result is not None
        assert "agent_id" in result
        assert result["agent_id"] == "ai_cfo_agent"
    
    @pytest.mark.asyncio
    async def test_tool_execution(self, setup_system):
        """Test tool execution through tool hub."""
        orchestrator, tool_hub = setup_system
        
        # Test financial ratio calculation
        result = await tool_hub.execute_tool(
            tool_name="financial_ratio_calculator",
            parameters={
                "ratio_type": "current_ratio",
                "financial_data": {
                    "current_assets": 100000,
                    "current_liabilities": 50000
                }
            }
        )
        
        assert result.success is True
        assert result.data is not None
        assert "ratio" in result.data
        assert result.data["ratio"] == 2.0  # 100000 / 50000
    
    @pytest.mark.asyncio
    @patch('ai_financial.agents.advisory.ai_cfo_agent.ChatOpenAI')
    async def test_workflow_execution(self, mock_llm, setup_system):
        """Test workflow execution."""
        orchestrator, tool_hub = setup_system
        
        # Mock LLM responses
        mock_response = AsyncMock()
        mock_response.content = "Workflow step completed successfully."
        mock_llm.return_value.ainvoke = AsyncMock(return_value=mock_response)
        
        # Test advisory workflow
        result = await orchestrator.route_request(
            request="Provide comprehensive financial analysis",
            workflow_type="advisory"
        )
        
        assert result is not None
        assert "workflow_type" in result
        assert result["workflow_type"] == "advisory"
    
    def test_configuration_loading(self):
        """Test that configuration loads correctly."""
        from ai_financial.core.config import settings
        
        assert settings is not None
        assert settings.environment in ["development", "staging", "production"]
        assert settings.api_host is not None
        assert settings.api_port > 0
    
    def test_agent_capabilities(self):
        """Test agent capabilities."""
        ai_cfo = AICFOAgent(industry="healthcare")
        
        capabilities = ai_cfo.get_capabilities()
        metadata = ai_cfo.get_metadata()
        
        assert len(capabilities) > 0
        assert "financial_analysis" in capabilities
        assert metadata["agent_id"] == "ai_cfo_agent"
        assert metadata["name"] == "AI CFO"
    
    def test_tool_capabilities(self):
        """Test tool capabilities."""
        ratio_tool = FinancialRatioTool()
        
        schema = ratio_tool.get_parameters_schema()
        info = ratio_tool.get_tool_info()
        
        assert schema is not None
        assert "properties" in schema
        assert "ratio_type" in schema["properties"]
        
        assert info["name"] == "financial_ratio_calculator"
        assert info["category"] == "financial_analysis"


class TestErrorHandling:
    """Test error handling and edge cases."""
    
    @pytest.mark.asyncio
    async def test_invalid_agent_routing(self):
        """Test routing to non-existent agent."""
        orchestrator = get_orchestrator()
        
        result = await orchestrator.route_request(
            request="Test request",
            preferred_agent="non_existent_agent"
        )
        
        assert result["success"] is False
        assert "not found" in result["error"]
    
    @pytest.mark.asyncio
    async def test_invalid_tool_execution(self):
        """Test execution of non-existent tool."""
        tool_hub = get_tool_hub()
        
        result = await tool_hub.execute_tool(
            tool_name="non_existent_tool",
            parameters={}
        )
        
        assert result.success is False
        assert "not found" in result.error
    
    @pytest.mark.asyncio
    async def test_invalid_tool_parameters(self):
        """Test tool execution with invalid parameters."""
        tool_hub = get_tool_hub()
        tool_hub.register_tool(FinancialRatioTool())
        
        result = await tool_hub.execute_tool(
            tool_name="financial_ratio_calculator",
            parameters={
                "invalid_param": "invalid_value"
            }
        )
        
        assert result.success is False
        assert "Invalid parameters" in result.error


if __name__ == "__main__":
    pytest.main([__file__])