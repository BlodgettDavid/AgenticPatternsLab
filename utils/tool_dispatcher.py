"""
utils/tool_dispatcher.py

Centralized dispatcher for routing tool execution requests safely through
the global tool registry and returning standardized ToolResults.
"""

from typing import Any, Dict, Optional
from utils.tool_base import ToolResult
from utils.tool_registry import global_tool_registry


class ToolDispatcher:
    """
    Handles dynamic lookup and execution of registered tools,
    ensuring safe error boundaries and standardized result formatting.
    """

    def __init__(self):
        self.registry = global_tool_registry

    def dispatch(self, tool_name: str, arguments: Dict[str, Any]) -> ToolResult:
        """
        Dispatches a tool call by name with provided keyword arguments.
        Returns a standardized ToolResult object.
        """
        tool = self.registry.get(tool_name)
        if not tool:
            return ToolResult(
                success=False,
                output=None,
                error=f"Tool '{tool_name}' not found in registry."
            )

        # Execute the tool using its built-in safety wrapper
        return tool.execute(**arguments)

    def get_available_tools_metadata(self) -> Dict[str, Dict[str, Any]]:
        """
        Retrieves all registered tool schemas for LLM function calling.
        """
        return self.registry.get_all_schemas()


# Global singleton dispatcher instance
global_tool_dispatcher = ToolDispatcher()