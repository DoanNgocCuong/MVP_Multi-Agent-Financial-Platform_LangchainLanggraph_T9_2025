"""Base tool class for MCP tools."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, Field

from ai_financial.core.logging import get_logger, get_tracer

logger = get_logger(__name__)
tracer = get_tracer(__name__)


class ToolResult(BaseModel):
    """Tool execution result."""
    
    success: bool = Field(..., description="Whether execution was successful")
    data: Optional[Any] = Field(None, description="Result data")
    error: Optional[str] = Field(None, description="Error message if failed")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    execution_time: float = Field(default=0.0, description="Execution time in seconds")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "data": {"result": 1.5, "ratio_type": "current_ratio"},
                "metadata": {"calculation_method": "standard"},
                "execution_time": 0.025
            }
        }


class BaseTool(ABC):
    """Base class for all MCP tools."""
    
    def __init__(
        self,
        name: str,
        description: str,
        category: str = "general",
        version: str = "1.0.0",
        required_permissions: Optional[List[str]] = None,
    ):
        """Initialize the base tool.
        
        Args:
            name: Tool name
            description: Tool description
            category: Tool category
            version: Tool version
            required_permissions: Required permissions to execute tool
        """
        self.name = name
        self.description = description
        self.category = category
        self.version = version
        self.required_permissions = required_permissions or []
        
        # Execution metrics
        self._execution_count = 0
        self._total_execution_time = 0.0
        self._error_count = 0
        
        logger.info(
            "Tool initialized",
            tool_name=self.name,
            category=self.category,
            version=self.version,
        )
    
    @abstractmethod
    async def execute(
        self,
        parameters: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None,
    ) -> ToolResult:
        """Execute the tool with given parameters.
        
        Args:
            parameters: Tool parameters
            context: Execution context
            
        Returns:
            Tool execution result
        """
        pass
    
    @abstractmethod
    def get_parameters_schema(self) -> Dict[str, Any]:
        """Get the JSON schema for tool parameters.
        
        Returns:
            JSON schema dictionary
        """
        pass
    
    def get_name(self) -> str:
        """Get tool name.
        
        Returns:
            Tool name
        """
        return self.name
    
    def get_description(self) -> str:
        """Get tool description.
        
        Returns:
            Tool description
        """
        return self.description
    
    def get_category(self) -> str:
        """Get tool category.
        
        Returns:
            Tool category
        """
        return self.category
    
    def get_version(self) -> str:
        """Get tool version.
        
        Returns:
            Tool version
        """
        return self.version
    
    def get_required_permissions(self) -> List[str]:
        """Get required permissions.
        
        Returns:
            List of required permissions
        """
        return self.required_permissions
    
    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        """Validate tool parameters against schema.
        
        Args:
            parameters: Parameters to validate
            
        Returns:
            True if parameters are valid
        """
        # Basic validation - in a real implementation, this would use JSON schema validation
        schema = self.get_parameters_schema()
        required_params = schema.get("required", [])
        
        # Check required parameters
        for param in required_params:
            if param not in parameters:
                logger.error(
                    "Missing required parameter",
                    tool_name=self.name,
                    parameter=param,
                )
                return False
        
        return True
    
    def check_permissions(self, user_permissions: List[str]) -> bool:
        """Check if user has required permissions.
        
        Args:
            user_permissions: User's permissions
            
        Returns:
            True if user has all required permissions
        """
        if not self.required_permissions:
            return True
        
        missing_permissions = set(self.required_permissions) - set(user_permissions)
        
        if missing_permissions:
            logger.warning(
                "Insufficient permissions",
                tool_name=self.name,
                missing_permissions=list(missing_permissions),
            )
            return False
        
        return True
    
    def update_metrics(self, execution_time: float, success: bool) -> None:
        """Update tool execution metrics.
        
        Args:
            execution_time: Execution time in seconds
            success: Whether execution was successful
        """
        self._execution_count += 1
        self._total_execution_time += execution_time
        
        if not success:
            self._error_count += 1
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get tool execution metrics.
        
        Returns:
            Metrics dictionary
        """
        avg_execution_time = (
            self._total_execution_time / self._execution_count
            if self._execution_count > 0 else 0.0
        )
        
        error_rate = (
            self._error_count / self._execution_count
            if self._execution_count > 0 else 0.0
        )
        
        return {
            "execution_count": self._execution_count,
            "total_execution_time": self._total_execution_time,
            "average_execution_time": avg_execution_time,
            "error_count": self._error_count,
            "error_rate": error_rate,
            "success_rate": 1.0 - error_rate,
        }
    
    def get_tool_info(self) -> Dict[str, Any]:
        """Get comprehensive tool information.
        
        Returns:
            Tool information dictionary
        """
        return {
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "version": self.version,
            "required_permissions": self.required_permissions,
            "parameters_schema": self.get_parameters_schema(),
            "metrics": self.get_metrics(),
        }


class SimpleCalculationTool(BaseTool):
    """Simple calculation tool for demonstration."""
    
    def __init__(self):
        super().__init__(
            name="simple_calculator",
            description="Perform basic mathematical calculations",
            category="calculation",
            version="1.0.0",
        )
    
    async def execute(
        self,
        parameters: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None,
    ) -> ToolResult:
        """Execute calculation."""
        with tracer.start_as_current_span("simple_calculator.execute"):
            try:
                if not self.validate_parameters(parameters):
                    return ToolResult(
                        success=False,
                        error="Invalid parameters"
                    )
                
                operation = parameters.get("operation")
                operand1 = parameters.get("operand1")
                operand2 = parameters.get("operand2")
                
                if operation == "add":
                    result = operand1 + operand2
                elif operation == "subtract":
                    result = operand1 - operand2
                elif operation == "multiply":
                    result = operand1 * operand2
                elif operation == "divide":
                    if operand2 == 0:
                        return ToolResult(
                            success=False,
                            error="Division by zero"
                        )
                    result = operand1 / operand2
                else:
                    return ToolResult(
                        success=False,
                        error=f"Unknown operation: {operation}"
                    )
                
                return ToolResult(
                    success=True,
                    data={
                        "result": result,
                        "operation": operation,
                        "operands": [operand1, operand2]
                    }
                )
                
            except Exception as e:
                logger.error(
                    "Calculation failed",
                    tool_name=self.name,
                    error=str(e),
                )
                
                return ToolResult(
                    success=False,
                    error=f"Calculation failed: {str(e)}"
                )
    
    def get_parameters_schema(self) -> Dict[str, Any]:
        """Get parameters schema for calculator."""
        return {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["add", "subtract", "multiply", "divide"],
                    "description": "Mathematical operation to perform"
                },
                "operand1": {
                    "type": "number",
                    "description": "First operand"
                },
                "operand2": {
                    "type": "number", 
                    "description": "Second operand"
                }
            },
            "required": ["operation", "operand1", "operand2"]
        }