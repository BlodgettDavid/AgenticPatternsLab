"""
utils/tool_registry.py

Provides a centralized registry for: 
    managing, registering, and retrieving tool instances 
    across AgenticPatternsLab.


What this achieves:
    Singleton & Instance Management: 
    Provides a clean ToolRegistry class 
    as well as a pre-instantiated global_tool_registry object 
    for convenient app-wide imports.

Schema Exporting (get_all_schemas): 
    -Aggregates metadata across all registered tools so LLMs can dynamically inspect tool definitions.
    =Type-Safe Registration: Ensures only valid subclasses of BaseTool can be added to the registry.
"""

from typing import Any, Dict, List, Optional
from utils.tool_base import BaseTool


class ToolRegistry:
    """
    Centralized registry to store and manage tool instances, their descriptions,
    and their schemas.
    """

    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        """
        Registers a tool instance into the registry.
        """
        if not isinstance(tool, BaseTool):
            raise TypeError(f"Object {tool} must inherit from BaseTool.")
        
        if tool.name in self._tools:
            # Overwrite or log warning for duplicate registrations
            pass
            
        self._tools[tool.name] = tool

    def get(self, name: str) -> Optional[BaseTool]:
        """
        Retrieves a registered tool instance by its name.
        """
        return self._tools.get(name)

    def list_tools(self) -> List[str]:
        """
        Returns a list of all registered tool names.
        """
        return list(self._tools.keys())

    def get_all_schemas(self) -> Dict[str, Dict[str, Any]]:
        """
        Returns metadata schemas for all registered tools, useful for
        exposing tool capabilities to LLM function-calling interfaces.
        """
        schemas = {}
        for name, tool in self._tools.items():
            schemas[name] = {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.parameters_schema
            }
        return schemas


# Global singleton instance for easy import across modules
global_tool_registry = ToolRegistry()