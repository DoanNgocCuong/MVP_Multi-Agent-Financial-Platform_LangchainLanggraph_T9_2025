"""MCP Server implementation following MCP standards."""

import asyncio
import json
from typing import Any, Dict, List, Optional, Callable
from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, Field

from ai_financial.core.config import settings
from ai_financial.core.logging import get_logger, get_tracer
from ai_financial.mcp.tools.base_tool import BaseTool, ToolResult

logger = get_logger(__name__)
tracer = get_tracer(__name__)


class MCPToolDefinition(BaseModel):
    """MCP tool definition following MCP standards."""
    
    name: str = Field(..., description="Tool name")
    description: str = Field(..., description="Tool description")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Tool parameters schema")
    required_permissions: List[str] = Field(default_factory=list, description="Required permissions")
    category: str = Field(default="general", description="Tool category")
    version: str = Field(default="1.0.0", description="Tool version")
    
    class Config:
        schema_extra = {
            "example": {
                "name": "calculate_financial_ratio",
                "description": "Calculate financial ratios from provided data",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "numerator": {"type": "number", "description": "Numerator value"},
                        "denominator": {"type": "number", "description": "Denominator value"},
                        "ratio_type": {"type": "string", "description": "Type of ratio"}
                    },
                    "required": ["numerator", "denominator"]
                },
                "category": "calculation",
                "required_permissions": ["read_financial_data"]
            }
        }


class MCPRequest(BaseModel):
    """MCP request model."""
    
    id: str = Field(default_factory=lambda: str(uuid4()))
    method: str = Field(..., description="Method name")
    params: Dict[str, Any] = Field(default_factory=dict, description="Method parameters")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class MCPResponse(BaseModel):
    """MCP response model."""
    
    id: str = Field(..., description="Request ID")
    result: Optional[Any] = Field(None, description="Result data")
    error: Optional[Dict[str, Any]] = Field(None, description="Error information")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class MCPServer:
    """MCP Server for managing and executing tools."""
    
    def __init__(
        self,
        server_id: str,
        name: str,
        description: str,
        host: str = "localhost",
        port: int = 8001,
    ):
        """Initialize MCP Server.
        
        Args:
            server_id: Unique server identifier
            name: Server name
            description: Server description
            host: Server host
            port: Server port
        """
        self.server_id = server_id
        self.name = name
        self.description = description
        self.host = host
        self.port = port
        
        # Tool registry
        self._tools: Dict[str, BaseTool] = {}
        self._tool_definitions: Dict[str, MCPToolDefinition] = {}
        
        # Server state
        self._running = False
        self._connections: Dict[str, Any] = {}
        
        logger.info(
            "MCP Server initialized",
            server_id=self.server_id,
            name=self.name,
            host=self.host,
            port=self.port,
        )
    
    def register_tool(self, tool: BaseTool) -> None:
        """Register a tool with the server.
        
        Args:
            tool: Tool instance to register
        """
        with tracer.start_as_current_span("mcp_server.register_tool"):
            tool_name = tool.get_name()
            
            if tool_name in self._tools:
                logger.warning(
                    "Tool already registered, overwriting",
                    tool_name=tool_name,
                    server_id=self.server_id,
                )
            
            self._tools[tool_name] = tool
            
            # Create tool definition
            definition = MCPToolDefinition(
                name=tool_name,
                description=tool.get_description(),
                parameters=tool.get_parameters_schema(),
                required_permissions=tool.get_required_permissions(),
                category=tool.get_category(),
                version=tool.get_version(),
            )
            
            self._tool_definitions[tool_name] = definition
            
            logger.info(
                "Tool registered",
                tool_name=tool_name,
                server_id=self.server_id,
                category=definition.category,
            )
    
    def unregister_tool(self, tool_name: str) -> bool:
        """Unregister a tool from the server.
        
        Args:
            tool_name: Name of tool to unregister
            
        Returns:
            True if tool was unregistered, False if not found
        """
        if tool_name in self._tools:
            del self._tools[tool_name]
            del self._tool_definitions[tool_name]
            
            logger.info(
                "Tool unregistered",
                tool_name=tool_name,
                server_id=self.server_id,
            )
            return True
        
        return False
    
    def get_tool_definitions(self) -> List[MCPToolDefinition]:
        """Get all registered tool definitions.
        
        Returns:
            List of tool definitions
        """
        return list(self._tool_definitions.values())
    
    def get_tool_definition(self, tool_name: str) -> Optional[MCPToolDefinition]:
        """Get a specific tool definition.
        
        Args:
            tool_name: Name of the tool
            
        Returns:
            Tool definition if found, None otherwise
        """
        return self._tool_definitions.get(tool_name)
    
    async def execute_tool(
        self,
        tool_name: str,
        parameters: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None,
    ) -> ToolResult:
        """Execute a registered tool.
        
        Args:
            tool_name: Name of tool to execute
            parameters: Tool parameters
            context: Execution context
            
        Returns:
            Tool execution result
        """
        with tracer.start_as_current_span("mcp_server.execute_tool") as span:
            span.set_attribute("tool_name", tool_name)
            
            if tool_name not in self._tools:
                error_msg = f"Tool '{tool_name}' not found"
                logger.error(error_msg, server_id=self.server_id)
                return ToolResult(
                    success=False,
                    error=error_msg,
                    execution_time=0.0,
                )
            
            tool = self._tools[tool_name]
            
            try:
                # Execute tool
                start_time = asyncio.get_event_loop().time()
                result = await tool.execute(parameters, context)
                execution_time = asyncio.get_event_loop().time() - start_time
                
                # Update execution time
                result.execution_time = execution_time
                
                logger.info(
                    "Tool executed successfully",
                    tool_name=tool_name,
                    server_id=self.server_id,
                    execution_time=execution_time,
                    success=result.success,
                )
                
                return result
                
            except Exception as e:
                execution_time = asyncio.get_event_loop().time() - start_time
                error_msg = f"Tool execution failed: {str(e)}"
                
                logger.error(
                    "Tool execution failed",
                    tool_name=tool_name,
                    server_id=self.server_id,
                    error=str(e),
                    execution_time=execution_time,
                )
                
                return ToolResult(
                    success=False,
                    error=error_msg,
                    execution_time=execution_time,
                )
    
    async def handle_request(self, request: MCPRequest) -> MCPResponse:
        """Handle an MCP request.
        
        Args:
            request: MCP request
            
        Returns:
            MCP response
        """
        with tracer.start_as_current_span("mcp_server.handle_request") as span:
            span.set_attribute("method", request.method)
            span.set_attribute("request_id", request.id)
            
            try:
                if request.method == "tools/list":
                    # List available tools
                    tools = [def_.model_dump() for def_ in self.get_tool_definitions()]
                    return MCPResponse(
                        id=request.id,
                        result={"tools": tools}
                    )
                
                elif request.method == "tools/call":
                    # Execute a tool
                    tool_name = request.params.get("name")
                    parameters = request.params.get("arguments", {})
                    
                    if not tool_name:
                        return MCPResponse(
                            id=request.id,
                            error={
                                "code": -32602,
                                "message": "Invalid params: 'name' is required"
                            }
                        )
                    
                    result = await self.execute_tool(tool_name, parameters)
                    
                    return MCPResponse(
                        id=request.id,
                        result=result.model_dump()
                    )
                
                elif request.method == "tools/get":
                    # Get tool definition
                    tool_name = request.params.get("name")
                    
                    if not tool_name:
                        return MCPResponse(
                            id=request.id,
                            error={
                                "code": -32602,
                                "message": "Invalid params: 'name' is required"
                            }
                        )
                    
                    definition = self.get_tool_definition(tool_name)
                    
                    if definition:
                        return MCPResponse(
                            id=request.id,
                            result=definition.model_dump()
                        )
                    else:
                        return MCPResponse(
                            id=request.id,
                            error={
                                "code": -32601,
                                "message": f"Tool '{tool_name}' not found"
                            }
                        )
                
                else:
                    return MCPResponse(
                        id=request.id,
                        error={
                            "code": -32601,
                            "message": f"Method '{request.method}' not found"
                        }
                    )
                    
            except Exception as e:
                logger.error(
                    "Request handling failed",
                    method=request.method,
                    request_id=request.id,
                    error=str(e),
                )
                
                return MCPResponse(
                    id=request.id,
                    error={
                        "code": -32603,
                        "message": f"Internal error: {str(e)}"
                    }
                )
    
    async def start(self) -> None:
        """Start the MCP server."""
        if self._running:
            logger.warning("Server already running", server_id=self.server_id)
            return
        
        self._running = True
        
        logger.info(
            "MCP Server started",
            server_id=self.server_id,
            host=self.host,
            port=self.port,
            tools_count=len(self._tools),
        )
    
    async def stop(self) -> None:
        """Stop the MCP server."""
        if not self._running:
            return
        
        self._running = False
        
        # Close all connections
        for connection_id in list(self._connections.keys()):
            await self._close_connection(connection_id)
        
        logger.info(
            "MCP Server stopped",
            server_id=self.server_id,
        )
    
    async def _close_connection(self, connection_id: str) -> None:
        """Close a client connection.
        
        Args:
            connection_id: Connection identifier
        """
        if connection_id in self._connections:
            del self._connections[connection_id]
            
            logger.info(
                "Connection closed",
                connection_id=connection_id,
                server_id=self.server_id,
            )
    
    def is_running(self) -> bool:
        """Check if server is running.
        
        Returns:
            True if server is running
        """
        return self._running
    
    def get_server_info(self) -> Dict[str, Any]:
        """Get server information.
        
        Returns:
            Server information dictionary
        """
        return {
            "server_id": self.server_id,
            "name": self.name,
            "description": self.description,
            "host": self.host,
            "port": self.port,
            "running": self._running,
            "tools_count": len(self._tools),
            "connections_count": len(self._connections),
            "registered_tools": list(self._tools.keys()),
        }
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get server metrics.
        
        Returns:
            Server metrics dictionary
        """
        # In a real implementation, this would collect actual metrics
        return {
            "requests_processed": 0,
            "tools_executed": 0,
            "average_response_time": 0.0,
            "error_rate": 0.0,
            "uptime_seconds": 0,
        }