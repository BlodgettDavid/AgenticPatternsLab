"""
tests/iteration2/test_iteration2_registry.py

Unit tests for ToolRegistry functionality.
"""

from utils.tool_registry import ToolRegistry
from utils.tool_base import BaseTool
from typing import Any, Dict

class DummyTool(BaseTool):
    name = "dummy_tool"
    description = "A dummy tool for testing registry."
    parameters_schema: Dict[str, Any] = {}

    def execute(self, **kwargs) -> Any:
        return "success"

    def run(self, **kwargs) -> Any:
        return self.execute(**kwargs)

def test_registry_register_and_get():
    """Verify tools can be registered and retrieved from the registry."""
    registry = ToolRegistry()
    tool = DummyTool()
    
    registry.register(tool)
    retrieved = registry.get("dummy_tool")
    
    assert retrieved is tool

def test_registry_list_tools():
    """Verify the registry correctly lists registered tool names."""
    registry = ToolRegistry()
    registry.register(DummyTool())
    
    tools = registry.list_tools()
    assert "dummy_tool" in tools