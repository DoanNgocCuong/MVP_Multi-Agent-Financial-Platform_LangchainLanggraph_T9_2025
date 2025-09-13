"""Tool Hub for managing MCP tools and servers."""

from typing import Any, Dict, List, Optional, Type
import asyncio
from datetime import datetime

from ai_financial.core.config import settings
from ai_financial.core.logging import get_logger, get_tracer
from ai_financial.mcp.server import MCPServer, MCPToolDefinition
from ai_financial.mcp.tools.base_tool import BaseTool, ToolResult

logger = get_logger(__name__)
tracer = get_tracer(__name__)


class ToolHub:
    """Central hub for managing MCP tools and servers."""
    
    def __init__(self):
        """Initialize the Tool Hub."""
        self.servers: Dict[str, MCPServer] = {}
        self.tool_registry: Dict[str, str] = {}  # tool_name -> server_id mapping
        
        # Initialize default server
        self.default_server = MCPServer(
            server_id="default",
            name="Default MCP Server",
            description="Default server for AI Financial tools",
            host=settings.mcp.mcp_server_host,
            port=settings.mcp.mcp_server_port,
        )
        
        self.servers["default"] = self.default_server
        
        logger.info(
            "Tool Hub initialized",
            default_server_host=settings.mcp.mcp_server_host,
            default_server_port=settings.mcp.mcp_server_port,
        )
    
    def register_server(self, server: MCPServer) -> None:
        """Register an MCP server with the hub.
        
        Args:
            server: MCP server to register
        """
        with tracer.start_as_current_span("tool_hub.register_server"):
            server_id = server.server_id
            
            if server_id in self.servers:
                logger.warning(
                    "Server already registered, overwriting",
                    server_id=server_id,
                )
            
            self.servers[server_id] = server
            
            # Update tool registry
            for tool_name in server._tools.keys():
                self.tool_registry[tool_name] = server_id
            
            logger.info(
                "Server registered",
                server_id=server_id,
                server_name=server.name,
                tools_count=len(server._tools),
            )
    
    def unregister_server(self, server_id: str) -> bool:
        """Unregister an MCP server from the hub.
        
        Args:
            server_id: Server ID to unregister
            
        Returns:
            True if server was unregistered, False if not found
        """
        if server_id not in self.servers:
            return False
        
        server = self.servers[server_id]
        
        # Remove tools from registry
        tools_to_remove = [
            tool_name for tool_name, sid in self.tool_registry.items()
            if sid == server_id
        ]
        
        for tool_name in tools_to_remove:
            del self.tool_registry[tool_name]
        
        # Remove server
        del self.servers[server_id]
        
        logger.info(
            "Server unregistered",
            server_id=server_id,
            tools_removed=len(tools_to_remove),
        )
        
        return True
    
    def register_tool(
        self,
        tool: BaseTool,
        server_id: Optional[str] = None,
    ) -> None:
        """Register a tool with a server.
        
        Args:
            tool: Tool to register
            server_id: Server ID (defaults to 'default')
        """
        with tracer.start_as_current_span("tool_hub.register_tool"):
            server_id = server_id or "default"
            
            if server_id not in self.servers:
                raise ValueError(f"Server '{server_id}' not found")
            
            server = self.servers[server_id]
            server.register_tool(tool)
            
            # Update tool registry
            tool_name = tool.get_name()
            self.tool_registry[tool_name] = server_id
            
            logger.info(
                "Tool registered with hub",
                tool_name=tool_name,
                server_id=server_id,
                category=tool.get_category(),
            )
    
    def unregister_tool(self, tool_name: str) -> bool:
        """Unregister a tool from the hub.
        
        Args:
            tool_name: Name of tool to unregister
            
        Returns:
            True if tool was unregistered, False if not found
        """
        if tool_name not in self.tool_registry:
            return False
        
        server_id = self.tool_registry[tool_name]
        server = self.servers[server_id]
        
        success = server.unregister_tool(tool_name)
        
        if success:
            del self.tool_registry[tool_name]
            
            logger.info(
                "Tool unregistered from hub",
                tool_name=tool_name,
                server_id=server_id,
            )
        
        return success
    
    async def execute_tool(
        self,
        tool_name: str,
        parameters: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None,
    ) -> ToolResult:
        """Execute a tool by name.
        
        Args:
            tool_name: Name of tool to execute
            parameters: Tool parameters
            context: Execution context
            
        Returns:
            Tool execution result
        """
        with tracer.start_as_current_span("tool_hub.execute_tool") as span:
            span.set_attribute("tool_name", tool_name)
            
            if tool_name not in self.tool_registry:
                error_msg = f"Tool '{tool_name}' not found in hub"
                logger.error(error_msg)
                return ToolResult(
                    success=False,
                    error=error_msg,
                )
            
            server_id = self.tool_registry[tool_name]
            server = self.servers[server_id]
            
            return await server.execute_tool(tool_name, parameters, context)
    
    def get_available_tools(self) -> List[MCPToolDefinition]:
        """Get all available tools across all servers.
        
        Returns:
            List of tool definitions
        """
        tools = []
        
        for server in self.servers.values():
            tools.extend(server.get_tool_definitions())
        
        return tools
    
    def get_tools_by_category(self, category: str) -> List[MCPToolDefinition]:
        """Get tools by category.
        
        Args:
            category: Tool category
            
        Returns:
            List of tool definitions in the category
        """
        all_tools = self.get_available_tools()
        return [tool for tool in all_tools if tool.category == category]
    
    def get_tool_definition(self, tool_name: str) -> Optional[MCPToolDefinition]:
        """Get a specific tool definition.
        
        Args:
            tool_name: Name of the tool
            
        Returns:
            Tool definition if found, None otherwise
        """
        if tool_name not in self.tool_registry:
            return None
        
        server_id = self.tool_registry[tool_name]
        server = self.servers[server_id]
        
        return server.get_tool_definition(tool_name)
    
    def search_tools(
        self,
        query: str,
        category: Optional[str] = None,
    ) -> List[MCPToolDefinition]:
        """Search for tools by name or description.
        
        Args:
            query: Search query
            category: Optional category filter
            
        Returns:
            List of matching tool definitions
        """
        all_tools = self.get_available_tools()
        
        # Filter by category if specified
        if category:
            all_tools = [tool for tool in all_tools if tool.category == category]
        
        # Search in name and description
        query_lower = query.lower()
        matching_tools = []
        
        for tool in all_tools:
            if (query_lower in tool.name.lower() or 
                query_lower in tool.description.lower()):
                matching_tools.append(tool)
        
        return matching_tools
    
    async def start_all_servers(self) -> None:
        """Start all registered servers."""
        for server_id, server in self.servers.items():
            try:
                await server.start()
                logger.info(
                    "Server started",
                    server_id=server_id,
                )
            except Exception as e:
                logger.error(
                    "Failed to start server",
                    server_id=server_id,
                    error=str(e),
                )
    
    async def stop_all_servers(self) -> None:
        """Stop all registered servers."""
        for server_id, server in self.servers.items():
            try:
                await server.stop()
                logger.info(
                    "Server stopped",
                    server_id=server_id,
                )
            except Exception as e:
                logger.error(
                    "Failed to stop server",
                    server_id=server_id,
                    error=str(e),
                )
    
    def get_hub_status(self) -> Dict[str, Any]:
        """Get hub status information.
        
        Returns:
            Hub status dictionary
        """
        server_statuses = {}
        total_tools = 0
        
        for server_id, server in self.servers.items():
            server_info = server.get_server_info()
            server_statuses[server_id] = server_info
            total_tools += server_info["tools_count"]
        
        return {
            "servers_count": len(self.servers),
            "total_tools": total_tools,
            "tool_registry_size": len(self.tool_registry),
            "servers": server_statuses,
            "enabled_tool_categories": list(set(
                tool.category for tool in self.get_available_tools()
            )),
        }
    
    def get_hub_metrics(self) -> Dict[str, Any]:
        """Get hub metrics.
        
        Returns:
            Hub metrics dictionary
        """
        server_metrics = {}
        
        for server_id, server in self.servers.items():
            server_metrics[server_id] = server.get_metrics()
        
        return {
            "servers": server_metrics,
            "timestamp": datetime.utcnow().isoformat(),
        }


# Global tool hub instance
tool_hub = ToolHub()


def get_tool_hub() -> ToolHub:
    """Get the global tool hub instance.
    
    Returns:
        Tool hub instance
    """
    return tool_hub